import React from 'react';
import InteractionForm from '../components/InteractionForm';
import ChatInterface from '../components/ChatInterface';

const HomePage = () => {
  return (
    <div className="app-container">
      <header className="header fade-in">
        <h1>Log HCP Interaction</h1>
        <p>Record your interaction details using the structured form or our AI assistant.</p>
      </header>
      
      <div className="layout-grid">
        <InteractionForm />
        <ChatInterface />
      </div>
    </div>
  );
};

export default HomePage;
