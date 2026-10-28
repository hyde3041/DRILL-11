# DRILL-11 소년 자동 무적 런

pico2d와 transitions 라이브러리를 사용한 캐릭터 상태 과제입니다.

## 실행

```bash
pip install -r requirements.txt
python main.py
```

## 조작

- `←` / `→`: 좌우 이동
- `a`: Idle 상태에서 AutoRun 시작
- 방향키: AutoRun 취소 후 해당 방향으로 이동

자세한 요구사항은 `PRD.md`를 참고하세요.

## 상태 테스트

```bash
python test_boy.py
```

테스트는 Boy의 초기 상태, AutoRun 반전, Sleep 전이와 기상, 방향키 취소 동작을 검증합니다.
