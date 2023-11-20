<template>
  <div>
    <img v-if="imageSrc" :src="imageSrc" alt="Received image" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      imageSrc: ""
    };
  },
  mounted() {
    this.socket = new WebSocket("ws://ip주소:8000/ws_a");
    this.socket.onmessage = this.handleMessage;
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
  methods: {
    handleMessage(event) {
      let data = JSON.parse(event.data)
      if (data.image) {
        this.imageSrc = 'data:image/jpeg;base64,' + data.image;
      }
    }
  }
};
</script>
