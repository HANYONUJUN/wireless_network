// websocket.js
const initWebSocket = () => {
  const ws = new WebSocket(process.env.VUE_APP_WEBSOCKET_URL);
  return ws;
};

export default {
  initWebSocket,
};
