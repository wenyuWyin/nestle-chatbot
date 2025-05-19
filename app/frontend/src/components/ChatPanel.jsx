import React, { useState } from 'react';
import {
    IconButton,
    Avatar,
    Card,
    Box,
    CardHeader,
    CardContent,
    CardActions,
    Typography,
    TextField,
} from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import SendIcon from '@mui/icons-material/Send';
import CloseIcon from '@mui/icons-material/Close';
import PersonOutlineOutlinedIcon from '@mui/icons-material/PersonOutlineOutlined';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { useChat } from '../contexts/ChatContext';
import { sendMessage } from '../api/ChatService';


const MessageBubble = ({ message }) => (
    <Box sx={{
        display: 'flex',
        flexDirection: message.isUser ? 'row-reverse' : 'row',
        alignItems: 'flex-end',
        mb: 2,
        gap: 1
    }}>
        <Avatar sx={{
            bgcolor: message.isUser ? 'secondary.main' : 'primary.main',
            color: message.isUser ? 'secondary.contrastText' : 'primary.contrastText',
            width: 32,
            height: 32,
        }}>
            {message.isUser ? <PersonOutlineOutlinedIcon /> : <SmartToyIcon />}
        </Avatar>

        <Box sx={{
            maxWidth: '70%',
            p: 1,
            borderRadius: 2,
            bgcolor: message.isUser ? 'secondary.main' : 'primary.main',
            color: message.isUser ? 'secondary.contrastText' : 'primary.contrastText',
            boxShadow: !message.isUser && 1,
        }}>
            <Typography variant="body2">{message.text}</Typography>
            <Typography variant="caption" sx={{
                display: 'block',
                mt: 1,
                textAlign: 'right',
                color: message.isUser ? 'secondary.contrastText' : 'primary.contrastText',
                fontSize: '0.7rem'
            }}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </Typography>

        </Box>
    </Box>
);

//TODO
const TypingIndicator = () => (
    <Box sx={{
        alignSelf: 'flex-start',
        p: 1.5,
        mb: 1.5,
        borderRadius: 4,
        bgcolor: 'grey.100',
        maxWidth: '40%'
    }}>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
            Assistant is typing...
        </Typography>
    </Box>
);

const ChatPanel = ({ onClose }) => {
    const {
        messages,
        addMessage,
        isLoading,
        setIsLoading,
        error
    } = useChat();
    const [input, setInput] = useState('');

    const handleSend = async () => {
        // Disable function if input is empty and/or answer is loading
        if (!input.trim() || isLoading) return;

        // Add user message
        const userMessage = {
            text: input,
            isUser: true,
            timestamp: new Date()
        };
        addMessage(userMessage);
        setInput('');
        setIsLoading(true);

        //TODO
        try {
            // API CALL POINT - Replace with real implementation
            const response = await sendMessage(input);
            const botResponse = {
                text: response.response,
                isUser: false,
                timestamp: new Date()
            }
            addMessage(botResponse);
        } catch (error) {
            addMessage({
                text: "Sorry, I encountered an error",
                isUser: false,
                timestamp: new Date()
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card
            sx={{
                display: 'flex',
                flexDirection: 'column',
                width: '45vh',
                height: '80vh',
                maxHeight: '700px',
                minHeight: '400px',
            }}>
            {/* Header */}
            <CardHeader
                sx={{ bgcolor: '#002e6e' }}
                avatar={
                    <Avatar sx={{ bgcolor: 'white' }}>
                        <ChatIcon sx={{ color: 'primary.main' }} />
                    </Avatar>
                }
                action={
                    <IconButton
                        onClick={onClose}
                        aria-label="close"
                        sx={{ color: 'white' }}
                    >
                        <CloseIcon />
                    </IconButton>
                }
                title={
                    <Typography
                        variant="subtitle1"
                        sx={{ color: 'white', fontWeight: 550 }}>
                        Nestlé Assistant
                    </Typography>
                }
            />

            {/* Chat History Display */}
            <CardContent sx={{
                flex: 1,
                overflowY: 'auto',
                p: 1.5,
                '&::-webkit-scrollbar': {
                    width: '6px'
                },
                '&::-webkit-scrollbar-thumb': {
                    backgroundColor: 'grey.400',
                    borderRadius: 3,
                },
            }}>
                {messages.map((message, index) => (
                    <MessageBubble key={index} message={message} />
                ))}
                {isLoading && <TypingIndicator />}
            </CardContent>

            {/* Input Field */}
            <CardActions sx={{
                p: 1,
                border: '1px solid primary.main',
            }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    size="small"
                    placeholder="Ask me anything..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    disabled={isLoading}
                />
                <IconButton
                    color="primary"
                    onClick={handleSend}
                    disabled={!input.trim() || isLoading}
                >
                    <SendIcon />
                </IconButton>
            </CardActions>
        </Card>
    );
};

export default ChatPanel;