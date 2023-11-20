<template>
 
    <div id="imageContainer">
      <img id="liveImage" :src="videoSource" :style="{ transform: `scale(${zoomLevel})` }" alt="Live Image">
    </div>

    <div class="pm_btn">
    <button @click="zoomIn">확대</button>
    <button @click="zoomOut">축소</button>
  </div>
</template>

<script>
import websocket from '../usedata/websocket';
import '../css/main.css';

export default {
  data() {
    return {
      videoSource: '',
      zoomLevel: 1.0,
    };
  },
  methods: {
    zoomIn() {
      if (this.zoomLevel < 2.0) {
        this.zoomLevel += 0.1;
      }
    },
    zoomOut() {
      if (this.zoomLevel > 0.5) {
        this.zoomLevel -= 0.1;
      }
    },
  },
  mixins: [websocket],
  mounted() {
    this.initWebSocket();
  },
};
</script>


  