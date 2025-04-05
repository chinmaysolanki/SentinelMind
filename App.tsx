import React from 'react';
import ActionMonitor from '../dashboard/ActionMonitor';

function App() {
  return (
    <div className="App">
      <header style={{ padding: '20px', backgroundColor: '#f5f5f5' }}>
        <h1>Cyber Brain Dashboard</h1>
      </header>
      <main style={{ padding: '20px' }}>
        <ActionMonitor />
      </main>
    </div>
  );
}

export default App; 