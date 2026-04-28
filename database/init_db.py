"""
데이터베이스 초기화 모듈
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'civil_cost.db')


def get_connection():
    """데이터베이스 연결 반환"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """데이터베이스 및 테이블 생성"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript('''
        -- 프로젝트 테이블
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 내역단가 목록표 (최상위 - 최종 설계)
        CREATE TABLE IF NOT EXISTS unit_cost_final (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            unit_quantity REAL DEFAULT 1.0,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            cost_source TEXT,
            source_id INTEGER,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            UNIQUE(project_id, work_name, spec)
        );

        -- 일위대가 목록표 (복합)
        CREATE TABLE IF NOT EXISTS unit_cost_composite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            unit_quantity REAL DEFAULT 1.0,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            composition_detail TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            UNIQUE(project_id, work_name, spec)
        );

        -- 품셈단가 목록표
        CREATE TABLE IF NOT EXISTS unit_cost_standard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            unit_quantity REAL DEFAULT 1.0,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            UNIQUE(project_id, work_name, spec)
        );

        -- 표준시장단가 목록표
        CREATE TABLE IF NOT EXISTS unit_cost_market (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            unit_quantity REAL DEFAULT 1.0,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            UNIQUE(project_id, work_name, spec)
        );

        -- 견적단가 목록표
        CREATE TABLE IF NOT EXISTS unit_cost_quote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            unit_quantity REAL DEFAULT 1.0,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            UNIQUE(project_id, work_name, spec)
        );

        -- 물가정보지 목록표
        CREATE TABLE IF NOT EXISTS unit_cost_price_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            unit_quantity REAL DEFAULT 1.0,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            publisher TEXT,
            issue_date TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            UNIQUE(project_id, work_name, spec)
        );
    ''')

    # 샘플 프로젝트
    cursor.execute('INSERT OR IGNORE INTO projects (id, name, location) VALUES (1, ?, ?)',
                   ('OO고속도로 1공구', '경기도'))

    # 샘플 단가 데이터 (project_id=1)
    samples = {
        'unit_cost_final': [
            ('흙파기(기계)', '3.0m 이내', 'm³', 1.0, 0, 7200, 1300, 'standard', 1, '품셈 참조'),
            ('되메우기(기계)', '3.0m 이내', 'm³', 1.0, 0, 5100, 1100, 'standard', 2, '품셈 참조'),
            ('콘크리트타설', '25-210-12', 'm³', 1.0, 125000, 48000, 12000, 'composite', 1, '일위대가 참조'),
            ('아스콘포장', '5cm', 'm²', 1.0, 9500, 2500, 500, 'market', 2, '표준시장 참조'),
            ('배수로설치', 'U형측구 300x300', 'm', 1.0, 32000, 10000, 3000, 'quote', 1, '견적 참조'),
        ],
        'unit_cost_composite': [
            ('콘크리트타설', '25-210-12', 'm³', 1.0, 125000, 48000, 12000, '{"standard": [1, 3], "market": [1]}', '레미콘+품셈'),
            ('철근가공조립', 'D13', 'ton', 1.0, 850000, 320000, 80000, '{"standard": [4]}', '철근 품셈'),
            ('거푸집', '일반형', 'm²', 1.0, 18500, 8500, 1500, '{"standard": [5]}', '합판 3회'),
        ],
        'unit_cost_standard': [
            ('흙파기', '3.0m 이내', 'm³', 1.0, 0, 7200, 1300, '인력'),
            ('되메우기', '3.0m 이내', 'm³', 1.0, 0, 5100, 1100, '다짐포함'),
            ('터파기', '5.0m 이내', 'm³', 1.0, 2500, 8500, 1500, '기계굴착'),
            ('철근', 'D13 가공', 'ton', 1.0, 800000, 300000, 70000, 'SD400'),
            ('콘크리트', '25MPa', 'm³', 1.0, 115000, 42000, 10000, '레미콘'),
        ],
        'unit_cost_market': [
            ('모래포설', '10cm', 'm²', 1.0, 2800, 800, 200, '강모래'),
            ('아스콘포장', '5cm', 'm²', 1.0, 9500, 2500, 500, '밀입도'),
        ],
        'unit_cost_quote': [
            ('배수로', 'U형측구 300x300', 'm', 1.0, 32000, 10000, 3000, '기성품'),
        ],
        'unit_cost_price_info': [
            ('시멘트', '보통포틀랜드 40kg', '포', 1.0, 4500, 0, 0, '한국물가정보', '2026-03', ''),
            ('레미콘', '25-210-12', 'm³', 1.0, 105000, 0, 0, '한국물가정보', '2026-03', ''),
        ],
    }

    for table, items in samples.items():
        for item in items:
            # unit_cost_final은 cost_source, source_id 포함
            if table == 'unit_cost_final':
                cursor.execute(f'''
                    INSERT OR IGNORE INTO {table}
                    (project_id, work_name, spec, unit, unit_quantity, material_cost, labor_cost, expense_cost, cost_source, source_id, note)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', item)
            elif table == 'unit_cost_composite':
                cursor.execute(f'''
                    INSERT OR IGNORE INTO {table}
                    (project_id, work_name, spec, unit, unit_quantity, material_cost, labor_cost, expense_cost, composition_detail, note)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', item)
            elif table == 'unit_cost_price_info':
                cursor.execute(f'''
                    INSERT OR IGNORE INTO {table}
                    (project_id, work_name, spec, unit, unit_quantity, material_cost, labor_cost, expense_cost, publisher, issue_date, note)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', item)
            else:
                cursor.execute(f'''
                    INSERT OR IGNORE INTO {table}
                    (project_id, work_name, spec, unit, unit_quantity, material_cost, labor_cost, expense_cost, note)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', item)

    conn.commit()
    conn.close()
    print(f"✅ 데이터베이스 초기화 완료: {DB_PATH}")
