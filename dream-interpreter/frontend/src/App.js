import React from 'react';
import { DreamForm, InterpretationResult } from './components';

function App() {
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleInterpret = async (dreamText) => {
    setLoading(true);
    setResult(null);
    try {
        // Backend runs on port 3000
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:3000';
        const response = await fetch(`${backendUrl}/api/interpret`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ dreamText }),
        });
        const data = await response.json();
        if (data.success) {
            setResult(data.interpretation);
        } else {
            alert('Error interpreting dream');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to server. Make sure the backend is running on port 3000.');
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>AI梦境解析</h1>
      <DreamForm onInterpret={handleInterpret} loading={loading} />
      {result && <InterpretationResult result={result} />}
    </div>
  );
}

export default App;
