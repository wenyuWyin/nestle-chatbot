// This will be your API service layer
export const ChatService = {
  async sendMessage(message) {
    // TODO: Replace with actual API call
    console.log('API would send:', message);
    
    // Simulate API response
    return new Promise(resolve => {
      setTimeout(() => {
        resolve({
          text: "This is a simulated response to: " + message,
          isUser: false,
          timestamp: new Date()
        });
      }, 800);
    });
  }
};