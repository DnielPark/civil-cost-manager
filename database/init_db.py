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
        -- 공사 정보 테이블
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            start_date TEXT,
            end_date TEXT,
            budget REAL DEFAULT 0,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 공종/항목 테이블
        CREATE TABLE IF NOT EXISTS cost_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            parent_id INTEGER,
            code TEXT,
            name TEXT NOT NULL,
            unit TEXT,
            quantity REAL DEFAULT 0,
            unit_price REAL DEFAULT 0,
            total_price REAL DEFAULT 0,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (parent_id) REFERENCES cost_items(id)
        );

        -- 단가명세서 테이블
        CREATE TABLE IF NOT EXISTS unit_price_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_name TEXT NOT NULL,
            spec TEXT NOT NULL,
            unit TEXT NOT NULL,
            total_price REAL NOT NULL,
            material_cost REAL DEFAULT 0,
            labor_cost REAL DEFAULT 0,
            expense_cost REAL DEFAULT 0,
            note TEXT,
            UNIQUE(work_name, spec)
        );
    ''')

    # 샘플 단가 데이터 (중복 방지)
    sample_prices = [
        ('흙파기', '3.0m 이내', 'm³', 8500, 0, 7200, 1300, '인력굴착'),
        ('되메우기', '3.0m 이내', 'm³', 6200, 0, 5100, 1100, '다짐포함'),
        ('콘크리트타설', '25-210-12', 'm³', 185000, 125000, 48000, 12000, '레미콘 포함'),
        ('거푸집', '일반형', 'm²', 28500, 18500, 8500, 1500, '합판 3회 전용'),
        ('철근가공조립', 'D13', 'ton', 1250000, 850000, 320000, 80000, 'SD400'),
        ('터파기', '5.0m 이내', 'm³', 12500, 2500, 8500, 1500, '기계굴착'),
        ('모래포설', '10cm', 'm²', 3800, 2800, 800, 200, '강모래'),
        ('잡석다짐', '20cm', 'm²', 8500, 6200, 1800, 500, 'CR-40'),
        ('배수로', 'U형측구 300x300', 'm', 45000, 32000, 10000, 3000, '기성품'),
        ('아스콘포장', '5cm', 'm²', 12500, 9500, 2500, 500, '밀입도'),
    ]

    for item in sample_prices:
        cursor.execute('''
            INSERT OR IGNORE INTO unit_price_list
            (work_name, spec, unit, total_price, material_cost, labor_cost, expense_cost, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)

    conn.commit()
    conn.close()
    print(f"✅ 데이터베이스 초기화 완료: {DB_PATH}")
