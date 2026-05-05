# Civil Cost Manager - 서버 실행 환경

프로젝트: civil-cost-manager
GitHub: https://github.com/DnielPark/civil-cost-manager
최종수정: 2026-05-05

---

## 레포 경로 (맥북 로컬)
~/.openclaw/workspace/civil-cost-manager

## 실행 방법
```bash
cd ~/.openclaw/workspace/civil-cost-manager
python run.py
```

> ⚠️ `python app.py` 직접 실행 금지
> app.py의 `if __name__ == '__main__'` 블록에서 존재하지 않는
> `init_database()`를 호출함 → ImportError 발생

## 서버 정보
- Host: 127.0.0.1
- Port: 8080
- 접속: http://localhost:8080
- Debug: True (개발환경)
- 기술스택: Flask 3.1.1 + SQLite3 + Vanilla JS

## 로컬 관리 스크립트
위치: `~/.openclaw/workspace/skills/`

| 스크립트 | 역할 |
|---|---|
| cost-manager-pull.sh | GitHub → 맥북 최신 pull |
| cost-manager-push.sh "메시지" | 맥북 → GitHub push |
| cost-manager-app-on.sh | 서버 시작 (8080) |
| cost-manager-app-off.sh | 서버 중지 |
| civil-cost-manager-migration.sh [프로젝트명] | DB 마이그레이션 실행 |

## DB 파일 위치
| 파일 | 경로 | 설명 |
|---|---|---|
| unit_price.db | database/unit_price.db | 11개 단가 테이블 |
| quantity.db | database/quantity.db | 수량내역 + 수량이력 |

## 디렉토리 구조
```
civil-cost-manager/
├── app.py              # Flask 앱 생성 (직접 실행 금지)
├── run.py              # 서버 실행 진입점 (이것만 사용)
├── config.py           # 환경설정 (HOST/PORT/DEBUG)
├── database/
│   ├── init_db.py      # DB 초기화 + 마이그레이션
│   ├── schema_unit_price.sql
│   └── schema_quantity.sql
├── routes/
│   ├── main.py         # 페이지 라우트
│   └── api.py          # REST API (⚠️ 구버전 테이블명 사용 중 — 수정 예정)
├── docs/               # 현장별 JSON 데이터 폴터
│   └── 샘플_1공구/      # 샘플 데이터
├── skills/             # 에이전트 스킬 문서
└── templates/          # HTML 템플릿
```
