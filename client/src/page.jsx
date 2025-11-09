import React, { useState } from "react";
import "./page.css";

const EmotionAnalyzer = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeEmotion = async () => {
    setError("");
    setResult(null);
    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:4000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Server not reachable. Make sure Node & Flask are running.");
    }
    setLoading(false);
  };

  return (
    <div className="emotion-container">
      <h2 className="emotion-title">🎭 Emotion Detection App</h2>

      <textarea
        className="emotion-textarea"
        rows="5"
        placeholder="Type something to analyze..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={analyzeEmotion}
        className="emotion-button"
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Emotion"}
      </button>

      {error && <p className="emotion-error">{error}</p>}

      {result && (
        <div className="emotion-result-box">
          <h3>Detected Emotion: {result.emotion}</h3>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
};

export default EmotionAnalyzer;
