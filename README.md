# Civil Cost Manager

토목 공사비 관리를 위한 웹 기반 단가 관리 시스템입니다.
SQLite 데이터베이스를 사용하며, 11가지 단가 유형을 지원합니다.

---

## 🤖 에이전트 스킬 문서

클로드 및 미르가 세션 시작 시 참조하는 문서 목록.
상세 내용은 각 스킬 파일 참조.

| 스킬 파일 | 내용 |
|---|---|
| [skills/civil_cost_manager_server_env.md](skills/civil_cost_manager_server_env.md) | 서버 실행환경, 포트, 스크립트, DB 경로 |
| [skills/civil_cost_manager_db_schema.md](skills/civil_cost_manager_db_schema.md) | DB 스키마 전체, 코드 체계, API 매핑 |
| [skills/civil_cost_manager_workflow.md](skills/civil_cost_manager_workflow.md) | 3자 역할 분담, 작업 흐름, 진행 상태 |

---

## 📌 프로젝트 개요

**개발 단계:** 환경 셋팅 완료 / v1.0 개발 진행 중  
**사용 기술:** Flask, SQLite, vanilla JavaScript  
**실행 포트:** 8080

---

## 📦 실제 프로젝트 구조

```
civil-cost-manager/
│
├─ app.py                 # Flask 앱 생성 및 블루프린트 등록
├─ run.py                 # 서버 실행 진입점
├─ config.py              # 환경 설정 (개발/운영)
├─ civil_cost.db          # SQLite 데이터베이스
├─ requirements.txt       # Python 의존성 패키지
│
├─ database/              # DB 관련
│   └─ init_db.py         # 테이블 생성 및 샘플 데이터 삽입
│
├─ routes/                # URL 요청 처리
│   ├─ main.py            # 페이지 렌더링 라우트
│   └─ api.py             # JSON API 라우트
│
├─ templates/             # HTML 화면
│   ├─ index.html         # 메인 페이지 (프로젝트 선택)
│   ├─ unit_prices_dashboard.html  # 단가 유형 선택 대시보드
│   ├─ unit_price_list.html        # 단가 목록 테이블
│   ├─ projects.html               # 프로젝트 목록 (준비중)
│   ├─ project_detail.html         # 프로젝트 상세 (준비중)
│   └─ error.html                  # 에러 페이지
│
├─ static/                # 정적 파일
│   ├─ css/style.css      # 공통 스타일
│   └─ js/app.js          # 공통 JavaScript
│
├─ utils/                 # 유틸리티
│   └─ excel_parser.py    # 엑셀 업로드 파싱
│
├─ tests/                 # 테스트 파일
│   ├─ sample_standard.xlsx
│   ├─ bad_header.xlsx
│   └─ create_sample.py
│
└─ README.md              # 이 파일
```

---

## 🗄️ 데이터베이스 구조

### 테이블 목록

| 테이블명 | 설명 | 특이사항 |
|---------|------|---------|
| `projects` | 프로젝트 정보 | id, name, location |
| `unit_cost_final` | 내역단가 목록표 (최종) | cost_source, source_id 컬럼 추가 |
| `unit_cost_composite` | 일위대가 목록표 | composition_detail 컬럼 추가 |
| `unit_cost_standard` | 품셈단가 목록표 | 기본 구조 |
| `unit_cost_market` | 표준시장단가 목록표 | 기본 구조 |
| `unit_cost_quote` | 견적단가 목록표 | 기본 구조 |
| `unit_cost_price_info` | 물가정보지 목록표 | publisher, issue_date 컬럼 추가 |
| `unit_cost_field_report` | 실정보고 단가 목록표 | 기본 구조 |

### 공통 컬럼 구조 (모든 단가 테이블)

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
project_id INTEGER NOT NULL          -- 프로젝트 참조
work_name TEXT NOT NULL              -- 공종명
spec TEXT NOT NULL                   -- 규격
unit TEXT NOT NULL                   -- 단위
unit_quantity REAL DEFAULT 1.0       -- 단위수량
material_cost REAL DEFAULT 0         -- 재료비
labor_cost REAL DEFAULT 0            -- 노묘비
expense_cost REAL DEFAULT 0          -- 경비
note TEXT                            -- 비고
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### ⚠️ 현재 구조 특징

- **재/노/경 분리 저장:** ✅ 구현됨 (material_cost, labor_cost, expense_cost 별도 컬럼)
- **total 컬럼 없음:** ✅ DB에 합계 저장 안 함 (프론트에서 JavaScript로 계산)
- **code 컬럼:** ✅ 구현됨 — 형식: `[파일명]-NNNNN` (예: `품셈단가_data-00001`)
- **합계 계산:** UI(JavaScript)에서 처리

---

## 🚀 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행 (방법 1: 직접 실행)
python run.py

# 3. 서버 실행 (방법 2: 개발 스크립트)
# ./cost-manager-dev.sh  # 로컬 개발용 스크립트 (준비중)

# 4. 브라우저 접속
http://localhost:8080
```

---

## 🌐 주요 화면 흐름

```
[메인 페이지]
    ↓ 프로젝트 선택
[단가명세표 대시보드]
    ↓ 단가 유형 선택
[단가 목록 테이블]
    ↓ 검색 / 엑셀 업로드 / 엑셀 다운로드
```

---

## 🔌 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/api/projects` | 프로젝트 목록 조회 |
| POST | `/api/projects` | 프로젝트 생성 |
| GET | `/api/unit-prices/<project_id>/<type>` | 단가 목록 조회 |
| GET | `/api/unit-prices/<project_id>` | 모든 단가 조회 |
| POST | `/api/unit-prices/<project_id>/<type>` | 단가 추가 |

### 단가 유형 코드

| 코드 | 설명 |
|------|------|
| `final` | 내역단가 목록표 |
| `composite` | 일위대가 목록표 |
| `standard` | 품셈단가 목록표 |
| `market` | 표준시장단가 목록표 |
| `quote` | 견적단가 목록표 |
| `price_info` | 물가정보지 목록표 |
| `field_report` | 실정보고 단가 목록표 |

---

## 📊 현재 기능 상태

> 상세 진행 상태는 [skills/civil_cost_manager_workflow.md](skills/civil_cost_manager_workflow.md) 참조

### ✅ 구현 완료
- [x] Flask 기본 구조 + SQLite 연동
- [x] 11개 단가 테이블 스키마 설계 및 확정
- [x] 단가 코드 체계 확정 (파일명-NNNNN 형식)
- [x] 샘플 JSON 데이터 (docs/샘플_1공구/ 12개 파일)
- [x] JSON → DB 마이그레이션 스크립트 (UPSERT)
- [x] 단가명세표 대시보드 UI
- [x] 단가 목록 조회 + 검색
- [x] 인셀 더블클릭 수정 기능
- [x] 엑셀 파싱 유틸리티 (excel_parser.py)
- [x] 에이전트 스킬 문서 3개 (skills/ 폴터)

### 🔜 v1.0 예정
- [ ] routes/api.py 신규 테이블명 연동 ← 현재 작업
- [ ] 메인 페이지 UI 개편 (docs/ 폴터 스캔 + 마이그레이션 버튼)
- [ ] 마이그레이션 실시간 로그 스트리밍

### ⏳ v2.0 예정
- [ ] 수량DB 마이그레이션 UI
- [ ] 수량내역서 관리 페이지
- [ ] 실정보고 패키지 출력
- [ ] 내역서 자동 생성
- [ ] projects 테이블 메타데이터 확장

---

## 📝 개발 노트

### 완료된 주요 작업 이력
- 1주차: Flask 기본 구조, 7개 테이블 초기 설계
- 2주차: DB 스키마 전면 재설계 (11개 테이블, code 컬럼, UPSERT)
- 환경 셋팅: 에이전트 스킬 문서, README/workflow 현행화, 오타 수정

### 향후 확장 고려사항
1. **엑셀 다운로드:** `=SUM()` 수식 포함 엑셀 생성
2. **물량 연동:** 단가 × 물량 = 금액 계산
3. **projects 테이블 확장:** 공사종류/발주처/계약금액/착공일/준공예정일

### ⚠️ 알려진 이슈
- routes/api.py 가 구버전 테이블명(unit_cost_*) 사용 중 → v1.0에서 수정 예정
- 현재 서버 실행 시 단가 데이터 화면에 표시 안 됨 (위 이슈 원인)

---

## 📐 단가 체계 구조

### 정상 흐름 (설계 단계)

```
물가정보지 → 품셈/시장/견적 → 일위대가 → 내역단가 (최종)
```

### 변경 흐름 (설계 변경 시)

```
... → 실정보고 단가 (별도 관리)
```

### 출처 추적 메커니즘

`unit_cost_final` 테이블의 `cost_source` + `source_id` 컬럼으로 단가 출처 추적:

| cost_source | 설명 | 예시 |
|-------------|------|------|
| `standard` | 품셈단가 참조 | 품셈단가 ID |
| `composite` | 일위대가 참조 | 일위대가 ID |
| `market` | 표준시장단가 참조 | 시장단가 ID |
| `quote` | 견적단가 참조 | 견적단가 ID |
| `field_report` | 실정보고 참조 | 실정보고 ID |
| `price_info` | 물가정보지 참조 | 물가정보지 ID |

---

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| 백엔드 | Flask 3.1.1 |
| 데이터베이스 | SQLite3 |
| 엑셀 처리 | openpyxl 3.1.5, pandas 2.2.3 |
| 프론트엔드 | vanilla JavaScript |
| 스타일 | CSS3 |

---

## 📄 라이선스

Civil Cost Manager © 2026
