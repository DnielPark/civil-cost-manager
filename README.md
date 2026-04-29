# Civil Cost Manager

토목 설계 변경 및 공사비 산출을 위한 웹 기반 관리 도구입니다.
단가(재료/노무/경비) 관리, 물량 연동, 엑셀 다운로드(수식 유지)를 목표로 설계된 시스템입니다.

---

# 📌 프로젝트 목적

이 프로젝트의 핵심 목적은 다음과 같습니다.

1. 단가 정보(재/노/경) 관리
2. 설계 변경 시 물량 변경 반영
3. 공사비 자동 계산
4. 엑셀 다운로드 시 **수식 유지**
5. 단가 목록표 및 산출서 자동 생성

---

# 📦 전체 프로젝트 구조

```text
civil-cost-manager/
│
├─ app.py                 # Flask 애플리케이션 생성 및 초기화
├─ run.py                 # 실제 실행 진입 스크립트
├─ config.py              # 환경 설정 파일
├─ civil_cost.db          # SQLite 데이터베이스 파일
│
├─ database/              # DB 연결 및 테이블 정의
│   ├─ __init__.py
│   ├─ models.py          # 데이터 모델 정의 (단가/물량 등)
│   ├─ db_manager.py      # DB 연결 및 세션 관리
│
├─ routes/                # URL 요청 처리 (핵심 로직 진입점)
│   ├─ __init__.py
│   ├─ main_routes.py     # 메인 화면 처리
│   ├─ unit_price_routes.py   # 단가 관련 기능
│   ├─ excel_routes.py        # 엑셀 다운로드 기능
│
├─ templates/             # HTML 화면 (UI)
│   ├─ base.html          # 공통 레이아웃
│   ├─ index.html         # 메인 화면
│   ├─ unit_price.html    # 단가 목록 화면
│   ├─ quantity.html      # 물량 입력 화면
│
├─ static/                # CSS / JavaScript / 이미지
│   ├─ css/
│   ├─ js/
│   ├─ images/
│
├─ utils/                 # 공통 유틸 기능
│   ├─ excel_exporter.py  # 엑셀 생성 로직 (매우 중요)
│   ├─ helpers.py         # 공통 함수
│
├─ tests/                 # 테스트 코드
│   ├─ test_routes.py
│   ├─ test_models.py
│
└─ README.md              # 프로젝트 설명 문서
```

---

# 🧠 핵심 실행 흐름

```text
run.py 실행
        ↓
app.py → Flask 앱 생성
        ↓
routes 등록
        ↓
사용자 요청 처리
        ↓
DB 조회/저장
        ↓
UI 출력 또는 엑셀 다운로드
```

---

# 📁 주요 파일 상세 설명

## app.py  ⭐ (매우 중요)

Flask 애플리케이션을 생성하고 전체 모듈을 연결하는 중심 파일입니다.

주요 역할:

* Flask 인스턴스 생성
* 설정(config) 로딩
* DB 연결 초기화
* routes 등록

검토 포인트:

* Blueprint 등록이 정상적으로 분리되어 있는지 확인
* DB 초기화 코드 위치 확인
* config 로딩 방식 확인

수정 가능 영역:

* 새로운 기능 모듈 추가 시 blueprint 등록
* 전역 설정 추가

---

## run.py  ⭐ (실행 진입점)

프로그램을 실제 실행하는 파일입니다.

예:

```python
python run.py
```

주요 역할:

* Flask 서버 실행
* 개발/운영 모드 설정

검토 포인트:

* debug 모드 설정 여부
* 실행 포트 설정

---

## config.py  ⭐ (환경 설정)

전체 프로젝트 설정값을 관리하는 파일입니다.

포함 가능 항목:

* DATABASE URI
* SECRET KEY
* 파일 저장 경로
* Excel 템플릿 경로

검토 포인트:

* DB 경로가 상대경로인지 확인
* 민감 정보 분리 여부

수정 가능 영역:

* 환경 변수 기반 설정 추가

---

## civil_cost.db  ⭐⭐⭐ (핵심 데이터)

SQLite 데이터베이스 파일입니다.

포함 테이블 예상:

```text
unit_price
quantity
project
cost_history
```

검토 포인트:

* 단가 테이블에 code 컬럼 존재 여부
* 재/노/경 분리 여부
* total 컬럼 존재 여부 (있으면 제거 검토)

---

# 📂 database/ 디렉토리

DB 관련 핵심 로직이 위치합니다.

## models.py  ⭐⭐⭐ (가장 중요)

데이터 테이블 구조 정의 파일입니다.

예:

```python
class UnitPrice(db.Model):
    code = db.Column(db.String)
    name = db.Column(db.String)
    material = db.Column(db.Float)
    labor = db.Column(db.Float)
    expense = db.Column(db.Float)
```

검토 포인트 (매우 중요):

* code 컬럼 존재 여부 (필수)
* material / labor / expense 분리 여부
* total 컬럼 존재 여부 (지양)

수정 가능 영역:

* 단가 버전 관리 컬럼 추가 (year 등)

---

## db_manager.py

DB 연결 및 세션 관리 담당 파일입니다.

주요 역할:

* DB 연결 생성
* 세션 관리
* 트랜잭션 처리

검토 포인트:

* 세션 종료 처리 여부
* 예외 처리 여부

---

# 📂 routes/ 디렉토리  ⭐⭐⭐

웹 요청을 실제 처리하는 핵심 로직 영역입니다.

여기에서 대부분의 기능 흐름이 결정됩니다.

---

## unit_price_routes.py  ⭐⭐⭐ (현재 가장 중요)

단가 입력 및 수정 처리 담당.

현재 작업과 직접 연결된 파일입니다.

예상 기능:

* 단가 목록 조회
* 단가 추가
* 단가 수정
* 단가 삭제

검토 포인트:

* 재/노/경 입력 분리 여부
* 합계 계산이 서버에서 되는지 여부
* UI 합계만 표시하는 구조인지 확인

주의 사항:

합계(total)는 DB 저장 금지 권장.

---

## excel_routes.py  ⭐⭐⭐ (엑셀 핵심)

엑셀 다운로드 기능 담당.

예상 기능:

* 단가 목록표 엑셀 생성
* 수식 포함 엑셀 생성

검토 포인트 (매우 중요):

* SUM 수식이 문자열로 들어가는지 확인

예:

```python
cell.value = "=SUM(B2:D2)"
```

값으로 계산 저장하면 안 됨.

---

# 📂 templates/ 디렉토리  ⭐⭐

HTML UI 파일 위치.

사용자 인터페이스 영역입니다.

---

## unit_price.html  ⭐⭐

단가 입력 및 조회 화면.

검토 포인트:

* 재/노/경 입력 필드 존재 여부
* 합계 표시 로직 위치 (JS인지 확인)

---

## base.html

공통 레이아웃 파일.

포함 가능 항목:

* navbar
* footer
* 공통 스타일

---

# 📂 static/ 디렉토리

CSS 및 JavaScript 파일 위치.

---

## js/  ⭐⭐

UI 계산 로직이 들어갈 가능성이 높은 영역.

예:

```javascript
material + labor + expense
```

검토 포인트:

* 합계 계산 JS 위치 확인
* 이벤트 처리 방식 확인

---

# 📂 utils/ 디렉토리  ⭐⭐⭐

공통 기능 모듈 위치.

---

## excel_exporter.py  ⭐⭐⭐ (가장 중요 파일 중 하나)

엑셀 생성 로직 핵심 파일.

현재 프로젝트의 성공 여부를 좌우할 가능성이 큼.

검토 포인트 (매우 중요):

1. 수식 삽입 방식 확인
2. 열 위치 고정 여부 확인
3. 스타일 적용 여부 확인

예:

```python
ws["E2"] = "=SUM(B2:D2)"
```

---

# 📂 tests/ 디렉토리

테스트 코드 위치.

현재 안정성 확보에 매우 중요합니다.

검토 포인트:

* 단가 입력 테스트 존재 여부
* 엑셀 생성 테스트 존재 여부

---

# 🚨 현재 가장 먼저 점검해야 할 파일 (우선순위)

다음 순서로 점검하는 것을 권장합니다.

1️⃣ database/models.py  ⭐⭐⭐⭐⭐
(단가 테이블 구조 확인)

2️⃣ utils/excel_exporter.py  ⭐⭐⭐⭐⭐
(엑셀 수식 처리 확인)

3️⃣ routes/unit_price_routes.py  ⭐⭐⭐⭐
(단가 입력 처리 확인)

4️⃣ templates/unit_price.html  ⭐⭐⭐
(UI 입력 구조 확인)

---

# 🧩 향후 확장 고려 사항

다음 기능은 추후 매우 중요해질 가능성이 큽니다.

---

## 단가 버전 관리

예:

```text
year = 2025
version = 1
```

---

## 프로젝트 단위 관리

```text
project_id
project_name
```

---

## 변경 이력 관리

```text
modified_date
modified_by
```

---

# 📝 TODO (초기 점검 체크리스트)

다음 항목을 하나씩 점검하세요.

* [ ] 단가 테이블에 code 존재 확인
* [ ] 재/노/경 분리 저장 확인
* [ ] total 컬럼 존재 여부 확인
* [ ] 엑셀 수식 삽입 방식 확인
* [ ] UI 합계 계산 위치 확인
* [ ] DB 연결 안정성 확인

---

# 📌 개발 환경 실행 방법 (예시)

```bash
pip install -r requirements.txt
python run.py
```

브라우저 접속:

```text
http://localhost:5000
```

---

# 📎 참고 사항

이 프로젝트는 다음 원칙을 기준으로 유지 관리하는 것을 권장합니다.

1. 계산 로직은 DB 또는 UI에 저장하지 않는다
2. 합계는 엑셀 수식으로 처리한다
3. 단가는 코드(code) 기반으로 관리한다
4. UI와 계산 로직은 분리한다

---

# ✍️ 유지보수 가이드

새 기능 추가 시 다음 위치를 기준으로 개발합니다.

| 기능        | 위치                      |
| --------- | ----------------------- |
| DB 테이블 추가 | database/models.py      |
| URL 처리 추가 | routes/                 |
| 화면 추가     | templates/              |
| 엑셀 기능 추가  | utils/excel_exporter.py |
| 스타일 변경    | static/css/             |

---

# 🔚 마무리

이 README는 프로젝트 구조 이해 및 유지보수를 쉽게 하기 위한 기본 문서입니다.

향후 기능이 추가되면 반드시 이 문서를 함께 업데이트해야 합니다.
