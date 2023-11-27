# 백엔드 서버 코드 예시 (backend_server.py)
import base64
import json
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from typing import List
from datetime import datetime
from Backend.AI.fall_model_test import process_image

from model.model import ImageData

app = FastAPI()
websocket_b_connections: List[WebSocket] = []

@app.websocket("/ws_a")
async def websocket_imagedata(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)

            image_data = ImageData(**data_json)
            if "image" in data_json:
                # 이미지 데이터를 Base64 디코딩
                img_data = base64.b64decode(image_data.image)

                # Bytes를 OpenCV 이미지로 변환
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

                ai_img = process_image(img, "AI/fall_detection_model.h5", f"AI/result/{current_time}.jpg")
                # 이미지 저장

                img_data = None
                if ai_img is not None:
                    img_data = base64.b64encode(ai_img)
                # 임시 이미지 저장 a.jpg
                #
                # cv2.imwrite(image_path, img)

                # 이미지 저장시 사용
                # result = {"image_path": image_path}
                if img_data is not None:
                    await pitofront(f"../Backend/AI/result/{current_time}.jpg")
    except WebSocketDisconnect:
        websocket_b_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket connection closed: {e}")


# 프론트에서 받을 이미지 통신용 소켓
@app.websocket("/ws_b")
async def websocket_htmlimagedata(websocket: WebSocket):
    await websocket.accept()
    websocket_b_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from B: {data}")
    except WebSocketDisconnect:
        websocket_b_connections.remove(websocket)

# 웹소켓초기화
@app.get("/reset")
async def socket_reset():
    global websocket_b_connections
    websocket_b_connections = []
    print("All WebSocket connections are reset.")


# 두 소켓간 통신용
async def pitofront(image_path: str):
    try:
        for connection in websocket_b_connections:
            # 이미지 데이터와 함께 데이터를 전송
            await connection.send_text(image_path)
    except WebSocketDisconnect as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        websocket_b_connections.clear()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=23241)
