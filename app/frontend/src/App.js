
import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import nestleImage from './assets/nestle.png'
import ChatBot from './components/ChatBot';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App" style={{ 
        backgroundImage: `url(${nestleImage})`,
        backgroundSize: 'cover',
        height: '100vh',
        width: '100vw',
        position: 'fixed',
      }}>
        <div style={{
          position: 'fixed',
          bottom: '24px',
          right: '50px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          zIndex: 1000,
        }}>
          <ChatBot />
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
