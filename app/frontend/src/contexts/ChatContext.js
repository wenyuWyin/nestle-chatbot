import { createContext, useContext, useState } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
    const [messages, setMessages] = useState([
        {
            text: "Hello! I'm xxx, your personal MadeWithNestlé assistant. Ask me anything, and I'll quickly search the entire site to find the answers you need!",
            isUser: false,
            timestamp: new Date(),
        }
    ]);

    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)

    const addMessage = (newMessage) => {
        setMessages(prev => [...prev, newMessage]);
    };

    return (
        <ChatContext.Provider value={{
            messages,
            addMessage,
            isLoading,
            setIsLoading,
            error,
            setError
        }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error('useChat must be used within a ChatProvider');
    }
    return context;
};