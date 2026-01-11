import React, { useState } from 'react';

export function DreamForm({ onInterpret, loading }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onInterpret(text);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '2rem 0' }}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe your dream here..."
        rows={6}
        style={{ width: '100%', padding: '1rem', marginBottom: '1rem', borderRadius: '8px', border: '1px solid #ccc', boxSizing: 'border-box' }}
      />
      <button 
        type="submit" 
        disabled={loading}
        style={{ 
            padding: '0.5rem 2rem', 
            fontSize: '1.2rem', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Interpreting...' : 'Interpret Dream'}
      </button>
    </form>
  );
}

export function InterpretationResult({ result }) {
  return (
    <div style={{ 
        textAlign: 'left', 
        padding: '2rem', 
        backgroundColor: 'white', 
        borderRadius: '8px', 
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)' 
    }}>
      <h3>Interpretation:</h3>
      <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{result}</p>
    </div>
  );
}
