# Civil Cost Manager - DB 스키마

프로젝트: civil-cost-manager
GitHub: https://github.com/DnielPark/civil-cost-manager
최종수정: 2026-05-05

---

## DB 구성
- unit_price.db: 단가 관련 11개 테이블 + projects
- quantity.db: 수량내역 + 수량이력 (차수 관리)

---

## 공통 컬럼 구조 (모든 단가 테이블)
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
project_id INTEGER NOT NULL        -- 프로젝트 분리 키
code TEXT NOT NULL                  -- 단가 코드 (불변)
품명 TEXT NOT NULL
규격 TEXT
단위 TEXT NOT NULL
material_cost REAL DEFAULT 0        -- 재료비
labor_cost REAL DEFAULT 0           -- 노묘비
expense_cost REAL DEFAULT 0         -- 경비
비고 TEXT
생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
UNIQUE(project_id, code)
```

> ⚠️ 합계 컬럼 없음 — 재+노+경 합산은 프론트에서 계산

---

## 단가 테이블 목록 (11개)

| 테이블명 | 특수 컬럼 | 비고 |
|---|---|---|
| 품셈단가 | - | |
| 일위대가 | 단위수량, 구성내역 | |
| 견적단가 | - | |
| 자재단가_사급 | - | |
| 자재단가_관급 | 검수일자 | |
| 경비단가 | - | |
| 노임단가 | 단가기준 | 예: "2024년 상반기" |
| 표준시장단가 | labor_ratio, 적용일자 | |
| 관급수수료 | 수량, 계약번호 | 준공 시 1회 갱신 |
| gov_tc | 수량, 계약번호 | 준공 시 1회 갱신 |
| 실정보고단가 | 버전, 실정보고걸명 | 감사 1순위, 수정일시 없음 |

---

## 실정보고단가 버전 관리 규칙
- 동일 품명+규격에서 단가 변경 시 → 코드 신규 채번 후 새 행 추가
- v1, v2... = 검토/협의 중
- final = 감사 완료 또는 승인 확정
- final 이후 해당 품명+규격 코드 변경 불가
- 원본 서류는 대호가 별도 파일로 관리 (DB에 저장 안 함)

---

## 노임단가 운용 규칙
- 발주 당시 적용 노임을 단가기준 컬럼에 명시하여 등록
- 노임 고시 변경 시 → 새 코드로 행 추가, 기존 행 유지
- 적용 시작/종료일 관리 안 함 — 코드로 구분

---

## 단가 코드 채번 규칙

형식: `[파일명(확장자제외)]-NNNNN` (5자리 연번)

예시:
- 품셈단가_data-00001
- 실정보고단가_data-00003
- gov_tc_data-00001

규칙:
- 코드 앞부분 = JSON 파일명에서 .json 제거
- 같은 파일 내 최대 연번 +1로 채번
- 파일 간 연번은 독립 관리
- 코드는 한번 부여하면 변경 불가 (불변)
- 엑셀 → JSON 변환 시 AI가 자동 채번

---

## API 타입코드 ↔ 테이블명 매핑

> ⚠️ 현재 routes/api.py는 구버전 테이블명(unit_cost_*)을 사용 중 — 수정 예정
