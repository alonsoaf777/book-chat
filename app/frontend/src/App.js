// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [chat, setChat] = useState([]); // conversación

  const handleSend = async () => {
    if (!query.trim()) return;

    
    // Agrega tu mensaje al chat
    const userMessage = { sender: 'user', text: query };
    setChat((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post('https://book-container-app.ambitiouswave-854a51bb.westus2.azurecontainerapps.io/recommend', { query });
      const botMessage = { sender: 'bot', text: res.data.response};
      setChat((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMsg = { sender: 'bot', text: '⚠️ Hubo un error. Intenta de nuevo.' };
      setChat((prev) => [...prev, errorMsg]);
    }

    setQuery('');
  };

  return (
    <div className="chat-container">
      <h1>BookBotAAF</h1>

      <div className="chat-box">
        {chat.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <div className="text">{msg.text}</div>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="What do you want to read today?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
