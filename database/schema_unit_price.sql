-- 단가DB 스키마 (unit_price.db)
-- 11개 테이블: JSON 키 기준으로 컬럼 정의

-- ========================================
-- 1단계: 기본 테이블 (재료비/labor_cost/경비 구조)
-- ========================================

-- 1. 품셈단가 (품셈 기준 표준 단가)
CREATE TABLE IF NOT EXISTS 품셈단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 2. 견적단가 (특수 자재/공법 견적)
CREATE TABLE IF NOT EXISTS 견적단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 3. 자재단가_사급 (시공사 조달 자재)
CREATE TABLE IF NOT EXISTS 자재단가_사급 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 4. 경비단가 (제경비 항목)
CREATE TABLE IF NOT EXISTS 경비단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 5. 노임단가 (인걸비 기준)
CREATE TABLE IF NOT EXISTS 노임단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    단가기준 TEXT, -- 예: "2024년 상반기", "2025년 하반기"
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- ========================================
-- 2단계: 특수 컬럼 테이블
-- ========================================

-- 6. 표준시장단가 (labor_cost_ratio, 적용일자)
CREATE TABLE IF NOT EXISTS 표준시장단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    labor_ratio REAL,
    적용일자 DATE,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 7. 자재단가_관급 (검수일자)
CREATE TABLE IF NOT EXISTS 자재단가_관급 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    검수일자 DATE,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 8. 관급수수료 (수량, 계약번호)
CREATE TABLE IF NOT EXISTS 관급수수료 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    수량 REAL DEFAULT 1,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    계약번호 TEXT,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 9. gov_tc (수량, 계약번호)
CREATE TABLE IF NOT EXISTS gov_tc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    수량 REAL DEFAULT 1,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    계약번호 TEXT,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 10. 일위대가 (단위수량, 구성내역)
CREATE TABLE IF NOT EXISTS 일위대가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    단위수량 REAL DEFAULT 1,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    구성내역 TEXT,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- 11. 실정보고단가 (버전, 실정보고걸명)
CREATE TABLE IF NOT EXISTS 실정보고단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    expense_cost REAL DEFAULT 0,
    버전 TEXT,
    실정보고걸명 TEXT,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, code)
);

-- ========================================
-- 인덱스 설계 (성능 최적화)
-- ========================================

-- 기본 테이블 인덱스
CREATE INDEX IF NOT EXISTS idx_품셈단가_품명 ON 품셈단가(품명);
CREATE INDEX IF NOT EXISTS idx_견적단가_품명 ON 견적단가(품명);
CREATE INDEX IF NOT EXISTS idx_자재단가_사급_품명 ON 자재단가_사급(품명);
CREATE INDEX IF NOT EXISTS idx_경비단가_품명 ON 경비단가(품명);
CREATE INDEX IF NOT EXISTS idx_노임단가_품명 ON 노임단가(품명);

-- 표준시장단가 인덱스
CREATE INDEX IF NOT EXISTS idx_표준시장단가_품명 ON 표준시장단가(품명);
CREATE INDEX IF NOT EXISTS idx_표준시장단가_코드 ON 표준시장단가(code);

-- 자재단가_관급
CREATE INDEX IF NOT EXISTS idx_자재단가_관급_품명 ON 자재단가_관급(품명);
CREATE INDEX IF NOT EXISTS idx_자재단가_관급_검수일자 ON 자재단가_관급(검수일자);

-- 관급수수료
CREATE INDEX IF NOT EXISTS idx_관급수수료_품명 ON 관급수수료(품명);
CREATE INDEX IF NOT EXISTS idx_관급수수료_계약번호 ON 관급수수료(계약번호);

-- gov_tc
CREATE INDEX IF NOT EXISTS idx_gov_tc_품명 ON gov_tc(품명);

-- 일위대가
CREATE INDEX IF NOT EXISTS idx_일위대가_품명 ON 일위대가(품명);

-- 실정보고단가 인덱스
CREATE INDEX IF NOT EXISTS idx_실정보고단가_품명 ON 실정보고단가(품명);
CREATE INDEX IF NOT EXISTS idx_실정보고단가_버전 ON 실정보고단가(버전);
