import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { sendMessage } from '../store/slices/chatSlice';
import { Bot, Send, User } from 'lucide-react';

const ChatInterface = () => {
  const dispatch = useDispatch();
  const { history, status } = useSelector((state) => state.chat);
  const formData = useSelector((state) => state.interaction.formData);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [history]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    dispatch(sendMessage(input));
    setInput('');
  };

  return (
    <div className="glass-card fade-in chat-container">
      <div className="chat-header">
        <Bot size={24} color="var(--primary-color)" />
        <h2>AI Assistant</h2>
      </div>
      
      <div className="chat-messages">
        {history.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '2rem' }}>
            <p>Describe your interaction with the HCP.</p>
            <p style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>E.g. "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure"</p>
          </div>
        )}
        
        {history.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
              <span style={{ fontSize: '0.8rem', opacity: 0.8 }}>
                {msg.role === 'user' ? 'You' : 'AI Assistant'}
              </span>
            </div>
            {msg.content}
          </div>
        ))}
        {status === 'loading' && (
          <div className="message assistant">
            <span style={{ fontStyle: 'italic', opacity: 0.7 }}>Agent is typing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input" onSubmit={handleSend}>
        <input 
          type="text" 
          placeholder="Describe interaction..." 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={status === 'loading'}
        />
        <button type="submit" className="btn btn-primary" disabled={status === 'loading' || !input.trim()}>
          <Send size={16} />
        </button>
      </form>
      
      <div className="action-buttons" style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
        <button 
          className="btn btn-secondary" 
          disabled={status === 'loading'}
          style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', border: '1px solid var(--border-color)', borderRadius: '4px', background: 'transparent', cursor: 'pointer' }}
          type="button"
          onClick={() => {
             const hcpName = formData?.hcp_name || 'Dr. Wilson';
             dispatch(sendMessage(`Show previous interactions with ${hcpName}`));
          }}
        >
          Fetch History
        </button>
        <button 
          className="btn btn-secondary" 
          disabled={status === 'loading'}
          style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', border: '1px solid var(--border-color)', borderRadius: '4px', background: 'transparent', cursor: 'pointer' }}
          type="button"
          onClick={() => {
             const hcpName = formData?.hcp_name || 'Dr. Wilson';
             dispatch(sendMessage(`Suggest follow-up actions for ${hcpName} based on previous interactions.`));
          }}
        >
          Suggest Follow-up
        </button>
        <button 
          className="btn btn-secondary" 
          disabled={status === 'loading'}
          style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', border: '1px solid var(--border-color)', borderRadius: '4px', background: 'transparent', cursor: 'pointer' }}
          type="button"
          onClick={() => {
             const id = window.prompt("Enter Interaction ID:");
             if (!id) return;
             const field = window.prompt("Enter field to update (e.g., sentiment, topics_discussed):");
             if (!field) return;
             const val = window.prompt("Enter new value:");
             if (!val) return;
             dispatch(sendMessage(`Update interaction ID ${id}. Change ${field} to ${val}.`));
          }}
        >
          Edit Interaction
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
