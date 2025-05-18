import React, { useState } from 'react';
import ChatPanel from './ChatPanel';
import ChatIcon from '@mui/icons-material/Chat';
import Button from '@mui/material/Button';

const ChatBot = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="chatbot-container">
            {isOpen ?
                <ChatPanel onClose={() => setIsOpen(false)} />
                :
                <Button
                    onClick={() => setIsOpen(!isOpen)}
                    sx={{
                        minWidth: '60px',
                        minHeight: '60px',
                        borderRadius: '50%',
                        backgroundColor: 'primary.main',
                        color: 'primary.contrastText',
                    }}
                >
                    <ChatIcon fontSize="large" />
                </Button>
            }
        </div>
    )
};

export default ChatBot;