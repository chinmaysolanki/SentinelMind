import React, { useState } from 'react';
import './ExplanationPanel.css';

const ExplanationPanel = ({ threat, action }) => {
  const [explanation, setExplanation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchExplanation = async (threat, action) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch("http://localhost:5000/api/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ threat, action }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch explanation');
      }
      
      const data = await response.json();
      setExplanation(data.explanation);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExplain = () => {
    if (threat && action) {
      fetchExplanation(threat, action);
    }
  };

  return (
    <div className="explanation-panel">
      <h3>AI Explanation</h3>
      <button 
        onClick={handleExplain}
        disabled={loading || !threat || !action}
        className="explain-button"
      >
        {loading ? 'Loading...' : 'Explain Decision'}
      </button>
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
      
      {explanation && (
        <div className="explanation-content">
          <p>{explanation}</p>
        </div>
      )}
    </div>
  );
};

export default ExplanationPanel; 