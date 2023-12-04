import json
import cv2
import asyncio
import websockets
import base64

async def send_video():
    # FastAPI 웹 소켓통신
    uri = "ws://211.105.65.25:23241/ws_a"

    async with websockets.connect(uri) as websocket:
        
        # 이때 타 프로그램에서 카메라를 사용중인경우 에러가 발생하니, 주의할 것
        cap = cv2.VideoCapture(1)
        
        # 초당 20프레임 제한 걸어서 통신
        # 없을경우 이미지 로드가 이상해지는 상태를 발견함
        cap.set(cv2.CAP_PROP_FPS, 20)
        while cap.isOpened():
            ret, frame = cap.read()

            # 이미지를 base64로 인코딩
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = base64.b64encode(img_encoded.tobytes())
            img_str = img_bytes.decode('utf-8')

            data_to_send = {"image": img_str}
            await websocket.send(json.dumps(data_to_send))
        cap.release()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_video())
