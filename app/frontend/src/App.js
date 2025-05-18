import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { ChatProvider } from './contexts/ChatContext';
import nestleImage from './assets/nestle.png';
import ChatBot from './components/ChatBot';

// Theme configuration
const theme = createTheme({
  palette: {
    primary: { main: '#2a528b', contrastText: '#ffffff' },
    secondary: { main: '#f3f4f6', contrastText: '#2a528b' }
  },
  components: {
    MuiButton: { styleOverrides: { root: { textTransform: 'none' } } }
  }
});

// Style objects
const backgroundStyle = {
  backgroundImage: `url(${nestleImage})`,
  backgroundSize: 'cover',
  height: '100vh',
  width: '100vw',
  position: 'fixed'
};

const chatbotContainerStyle = {
  position: 'fixed',
  bottom: '24px',
  right: '24px',
  zIndex: 1000
};

// Main App component
function App() {
  return (
    <ThemeProvider theme={theme}>
      <ChatProvider>
        <div 
          className="app-background"
          style={backgroundStyle}
        >
          <div style={chatbotContainerStyle}>
            <ChatBot />
          </div>
        </div>
      </ChatProvider>
    </ThemeProvider>
  );
}

export default App;