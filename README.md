# Civil Cost Manager

토목 공사비 관리를 위한 웹 기반 단가 관리 시스템입니다.
SQLite 데이터베이스를 사용하며, 7가지 단가 유형을 지원합니다.

---

## 📌 프로젝트 개요

**개발 단계:** 1주차 (기본 구조 및 단가 조회 기능 구현)  
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

- **재/노/경 분리 저장:** ✅ 구현됨
- **total 컬럼 없음:** ✅ DB에 합계 저장 안 함
- **code 컬럼 없음:** ❌ 미구현 (추가 권장)
- **합계 계산:** UI(JavaScript)에서 처리

---

## 🚀 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행
python run.py

# 3. 브라우저 접속
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

### ✅ 구현된 기능

- [x] 프로젝트 생성/조회
- [x] 7가지 단가 유형별 조회
- [x] 단가 목록 테이블 표시 (재/노/경 + 합계)
- [x] 단가 검색 (공종명/규격)
- [x] 엑셀 파일 파싱 (업로드 준비)
- [x] 샘플 데이터 자동 생성

### 🚧 미구현 기능 (예정)

- [ ] 엑셀 업로드 (UI 버튼만 존재)
- [ ] 엑셀 다운로드 (UI 버튼만 존재)
- [ ] 단가 수정/삭제
- [ ] 물량 입력 및 공사비 계산
- [ ] 단가 코드(code) 컬럼 관리
- [ ] 단가 버전 관리

---

## 📝 개발 노트

### 1주차 완료 사항

- Flask 기본 구조 설정
- SQLite 데이터베이스 및 8개 테이블 생성
- 프로젝트/단가 API 구현
- 단가 대시보드 및 목록 화면 구현
- 엑셀 파싱 유틸리티 작성

### 향후 확장 고려사항

1. **code 컬럼 추가:** 단가 고유 코드 관리 (CONC001 등)
2. **엑셀 다운로드:** `=SUM()` 수식 포함 엑셀 생성
3. **단가 버전 관리:** 연도별 단가 이력 관리
4. **물량 연동:** 단가 × 물량 = 금액 계산

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
