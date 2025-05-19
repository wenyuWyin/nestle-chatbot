

// export const ChatService = {
//   async sendMessage(message) {
//     // TODO: Replace with actual API call
//     console.log('API would send:', message);
    
//     // Simulate API response
//     return new Promise(resolve => {
//       setTimeout(() => {
//         resolve({
//           text: "This is a simulated response to: " + message,
//           isUser: false,
//           timestamp: new Date()
//         });
//       }, 800);
//     });
//   }
// };

import { API_CONFIG } from './config';

export const sendMessage = async (message) => {
  const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SEND_MESSAGE}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  if (!response.ok) throw new Error('Failed to send message');
  return await response.json();
};