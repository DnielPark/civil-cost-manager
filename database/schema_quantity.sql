-- 수량DB 스키마 (quantity.db)
-- 수량내역 + 수량이력 (차수 관리)

-- ========================================
-- 1단계: 수량내역 테이블 (메타 정보)
-- ========================================

CREATE TABLE IF NOT EXISTS 수량내역 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 계층 구조 (유연하게 NULL 허용)
    하위프로젝트 TEXT, -- 토목/건축/기계/전기/관급/폐기물/기타
    공구 TEXT DEFAULT '-', -- 1공구/2공구/1지구/2지구 (없으면 '-')
    분구 TEXT DEFAULT '-', -- 1마을/2마을/1권역/2권역 (없으면 '-')
    세부공종 TEXT, -- 토공/하천공/구조물공/부대공/경비성
    
    -- 단가 참조
    단가_테이블 TEXT NOT NULL, -- '일위대가', '품셈단가', '실정보고단가' 등
    단가_ID INTEGER NOT NULL,
    
    -- 이력 관리
    최초생성차수 INTEGER DEFAULT 0, -- 언제 처음 생겼는지 (0=당초)
    최종수정차수 INTEGER DEFAULT 0, -- 마지막 수정 차수
    활성여부 BOOLEAN DEFAULT 1, -- 삭제된 항목 = 0
    
    비고 TEXT,
    생성일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 2단계: 수량이력 테이블 (차수별 실제 수량) ⭐ 핵심
-- ========================================

CREATE TABLE IF NOT EXISTS 수량이력 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    수량내역_id INTEGER NOT NULL,
    
    -- ⭐ 차수별 버전 관리
    차수 INTEGER NOT NULL, -- 0=당초, 1=1차, 2=2차...
    회차 INTEGER NOT NULL, -- 1=1회, 2=2회...
    버전 TEXT NOT NULL, -- 'v1', 'v2', 'Final'
    
    수량 REAL NOT NULL,
    변경사유 TEXT,
    변경일시 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (수량내역_id) REFERENCES 수량내역(id)
);

-- ========================================
-- 3단계: 인덱스 설계 (성능 최적화) ⭐ 매우 중요
-- ========================================

-- 복합 인덱스 (계층 구조 필터용)
CREATE INDEX IF NOT EXISTS idx_계층구조 
ON 수량내역(하위프로젝트, 공구, 분구, 세부공종);

-- 단가 참조 인덱스 (JOIN 최적화)
CREATE INDEX IF NOT EXISTS idx_단가참조 
ON 수량내역(단가_테이블, 단가_ID);

-- 개별 필터용
CREATE INDEX IF NOT EXISTS idx_하위프로젝트 ON 수량내역(하위프로젝트);
CREATE INDEX IF NOT EXISTS idx_공구 ON 수량내역(공구);
CREATE INDEX IF NOT EXISTS idx_세부공종 ON 수량내역(세부공종);

-- 수량이력 조회 최적화 (핵심!)
CREATE UNIQUE INDEX IF NOT EXISTS idx_수량이력_조회 
ON 수량이력(수량내역_id, 차수, 회차, 버전);

-- 개별 필터용
CREATE INDEX IF NOT EXISTS idx_차수 ON 수량이력(차수);
CREATE INDEX IF NOT EXISTS idx_회차 ON 수량이력(회차);
CREATE INDEX IF NOT EXISTS idx_버전 ON 수량이력(버전);
