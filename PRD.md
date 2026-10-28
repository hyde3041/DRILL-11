# DRILL-11 소년 자동 무적 런(PRD)

## 개요
pico2d와 transitions 라이브러리를 사용하여 캐릭터 상태를 구현한다.

## 실행 방법
```bash
python main.py
```

## 기능 요구사항

1. 캐릭터는 최초에 Idle 상태로 시작한다.
2. Idle 상태에서 좌우 방향키를 누르면 Run 상태로 이동한다.
3. Idle 상태에서 a 키를 누르면 AutoRun 상태로 이동한다.
4. AutoRun 상태의 Boy는 크기가 커지고 빠르게 좌우로 이동하며, 화면 양쪽 끝에서 방향을 전환한다.
5. AutoRun 상태에서 방향키를 누르면 AutoRun을 취소하고 해당 방향의 Run 상태로 이동한다.
6. AutoRun 상태가 5초 이상 유지되면 Idle 상태로 복귀한다.
7. Idle 상태에서 키 입력 없이 5초가 지나면 Sleep 상태로 전환한다.
8. Sleep 상태는 아래 방향에 관계없이 누워 있는 모습으로 표시한다.

## 상태 전이
- IDLE → RUN_LEFT / RUN_RIGHT: 좌우 방향키 입력
- IDLE → AUTO_RUN: a 키 입력
- AUTO_RUN → RUN_LEFT / RUN_RIGHT: 방향키 입력
- AUTO_RUN → IDLE: 5초 경과 또는 상태 종료
- RUN_LEFT / RUN_RIGHT → IDLE: 방향키 해제
- IDLE → SLEEP: 키 입력 없이 5초 경과
- SLEEP → IDLE / RUN: 방향키 입력

## 제출 구성
- main.py
- boy.py
- grass.py
- animation_sheet.png
- grass.png
- PRD.md
- requirements.txt
