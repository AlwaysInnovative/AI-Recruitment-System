export const setupSocket = (onMessage) => {
  const socket = new WebSocket('wss://ai-recruitment-system.onrender.com/ws');

  socket.onopen = () => {
    console.log('WebSocket connected');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onclose = () => {
    console.log('WebSocket disconnected');
  };

  return socket;
};
