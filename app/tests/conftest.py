import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture(autouse=True)
def mock_redis():
    with patch("app.services.cache.get_cached_url", new_callable=AsyncMock) as mock_get, \
         patch("app.services.cache.set_cached_url", new_callable=AsyncMock) as mock_set, \
         patch("app.services.cache.delete_cached_url", new_callable=AsyncMock) as mock_delete:
        mock_get.return_value = None
        yield mock_get, mock_set, mock_delete