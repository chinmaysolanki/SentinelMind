import React, { useState, useEffect } from 'react';
import './App.css';
import ExplanationPanel from './components/ExplanationPanel';

function App() {
  const [threats, setThreats] = useState([]);
  const [actions, setActions] = useState([]);
  const [selectedThreat, setSelectedThreat] = useState(null);
  const [selectedAction, setSelectedAction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch threats and actions from the backend
    const fetchData = async () => {
      try {
        setLoading(true);
        const [threatsResponse, actionsResponse] = await Promise.all([
          fetch('http://localhost:5000/api/threats'),
          fetch('http://localhost:5000/api/actions')
        ]);

        if (!threatsResponse.ok || !actionsResponse.ok) {
          throw new Error('Failed to fetch data');
        }

        const threatsData = await threatsResponse.json();
        const actionsData = await actionsResponse.json();

        setThreats(threatsData);
        setActions(actionsData);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleThreatSelect = (threat) => {
    setSelectedThreat(threat);
    // Find the corresponding action for this threat
    const action = actions.find(a => a.threat_id === threat.id);
    setSelectedAction(action || null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cyber Brain Dashboard</h1>
      </header>
      
      <main className="App-main">
        {loading ? (
          <div className="loading">Loading data...</div>
        ) : error ? (
          <div className="error">Error: {error}</div>
        ) : (
          <div className="dashboard-container">
            <div className="threats-panel">
              <h2>Threats</h2>
              <div className="threats-list">
                {threats.map(threat => (
                  <div 
                    key={threat.id} 
                    className={`threat-item ${selectedThreat?.id === threat.id ? 'selected' : ''}`}
                    onClick={() => handleThreatSelect(threat)}
                  >
                    <h3>{threat.type}</h3>
                    <p>{threat.summary}</p>
                    <div className="threat-meta">
                      <span className={`severity ${threat.severity}`}>{threat.severity}</span>
                      <span className="source">{threat.source}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="actions-panel">
              <h2>Actions</h2>
              {selectedAction ? (
                <div className="action-details">
                  <h3>{selectedAction.action}</h3>
                  <p>Confidence: {Math.round(selectedAction.confidence * 100)}%</p>
                  <p>Reward: {Math.round(selectedAction.reward * 100)}%</p>
                </div>
              ) : (
                <div className="no-selection">
                  <p>Select a threat to see its action</p>
                </div>
              )}
            </div>
            
            {selectedThreat && selectedAction && (
              <ExplanationPanel 
                threat={selectedThreat} 
                action={selectedAction} 
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 