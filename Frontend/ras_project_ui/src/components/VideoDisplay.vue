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
              <div v-for="log in logs" :key="log.seq" id="key_word">
                <p>{{ log.administrator }}</p>
                <p>{{ log.phone }}</p>
                <p>{{ log.logtime }}</p>
                <p>{{ log.logpath }}</p>
                <p>{{ log.smsflag }}</p>
              </div>
            </div>
          </div>
        </td>

      </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import websocket from '../usedata/websocket';
import '../css/main.css';


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
    },
    fetchLogData() {
      axios.get(process.env.VUE_APP_API_URL) // API 주소 수정
      .then(response => {
        console.log(response.data); // 응답 데이터 콘솔에 출력
        this.logs = response.data; // 응답 데이터를 logs 변수에 저장
      })
      .catch(error => console.error(error));
    },
  },
  created() {
    this.setCurrentData();
    this.fetchLogData(); // 컴포넌트가 생성될 때 로그 데이터를 가져옴
  },
};
</script>
