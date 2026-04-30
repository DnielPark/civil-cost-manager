-- 단가DB 스키마 (unit_price.db)
-- 12개 테이블: 10개 기본 + 표준시장단가 + 관급자재3종 + 실정보고단가

-- ========================================
-- 1단계: 공통 컬럼 구조 (10개 기본 테이블)
-- ========================================

-- 1. 일위대가 (설계 시 복합 공종 단가)
CREATE TABLE IF NOT EXISTS 일위대가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 품셈단가 (품셈 기준 표준 단가)
CREATE TABLE IF NOT EXISTS 품셈단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 견적단가 (특수 자재/공법 견적)
CREATE TABLE IF NOT EXISTS 견적단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. 자재단가_사급 (시공사 조달 자재)
CREATE TABLE IF NOT EXISTS 자재단가_사급 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 경비단가 (제경비 항목)
CREATE TABLE IF NOT EXISTS 경비단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 노임단가 (인걸비 기준)
CREATE TABLE IF NOT EXISTS 노임단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 2단계: 표준시장단가 (특수 컬럼 추가)
-- ========================================

CREATE TABLE IF NOT EXISTS 표준시장단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    코드 TEXT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    노무비율 REAL,
    적용일자 DATE,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 3단계: 관급자재 3종 (검수일자 + 계약 추적)
-- ========================================

-- 7. 자재단가_관급 (발주처 제공 자재)
CREATE TABLE IF NOT EXISTS 자재단가_관급 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    검수일자 DATE,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. 관급수수료 (조달청 발주 계약별)
CREATE TABLE IF NOT EXISTS 관급수수료 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    계약번호 TEXT NOT NULL,
    단위 TEXT NOT NULL,
    경비 REAL NOT NULL,
    합계 REAL NOT NULL,
    계약일자 DATE,
    변경차수 INTEGER DEFAULT 0,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. 관급울반비 (극히 드문 특수 케이스)
CREATE TABLE IF NOT EXISTS 관급울반비 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT,
    단위 TEXT NOT NULL,
    경비 REAL NOT NULL,
    합계 REAL NOT NULL,
    발생일자 DATE,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    수정일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 4단계: 실정보고단가 (버전 관리 시스템)
-- ========================================

CREATE TABLE IF NOT EXISTS 실정보고단가 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    품명 TEXT NOT NULL,
    규격 TEXT NOT NULL,
    단위 TEXT,
    재료비 REAL DEFAULT 0,
    노무비 REAL DEFAULT 0,
    경비 REAL DEFAULT 0,
    합계 REAL NOT NULL,
    
    -- ⭐ 추적 라벨: "1차 1회분 v1", "1차 1회분 Final"
    추적라벨 TEXT NOT NULL,
    승인공문번호 TEXT, -- Final일 때만 입력
    
    접수일자 DATE,
    승인일자 DATE, -- Final일 때만 입력
    증감사유 TEXT,
    보고일자 DATE,
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 인덱스 설계 (성능 최적화)
-- ========================================

-- 기본 테이블 인덱스
CREATE INDEX IF NOT EXISTS idx_일위대가_품명 ON 일위대가(품명);
CREATE INDEX IF NOT EXISTS idx_품셈단가_품명 ON 품셈단가(품명);
CREATE INDEX IF NOT EXISTS idx_견적단가_품명 ON 견적단가(품명);
CREATE INDEX IF NOT EXISTS idx_자재단가_사급_품명 ON 자재단가_사급(품명);
CREATE INDEX IF NOT EXISTS idx_경비단가_품명 ON 경비단가(품명);
CREATE INDEX IF NOT EXISTS idx_노임단가_품명 ON 노임단가(품명);

-- 표준시장단가 인덱스
CREATE INDEX IF NOT EXISTS idx_표준시장단가_품명 ON 표준시장단가(품명);
CREATE INDEX IF NOT EXISTS idx_표준시장단가_코드 ON 표준시장단가(코드);

-- 자재단가_관급
CREATE INDEX IF NOT EXISTS idx_자재단가_관급_품명 ON 자재단가_관급(품명);
CREATE INDEX IF NOT EXISTS idx_자재단가_관급_검수일자 ON 자재단가_관급(검수일자);

-- 관급수수료 (계약 추적)
CREATE INDEX IF NOT EXISTS idx_관급수수료_품명 ON 관급수수료(품명);
CREATE INDEX IF NOT EXISTS idx_관급수수료_계약번호 ON 관급수수료(계약번호);
CREATE INDEX IF NOT EXISTS idx_관급수수료_계약번호_변경차수 ON 관급수수료(계약번호, 변경차수);

-- 관급울반비
CREATE INDEX IF NOT EXISTS idx_관급울반비_품명 ON 관급울반비(품명);

-- 실정보고단가 인덱스
CREATE INDEX IF NOT EXISTS idx_실정보고단가_품명 ON 실정보고단가(품명);
CREATE INDEX IF NOT EXISTS idx_실정보고단가_추적라벨 ON 실정보고단가(추적라벨);
CREATE INDEX IF NOT EXISTS idx_실정보고단가_공문번호 ON 실정보고단가(승인공문번호);
CREATE INDEX IF NOT EXISTS idx_실정보고단가_접수일자 ON 실정보고단가(접수일자);
CREATE INDEX IF NOT EXISTS idx_실정보고단가_승인일자 ON 실정보고단가(승인일자);
