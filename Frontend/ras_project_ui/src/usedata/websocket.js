// websocket.js
const initWebSocket = () => {
  const ws = new WebSocket(process.env.VUE_APP_WEBSOCKET_URL);
  return ws;
};


const getCurrentData = () => {
  const today = new Date();
  const dd = String(today.getDate()).padStart(2,'0');
  const mm = String(today.getMonth() + 1).padStart(2,'0');
  const yyyy = today.getFullYear();

  return yyyy + '-' + mm + '-' + dd;
}


export default {
  initWebSocket,
  getCurrentData
};
