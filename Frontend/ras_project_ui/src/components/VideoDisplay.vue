<template>
  <div id="imageContainer">
    <table>
      <tr>
        <td>
          <div class="rectangle">
            <img id="liveImage" :src="isStreaming ? videoSource : ''" alt="Live Image">
          </div>
        </td>
        <td>
          <div class="rectangle" id="serve_img">

        </div>
      </td>

      </tr>
      <button @click="startStreaming" id="camera_start_btn">Start Streaming</button>
      <tr>
        <td>
          <div class="rectangle2" id="user_it">
            <div id="user_input">
            <input type="text" placeholder="이름">
            <input type="text" placeholder="전화번호">
            <input type="date">
          </div>
        </div>
        <button id="info_btn">등록</button>
      </td>

      <td>
        <div class="rectangle2" id="log_it">
   
          <div id="footer"></div>
      </div>
     </td>

      </tr>
    </table>
  </div>
  <!-- 생략... -->
</template>

<script>
import websocket from '../usedata/websocket'; 
import '../css/main.css';

export default {
  data() {
    return {
      videoSource: '',
      isStreaming: false,
      ws: null,
    };
  },

  methods: {
    startStreaming() {
      this.isStreaming = true;
      this.ws = websocket.initWebSocket();

      this.ws.onmessage = event => {
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        this.videoSource = URL.createObjectURL(blob);
      };

      this.ws.onclose = event => {
        console.error("WebSocket closed:", event);
      };
    },
  },
};
</script>
