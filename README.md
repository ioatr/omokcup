# 아이오배 인공(간)지능 오목대회 2016
안녕하세요. 아이오배 인공(간)지능 오목대회는 인공지능과 인간(사람)이 참여하여 경쟁을 벌이는 대회입니다. 상품으로는 1등 5만원, 2등 1만원의 문화상품권을 준비하였습니다. 본 대회는 취미코딩을 장려하는 목적으로 준비한 이벤트입니다. 많은 분들이 함께하면 좋기 때문에, 다과를 드시면서 구경만 하셔도 좋습니다.


## 참여방법
### 코드로 참여
- omok_your_client.(py or cs)을 수정하여, 대회 당일까지 [io_atr@smilegate.com](mailto:io_atr@smilegate.com)으로 실행코드(or 실행파일)를 보내주세요. (또는 USB에 담아오셔도 됩니다.)
- Python, C# 유저를 위해 샘플 코드를 준비 했습니다.
    - omok_your_client.(py or cs)의 choose 함수 부분만 수정하여 작성하는 것을 추천합니다.
    - 편의성을 위하여 오목승패, 통신은 다 구현되어 있습니다.
- 작성 방법에 제한은 없습니다.

### 사람으로 참여
- 몸만 오셔서, 당신의 실력을 보여주세요.


## 규칙
- 15 * 15 오목판의 일반적인 오목룰 적용 예정
- 5판 3선 승제 토너먼트
- 30초 타임아웃 (수동으로 측정합니다)
- 페어플레이를 권장합니다

## 진행 및 상품
### 진행
- 일자: 2016. 11. 25(금)
- 시간: 오후 3시 ~ 4시
- 장소: 엠텍 9층 5번 회의실

### 참가
- 일자: 2016.11.25(금) 오전 11시까지 참가 여부를 알려주세요. 메일 또는 직접 알려주셔도 좋습니다.
    - 메일 주소: [io_atr@smilegate.com](mailto:io_atr@smilegate.com)

### 상품
- 1등: 5만원 문화상품권
- 2등: 1만원 문화상품권
- 소소한 다과


## 코드 관련
### 실행
- [Python2.7](https://www.python.org/downloads/) 이상이 필요합니다.
- 시각화를 위한 pygame module 사용
- 실행 인자는 2개의 파이썬 코드 및 컴파일 된 실행파일(*.exe)를 받을 수 있습니다.
  - 생략시 기본 AI 실행
  - 인자로 manual(or m)을 주시면 수동모드를 활성화하여 마우스로 오목을 둘 수 있습니다.

```bash
# pygame 설치
$ pip install pygame

# 기본 실행
$ python omok_host.py [omok_your_client.py [omok_your_client.py]]

# 자신의 AI vs 기본 AI
$ python omok_host.py omok_your_client.py
$ python omok_host.py omok_your_client.exe

# 수동 모드: 마우스로 오목을 둘 수 있습니다.
$ python omok_host.py m[anual]
```

### 구조
- core/ 오목 핵심 코드 [저장소 링크](https://github.com/ioatr/omok)
- omok_host.py 오목 규칙을 중계해주는 호스트
- omok_client.py 오목 클라이언트
- omok_your_client.py 오목 개인 클라이언트

### 실행예제
![omok_example](https://cloud.githubusercontent.com/assets/760514/20297318/4d463e2e-ab53-11e6-8762-ab7219dc978d.gif)


# Q&A
Q. 사람은 왜 참여하나요?
> 많은 분들이 참가해주셨으면해서... 어쩌다보니 man vs machine...

Q. 윈도우 실행 버전은 없나요? 파이썬 설치하기 싫어요...
> py2exe로 만들다가 실패했습니다. 코드 기부 받습니다.
