import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Link, Click

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)


# ── shorten ────────────────────────────────────────────────

def test_shorten_valid_url():
    response = client.post("/shorten", json={
        "original_url": "https://example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert "slug" in data
    assert "short_url" in data
    assert data["original_url"] == "https://example.com"


def test_shorten_custom_slug():
    response = client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_slug": "mylink"
    })
    assert response.status_code == 200
    assert response.json()["slug"] == "mylink"


def test_shorten_duplicate_slug():
    client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_slug": "duplicate"
    })
    response = client.post("/shorten", json={
        "original_url": "https://google.com",
        "custom_slug": "duplicate"
    })
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_shorten_invalid_url():
    response = client.post("/shorten", json={
        "original_url": "not-a-url"
    })
    assert response.status_code == 422


# ── redirect ───────────────────────────────────────────────

def test_redirect_valid_slug():
    shorten = client.post("/shorten", json={
        "original_url": "https://example.com"
    })
    slug = shorten.json()["slug"]

    response = client.get(f"/r/{slug}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "https://example.com"


def test_redirect_unknown_slug():
    response = client.get("/r/unknown123", follow_redirects=False)
    assert response.status_code == 302


def test_redirect_inactive_link():
    shorten = client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_slug": "inactive"
    })

    db = TestingSessionLocal()
    link = db.query(Link).filter(Link.slug == "inactive").first()
    link.is_active = False
    db.commit()
    db.close()

    response = client.get("/r/inactive", follow_redirects=False)
    assert response.status_code == 302


# ── stats ──────────────────────────────────────────────────

def test_stats_valid_slug():
    client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_slug": "statstest"
    })

    response = client.get("/stats/statstest")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "statstest"
    assert data["total_clicks"] == 0
    assert data["is_active"] is True


def test_stats_unknown_slug():
    response = client.get("/stats/doesnotexist")
    assert response.status_code == 404


def test_stats_summary():
    client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_slug": "testslug"
    })

    response = client.get("/stats/testslug/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_clicks" in data
    assert "top_countries" in data
    assert "top_referrers" in data


# ── health ─────────────────────────────────────────────────

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}