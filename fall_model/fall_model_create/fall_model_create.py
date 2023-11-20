import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.callbacks import ModelCheckpoint
from keras.models import load_model


# 데이터 디렉토리 경로
fallen_data_dir = "dataset1/fall"
not_fallen_data_dir = "dataset1/not_fall"

# 데이터 로드 및 전처리
def load_and_preprocess_data(data_dir, label):
    images = []
    labels = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".png"):
            img_path = os.path.join(data_dir, filename)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (224, 224))
            img = img / 255.0  # 정규화
            images.append(img)
            labels.append(label)  # 클래스 레이블 추가

    return np.array(images), np.array(labels)

# "쓰러짐" 데이터 로드
fallen_images, fallen_labels = load_and_preprocess_data(fallen_data_dir, 1)

# "쓰러지지 않음" 데이터 로드
not_fallen_images, not_fallen_labels = load_and_preprocess_data(not_fallen_data_dir, 0)

# 모든 데이터 합치기
images = np.concatenate((fallen_images, not_fallen_images), axis=0)
labels = np.concatenate((fallen_labels, not_fallen_labels), axis=0)

# 레이블을 이진 분류로 변환
labels = to_categorical(labels, num_classes=2)

# 훈련 및 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# 모델 구축
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(2, activation='softmax'))  # 이진 분류 문제이므로 출력 레이어는 2개

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 모델 훈련
checkpoint = ModelCheckpoint("best_model.h5", monitor='val_accuracy', save_best_only=True, mode='max')
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, callbacks=[checkpoint])

# 모델 저장
model.save("fall_detection_model.h5")

