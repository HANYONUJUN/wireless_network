<template>
  <div id="imageContainer">
    <table>
      <tr>
        <td>
          <div class="rectangle">
            <img id="liveImage" :src="videoSource" alt="Live Image">
          </div>
        </td>
        <td>
          <div class="rectangle" id="serve_img">
            <img :src="latestImage" alt="Latest Image" id="serve_img2">
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
            <div class="log_date_text"  >
              <div v-for="(logs, date) in groupedLogs" :key="date" id="date_log">
              <h2>-- {{ date }} --</h2>
              <table border="1" style="margin: auto">
                  <thead>
                    <tr>
                      <th>관리자ID</th>
                      <th>전화번호</th>
                      <th>로그발생시간</th>
                      <th>로그경로</th>
                      <th>SMS수신여부</th>
                    </tr>

                  </thead>
                  <tbody  v-for="log in logs" :key="log.seq" class="key_word">
                    <tr>
                      <td>{{ log.administrator }}</td>
                      <td>{{ log.phone }}</td>
                      <td>{{ formatDateTime(log.logtime) }}</td>
                      <td>{{ log.logpath }}</td>
                      <td>{{ log.smsflag }}</td>
                    </tr>
                  </tbody>
              </table>
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
import { format } from 'date-fns';


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
      latestImage: '',
    };
  },

  methods: { 
    saveUserInfo(){
      if(!this.name || !this.phone || !this.date) {
        alert("입력되지 않은 정보가 있습니다");
        return;
      }

      this.userInfo ={ name: this.name, phone: this.phone, date:this.date};
      alert('사용자 정보 등록 완료');
    },

    formatDateTime(dateTime) {
      // 'yyyy-MM-dd HH:mm:ss' 형식으로 포맷
      return format(new Date(dateTime), 'yyyy-MM-dd HH:mm:ss');
     },

     startStreaming() {
      if (!this.userInfo) {
        alert('사용자 정보가 등록되지 않았습니다.');
        return;
      }else {
        if (this.userInfo != null) {
          this.isStreaming = true;
          this.ws = websocket.initWebSocket();
        }
      }
        this.ws.onopen = () => {
        if (this.userInfo) {
          this.ws.send(JSON.stringify(this.userInfo));
        }
      };

      this.ws.onmessage = event => {
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(blob);
        this.videoSource = imageUrl;
        this.latestImage = imageUrl;
      };

      this.ws.onclose = event => {
        console.error("WebSocket closed:", event);
      };

      this.ws.onerror = error => {
        console.error("WebSocket error:", error);
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

