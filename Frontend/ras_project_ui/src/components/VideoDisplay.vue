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
              <input type="text" v-model="name" placeholder="이름">
              <input type="text" v-model="phone" placeholder="전화번호">
              <input type="date" v-model="date">
            </div>
          </div>
          <button id="info_btn">등록</button>
        </td>

        <td>
          <div class="rectangle2" id="log_it">
            <div>
              <div v-for="log in logs" :key="log.seq">
                <p>{{ log.administrator }}</p>
                <p>{{ log.phone }}</p>
                <p>{{ log.logtime }}</p>
                <p>{{ log.logpath }}</p>
                <p>{{ log.smsflag }}</p>
              </div>
            </div>
            <div id="footer"></div>
          </div>
        </td>

      </tr>
    </table>
  </div>
</template>

<script>
import websocket from '../usedata/websocket';
import '../css/main.css';
//import axios from 'axios';


export default {
  data() {
    return {
      videoSource: '',
      isStreaming: false,
      ws: null,
      name: "",
      phone: "",
      logs: [],  // logs 배열 추가
      date: "",
    };
  },
  methods: {
    startStreaming() {
      this.isStreaming = true;
      this.ws = websocket.initWebSocket();

      this.ws.onopen = () => {
        this.ws.send(this.name + "," + this.phone);
      };

      this.ws.onmessage = event => {
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        this.videoSource = URL.createObjectURL(blob);
      };

      this.ws.onclose = event => {
        console.error("WebSocket closed:", event);
      };
    },
    setCurrentData() {
      this.date = websocket.getCurrentData(); //날짜 설정 메소드 추가
    }
  },
  created() {
    this.setCurrentData();
  }
  //async created() {  // created 라이프사이클 훅에서 데이터 가져오기
    //const response = await axios.get('http://ip주소/docs#/default/logs_api_v1_logs_get');
    //this.logs = response.data;
  //},
};
</script>
