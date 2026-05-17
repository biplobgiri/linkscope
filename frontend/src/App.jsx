import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [longUrl, setLongUrl] = useState("");
  const [customSlug, setCustomSlug] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleShorten = async () => {
    setError(null);
    setResult(null);
    setLoading(true);

    let url=longUrl.trim();
    if (!url.startsWith("http://") && !url.startsWith("https://")){
      url="http://"+url;
    }

    try {
      const response = await axios.post(`${API_URL}/shorten`, {
        original_url: longUrl,
        custom_slug: customSlug || undefined,
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(result.short_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>LinkScope</h1>
        <p style={styles.subtitle}>Shorten and track your links</p>

        <input
          style={styles.input}
          type="text"
          placeholder="Paste your long URL here"
          value={longUrl}
          onChange={(e) => setLongUrl(e.target.value)}
        />

        <input
          style={styles.input}
          type="text"
          placeholder="Custom slug (optional)"
          value={customSlug}
          onChange={(e) => setCustomSlug(e.target.value)}
        />

        <button
          style={styles.button}
          onClick={handleShorten}
          disabled={!longUrl || loading}
        >
          {loading ? "Shortening..." : "Shorten"}
        </button>

        {error && <p style={styles.error}>{error}</p>}

        {result && (
          <div style={styles.result}>
            <p style={styles.resultLabel}>Your short link</p>
            <div style={styles.resultRow}>
              <a href={result.short_url} target="_blank" style={styles.link}>
                {result.short_url}
              </a>
              <button style={styles.copyBtn} onClick={handleCopy}>
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f5f5f5",
    fontFamily: "sans-serif",
  },
  card: {
    background: "#fff",
    padding: "2rem",
    borderRadius: "12px",
    width: "100%",
    maxWidth: "480px",
    boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
  },
  title: { fontSize: "24px", fontWeight: "600", marginBottom: "4px" },
  subtitle: { fontSize: "14px", color: "#888", marginBottom: "1.5rem" },
  input: {
    width: "100%",
    padding: "10px 12px",
    fontSize: "14px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    marginBottom: "12px",
    boxSizing: "border-box",
  },
  button: {
    width: "100%",
    padding: "10px",
    fontSize: "15px",
    fontWeight: "500",
    backgroundColor: "#111",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  error: { color: "#e53e3e", fontSize: "13px", marginTop: "12px" },
  result: {
    marginTop: "1.5rem",
    padding: "1rem",
    background: "#f9f9f9",
    borderRadius: "8px",
    border: "1px solid #eee",
  },
  resultLabel: { fontSize: "12px", color: "#888", marginBottom: "6px" },
  resultRow: { display: "flex", alignItems: "center", gap: "8px" },
  link: { fontSize: "14px", color: "#2563eb", flex: 1, wordBreak: "break-all" },
  copyBtn: {
    padding: "6px 12px",
    fontSize: "13px",
    border: "1px solid #ddd",
    borderRadius: "6px",
    cursor: "pointer",
    background: "#fff",
  },
};