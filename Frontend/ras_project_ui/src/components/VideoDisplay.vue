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
          <button id="info_btn" @click="saveUserInfo">등록</button>
        </td>

        <td>
          <div class="rectangle2" id="log_it">
            <div class="log_date_text">
              <div v-for="(logs, date) in groupedLogs" :key="date" id="date_log">
              <h2>-- {{ date }} --</h2>
              <div v-for="log in logs" :key="log.seq" id="key_word">
                <span>{{ log.administrator }} | </span>
                <span>{{ log.phone }} | </span>
                <span>{{ log.logtime }} | </span>
                <span>{{ log.logpath }} | </span>
                <span>{{ log.smsflag }}</span>
              </div>
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
      date: "",
      logs: [],  // logs 배열 추가
      userInfo: null,
      wsUserInfo: null,
    };
  },
  methods: {
    saveUserInfo(){
      if(!this.name || !this.phone || !this.date) {
        alert("입력되지 않은 정보가 있습니다");
        return;
      }

      this.userInfo ={ name: this.name, phone: this.phone, date:this.date};
    },

    startStreaming() {
      if (!this.userInfo) {
        alert('사용자 정보가 등록되지 않았습니다.');
        return;
      }else{
        if(this.userInfo != null) {
          alert('사용자 정보 등록 완료');
          this.isStreaming = true;
          this.ws = websocket.initWebSocket();
          this.wsUserInfo = new WebSocket("ws://localhost:9998");
        }
      }

      this.ws.onopen = () => {
        if (this.userInfo) {
          this.ws.send(JSON.stringify(this.userInfo));
        }
      };

      this.wsUserInfo.onopen = () => {
        if (this.userInfo) {
          this.wsUserInfo.send(JSON.stringify(this.userInfo)); // 사용자 정보 전송
        } 
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

  computed: {
    groupedLogs() {
      return this.logs.reduce((groups, log) =>{
        const date = log.logtime.split('T')[0];
        if(!groups[date]) {
          groups[date] = []
        }
        groups[date].push(log);
        return groups;
      }, {});
    }
  },

  created() {
    this.setCurrentData();
    this.fetchLogData(); // 컴포넌트가 생성될 때 로그 데이터를 가져옴
  },
};
</script>

