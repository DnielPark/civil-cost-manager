# ✅ 1주차+ 작업 완료 보고 (2026-04-28)

## 📋 완료 항목

### 1. GitHub 공개 레포
- **URL**: https://github.com/DnielPark/civil-cost-manager
- **기술**: Flask + SQLite3 + HTML/CSS/JS + openpyxl + pandas

### 2. 프로젝트 구조
```
civil-cost-manager/
├── app.py                    # Flask 메인 (127.0.0.1:8080)
├── config.py                 # 설정 분리 (HOST/PORT/DEBUG)
├── run.py                    # debug=False 실행
├── requirements.txt
├── database/
│   ├── __init__.py            # init_db.py import
│   └── init_db.py             # 7종 단가 테이블 생성
├── routes/
│   ├── __init__.py
│   ├── main.py                # 페이지 라우트 (Blueprint)
│   └── api.py                 # REST API + POST 추가 엔드포인트
├── utils/
│   ├── __init__.py
│   └── excel_parser.py        # 엑셀 파싱 유틸리티
├── static/css/style.css
├── templates/
│   ├── index.html              # 메인 (프로젝트 선택 + 4개 메뉴)
│   ├── unit_prices_dashboard.html  # 단가명세표 대시보드 (6개 카드)
│   ├── unit_price_list.html    # 공통 목록표 템플릿 (동적 칼럼)
│   └── error.html
└── tests/
    ├── sample_standard.xlsx    # 테스트용 샘플 엑셀
    └── create_sample.py
```

### 3. DB 스키마 (7개 테이블)

| 테이블 | 설명 | 샘플 |
|--------|------|------|
| `projects` | 프로젝트 | OO고속도로 1공구 |
| `unit_cost_final` | 📊 내역단가 (최종 설계) | 5건 |
| `unit_cost_composite` | 📋 일위대가 (복합) | 3건 |
| `unit_cost_standard` | 📐 품셈단가 | 5건 |
| `unit_cost_market` | 🏪 표준시장단가 | 2건 |
| `unit_cost_quote` | 📄 견적단가 | 1건 |
| `unit_cost_price_info` | 💰 물가정보지 | 2건 |
| `unit_cost_field_report` | 🔧 실정보고 단가 | 3건 |

**핵심 구조**: 내역단가 → cost_source + source_id로 출처 추적

### 4. 주요 기능
- **메인 페이지**: 프로젝트 선택 드롭다운 + 4개 메뉴 (단가명세표만 활성화, 나머진 준비중)
- **단가명세표 대시보드**: 내역단가(최상위 강조) + 5개 기초단가 카드 (건수 표시)
- **개별 목록표**: 유형별 동적 칼럼 (내역단가=출처, 일위대가=구성내역, 물가정보지=발행처/발행일)
- **검색**: 공종명/규격 실시간 필터링
- **POST API**: 단가 추가 엔드포인트 (중복 시 409)
- **엑셀 파싱**: `utils/excel_parser.py` — 헤더 매칭 + 행별 검증

### 5. 로컬 스크립트
```bash
cd ~/.openclaw/workspace/skills
./cost-manager-pull.sh         # GitHub → 맥북
./cost-manager-push.sh "메시지" # 맥북 → GitHub
./cost-manager-app-on.sh       # 서버 시작 (8080)
./cost-manager-app-off.sh      # 서버 중지
```

### 6. 단가 구조 규칙
- 정상: 물가정보지 → 품셈/시장/견적 → 일위대가 → 내역단가
- 비정상(변경/이슈): → 실정보고 단가 (별도 관리)
- 상세: `skills/unit-cost-structure.md` 참조

## 📌 커밋 기록 (전체)

| 커밋 ID | 내용 |
|---------|------|
| `eb1bb24` | Flask 프로젝트 초기 세팅 |
| `72eeb42` | 메인 대문 페이지 |
| `091df6d` | config.py 설정 분리 |
| `25a1362` | app.py config 적용 |
| `82bd970` | 단가명세서 샘플 및 화면 |
| `e39d65d` | 스키마 개선 (합계 제거, 단위수량/산출근거) |
| `20aa2f2` | 단가 체계 4개 테이블 |
| `9ce13f4` | 대시보드 + 개별 목록표 분리 |
| `8d32d5a` | 6개 테이블 구조 확장 |
| `63e7ecb` | 실정보고 단가 추가 |
| `11c8b16` | __init__.py 정리 + run.py 포트 통일 |
| `d71b845` | 미구현 메뉴 disabled |
| `8fa8798` | API 에러 핸들링 + POST 엔드포인트 |
| `7ce3146` | 엑셀 파싱 유틸리티 |

## ⚠️ 이슈
- 포트 5000: AirPlay 리시버와 충돌 → **8080**으로 변경

## ▶️ 다음 단계 예정
1. 엑셀 업로드 → API 연결 (5단계)
2. 프론트 업로드 UI (6단계)
3. 내역서 관리 페이지
4. 내역단가 출처 자동 연결
