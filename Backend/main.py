# 백엔드 서버 코드 예시 (backend_server.py)
import base64
import json
import cv2
import numpy as np
import pymysql
import os

from starlette.middleware.cors import CORSMiddleware
from twilio.rest import Client
from fastapi import FastAPI, WebSocket
from sqlalchemy.orm import sessionmaker
from starlette.websockets import WebSocketDisconnect
from typing import List
from datetime import datetime
from AI.fall_model_test import process_image
from model.schema import Logs
from model.model import ImageData, Log
from dotenv import load_dotenv
from sqlalchemy import create_engine

app = FastAPI()
load_dotenv()
database_url = os.getenv('DATABASE_URL')
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
myphone = os.getenv('myphone')

engine = create_engine(
    database_url
)
session = sessionmaker(bind=engine)

websocket_b_connections: List[WebSocket] = []
websocket_c_dict = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.websocket("/ws_a")
async def websocket_imagedata(websocket: WebSocket):
    global ai_data
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
                ai_img, flag = process_image(img, "AI/fall_detection_model.h5", f"AI/result/{current_time}.jpg")

                print(websocket_c_dict.get(websocket, {}))

                if ai_img is not None:
                    ai_data = base64.b64decode(ai_img)
                    await pitofront(ai_data)
                else:
                    await pitofront(img_data)
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
            # 프론트에서 관리자 정보 수신
            data = await websocket.receive_text()
            print(f"Received from B: {data}")
            data_dict = json.loads(data)
            websocket_c_dict[websocket] = json.loads(data)
    except WebSocketDisconnect:
        websocket_b_connections.remove(websocket)

# 웹소켓초기화
@app.get("/reset")
async def socket_reset():
    global websocket_b_connections
    websocket_b_connections = []
    print("All WebSocket connections are reset.")


@app.get("/api/v1/logs", response_model=List[Logs])
def logs():
    """
    seq: 로그번호\n
    administrator: 해당시간 관리자\n
    phone: 관리자 전화번호\n
    logtime: 감지경보 시간\n
    logpath: 감지당시 이미지 파일경로\n
    smsflag: sms수신여부\n
    로그 출력
    """
    db = session()
    val = db.query(Log).order_by(Log.logtime).all()
    return val

@app.post("/app/v1/sms")
def smsrequest(phone: str = None):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=f"+82{phone}",
        from_=f"{myphone}",
        body="[사고감지] 현재 라즈베리파이 A카메라에 사고가 감지 되었습니다.")
    return message.sid


# 두 소켓간 통신용
async def pitofront(image_path: bytes):
    try:
        for connection in websocket_b_connections:
            # 이미지 데이터와 함께 데이터를 전송
            await connection.send_bytes(image_path)
    except WebSocketDisconnect as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        websocket_b_connections.clear()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23241, reload=False)
