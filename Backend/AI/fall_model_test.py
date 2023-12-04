import base64
import os

from dotenv import load_dotenv

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import cv2
import numpy as np
from sklearn.model_selection import train_test_split


from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

load_dotenv()
yolov4_weightes = os.getenv('yolov4_weightes')
yolov4_cfg = os.getenv('yolov4_cfg')

def process_image(img, model_path, output_path):
    # YOLO 모델 로드
    net = cv2.dnn.readNet(yolov4_weightes, yolov4_cfg)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    classes = []

    with open("AI/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getUnconnectedOutLayersNames()
    # 이미지 읽기
    #img = cv2.imread(img_path)

    # 이미지가 정상적으로 읽어졌는지 확인
    if img is None:
        print("에러: 이미지를 읽을 수 없습니다.")
    else:
        # YOLO 입력으로 변환
        height, width = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 0.00392, (224, 224), (0, 0, 0), True, crop=False)
        net.setInput(blob)

        # YOLO 추론 수행
        outs = net.forward(layer_names)

        # 검출된 객체 정보 추출
        person_detected = False
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:  # 클래스 ID가 0은 '사람' 클래스일 때
                    person_detected = True  # 사람이 검출되었음을 표시
                    center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                    w, h = int(detection[2] * width), int(detection[3] * height)
                    x, y = int(center_x - w / 2), int(center_y - h / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # 사람을 검출하지 못한 경우 "not_detect" 출력
        if not person_detected:
            cv2.putText(img, "not_detect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            # 경계 상자 그리기
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]

                    # 추출된 객체의 부분 이미지
                    detected_object = img[y:y + h, x:x + w]
                    if detected_object is not None and not detected_object.size == 0:
                        # CNN 모델을 사용하여 쓰러짐 여부 분류
                        detected_object = cv2.resize(detected_object, (224, 224))  # CNN 모델의 입력 크기에 맞게 조정
                        detected_object = detected_object / 255.0  # 정규화
                        detected_object = np.expand_dims(detected_object, axis=0)  # 배치 차원 추가

                        # CNN 모델을 사용하여 예측
                        loaded_model = load_model(model_path)
                        prediction = loaded_model.predict(detected_object)
                        class_index = np.argmax(prediction)

                        # 결과에 따라 출력
                        if class_index == 1:  # 클래스 1은 '쓰러짐' 클래스일 때
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(img, "fall", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            _, img_encoded = cv2.imencode('.jpg', img)
                            img_bytes = base64.b64encode(img_encoded.tobytes())
                            img_str = img_bytes.decode('utf-8')
                            cv2.imwrite(output_path, img)
                            return img_str
                        else:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(img, "not_fall", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            return None

            # 결과 이미지 출력
            cv2.imwrite(output_path, img)
            #cv2.imshow("Result", img)
            #cv2.waitKey(0)
            cv2.destroyAllWindows()
        return None

# 이미지 처리 함수 호출
