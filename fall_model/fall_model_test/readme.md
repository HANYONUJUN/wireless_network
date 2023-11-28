## model 다운
https://drive.google.com/file/d/1ri-IRMX6sfvutJgWdVmFwiEb8HyovBps/view?usp=drive_link


## image 파일들

테스트할때 필요한 이미지들

## fall_model_test.py

이 코드를 통해서 테스트를 할수 있음

## 실행법

폴더에 coco.names, yolov4.cfg, yolov4.weights(용량이 커서 깃허브에 업로드 못함), fall_detection_model.h5 ( fall_model_create.py를 실행시켜 만들어진 모델)
이 파일들하고 image 파일들 있을시 실행시키면 result 폴더내에 쓰러짐이 감지된 이미지가 업로드됨

### 각각 코드는 경로에따라 조금씩 코드 내용이 바뀜

### yolov4.weights를 다운하고 싶으면 

  colab 기준
  
    Darknet 설치
    https://drive.google.com/file/d/19LPcnMPCcdgyFMZlSIKRbDMSjOHji2cy/view?usp=drive_link

    or
    
    git clone https://github.com/AlexeyAB/darknet.git
    %cd darknet
    make
    
    COCO 데이터셋 다운로드
    wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
    !wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
    !wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.data
    !wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.names
    
    COCO 데이터 경로 설정
    mkdir data
    echo classes=80 > data/coco.names
    cp cfg/coco.names data/coco.names
    
    사람 클래스 설정
    echo -e 'person' > data/obj.names
    
    데이터 다운로드 (train, val, test)
    wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/coco.names
    !wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
    
    YOLO 모델 학습
    ./darknet detector train cfg/coco.data cfg/yolov4.cfg yolov4.conv.137 -dont_show
    
    학습된 모델로 이미지 테스트
    ./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights -ext_output input.jpg

  리눅스 기준
  
      sudo apt-get update
      sudo apt-get install build-essential

      COCO 데이터셋 다운로드
      curl -O https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
      curl -O https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
      curl -O https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.data
      curl -O https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.names
      
      데이터 다운로드 (train, val, test)
      curl -O https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/coco.names
      curl -O https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
      
      필요한 라이브러리 설치 (예: GPU 지원을 위한 CUDA 및 cuDNN)
      필요에 따라 다른 라이브러리 및 헤더 파일 설치 필요
      sudo apt-get install libopencv-dev
      sudo apt-get install libopencv-highgui-dev
      sudo apt-get install libopencv-imgcodecs-dev
      
      Makefile 수정 (GPU 사용 시)
      GPU=1, CUDNN=1 등을 설정하여 GPU 및 cuDNN을 사용하도록 수정

다운시 나오는 파일 안에 coco.names, yolov4.cfg, yolov4.weights가 있음

## 다음 작업 예정

다른 동작시 그걸 감지하는 모델 가능하면 구현

