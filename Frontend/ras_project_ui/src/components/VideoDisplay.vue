<template>
    <div>
      <div id="imageContainer">
        <img id="liveImage" :src="videoSource" alt="Live Image">
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        videoSource: ''
      };
    },
    methods: {
      initWebSocket() {
        const ws = new WebSocket(process.env.VUE_APP_WEBSOCKET_URL);
  
        ws.onmessage = event => {
          this.updateVideoSource(event.data);
        };
  
        ws.onclose = event => {
          console.error("WebSocket closed:", event);
        };
      },
      updateVideoSource(newSource) {
        const blob = new Blob([newSource], { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(blob);
        this.videoSource = imageUrl;
      }
    },
    mounted() {
      this.initWebSocket();
    }
  };
  </script>
  
  <style scoped>

</style>
  