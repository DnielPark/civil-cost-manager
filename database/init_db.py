#!/usr/bin/env python3
"""
단가/수량 데이터베이스 초기화 스크립트
- unit_price.db: 11개 단가 테이블 + projects 테이블
- quantity.db: 수량내역 + 수량이력 (차수 관리)

사용법:
  python3 database/init_db.py --project 샘플_1공구
  python3 database/init_db.py  # 프로젝트 목록 출력 후 선택
"""

import sqlite3
import json
import os
import sys
import argparse
from pathlib import Path

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / 'database'
DOCS_BASE_DIR = BASE_DIR / 'docs'

UNIT_PRICE_DB = DB_DIR / 'unit_price.db'
QUANTITY_DB = DB_DIR / 'quantity.db'

SCHEMA_UNIT_PRICE = DB_DIR / 'schema_unit_price.sql'
SCHEMA_QUANTITY = DB_DIR / 'schema_quantity.sql'


def init_projects_table():
    """projects 테이블 생성 (없으면)"""
    conn = sqlite3.connect(UNIT_PRICE_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ projects 테이블 준비 완료")


def get_connection():
    """단가DB 연결 반환 (row_factory 설정)"""
    conn = sqlite3.connect(str(UNIT_PRICE_DB))
    conn.row_factory = sqlite3.Row
    return conn


def get_or_create_project(project_name):
    """프로젝트 등록 또는 기존 ID 반환"""
    conn = sqlite3.connect(UNIT_PRICE_DB)
    cursor = conn.cursor()
    
    # 기존 프로젝트 확인
    cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
    result = cursor.fetchone()
    
    if result:
        project_id = result[0]
        print(f"📁 기존 프로젝트 사용: {project_name} (ID: {project_id})")
    else:
        # 새 프로젝트 등록
        cursor.execute("INSERT INTO projects (name) VALUES (?)", (project_name,))
        project_id = cursor.lastrowid
        print(f"📁 새 프로젝트 등록: {project_name} (ID: {project_id})")
    
    conn.commit()
    conn.close()
    return project_id


def list_projects():
    """docs/ 하위 폴터 목록 출력"""
    if not DOCS_BASE_DIR.exists():
        print("❌ docs/ 폴터가 없습니다.")
        return []
    
    projects = [d.name for d in DOCS_BASE_DIR.iterdir() if d.is_dir()]
    return projects


def init_unit_price_db():
    """단가DB 초기화 (unit_price.db)"""
    print(f"📦 단가DB 초기화: {UNIT_PRICE_DB}")
    
    conn = sqlite3.connect(UNIT_PRICE_DB)
    cursor = conn.cursor()
    
    if SCHEMA_UNIT_PRICE.exists():
        with open(SCHEMA_UNIT_PRICE, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("✅ 단가DB 스키마 적용 완료 (11개 테이블)")
    else:
        print(f"❌ 스키마 파일 없음: {SCHEMA_UNIT_PRICE}")
        return False
    
    conn.commit()
    conn.close()
    return True


def init_quantity_db():
    """수량DB 초기화 (quantity.db)"""
    print(f"📦 수량DB 초기화: {QUANTITY_DB}")
    
    conn = sqlite3.connect(QUANTITY_DB)
    cursor = conn.cursor()
    
    # 외래키 제약조건 활성화
    cursor.execute("PRAGMA foreign_keys = ON")
    
    if SCHEMA_QUANTITY.exists():
        with open(SCHEMA_QUANTITY, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("✅ 수량DB 스키마 적용 완료 (2개 테이블)")
    else:
        print(f"❌ 스키마 파일 없음: {SCHEMA_QUANTITY}")
        return False
    
    conn.commit()
    conn.close()
    return True


def verify_unit_price_tables():
    """단가DB 테이블 확인"""
    conn = sqlite3.connect(UNIT_PRICE_DB)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("\n📊 단가DB 테이블 목록:")
    expected_tables = [
        '일위대가', '품셈단가', '표준시장단가', '견적단가',
        '자재단가_사급', '자재단가_관급', '관급수수료',
        '경비단가', '노임단가', '실정보고단가', 'gov_tc'
    ]
    
    for table in expected_tables:
        exists = any(t[0] == table for t in tables)
        status = "✅" if exists else "❌"
        print(f"  {status} {table}")
    
    conn.close()


def verify_quantity_tables():
    """수량DB 테이블 확인"""
    conn = sqlite3.connect(QUANTITY_DB)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("\n📊 수량DB 테이블 목록:")
    expected_tables = ['수량내역', '수량이력']
    
    for table in expected_tables:
        exists = any(t[0] == table for t in tables)
        status = "✅" if exists else "❌"
        print(f"  {status} {table}")
    
    conn.close()


def migrate_json_to_unit_price(project_id, docs_dir):
    """docs/*.json 파일을 단가DB로 마이그레이션 (UPSERT 지원, 테이블별 동적 컬럼)"""
    conn = sqlite3.connect(UNIT_PRICE_DB)
    cursor = conn.cursor()
    
    # 마이그레이션 매핑: JSON 파일명 → 테이블명
    migration_map = {
        '견적단가_data.json': '견적단가',
        '경비단가_data.json': '경비단가',
        '관급수수료_data.json': '관급수수료',
        'gov_tc_data.json': 'gov_tc',
        '노임단가_data.json': '노임단가',
        '실정보고단가_data.json': '실정보고단가',
        '일위대가_data.json': '일위대가',
        '자재단가_관급_data.json': '자재단가_관급',
        '자재단가_사급_data.json': '자재단가_사급',
        '표준시장단가_data.json': '표준시장단가',
        '품셈단가_data.json': '품셈단가',
    }
    
    # 테이블별 컬럼 매핑: JSON 키 → DB 컬럼명
    column_map = {
        '견적단가': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '비고'],
        '경비단가': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '비고'],
        '관급수수료': ['코드', '품명', '규격', '단위', '수량', 'material_cost', 'labor_cost', 'expense_cost', '계약번호', '비고'],
        'gov_tc': ['코드', '품명', '규격', '단위', '수량', 'material_cost', 'labor_cost', 'expense_cost', '계약번호', '비고'],
        '노임단가': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '단가기준', '비고'],
        '실정보고단가': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '버전', '실정보고건명', '비고'],
        '일위대가': ['코드', '품명', '규격', '단위', '단위수량', 'material_cost', 'labor_cost', 'expense_cost', '구성내역', '비고'],
        '자재단가_관급': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '검수일자', '비고'],
        '자재단가_사급': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '비고'],
        '표준시장단가': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', 'labor_ratio', '적용일자', '비고'],
        '품셈단가': ['코드', '품명', '규격', '단위', 'material_cost', 'labor_cost', 'expense_cost', '비고'],
    }
    
    for json_file, table_name in migration_map.items():
        json_path = docs_dir / json_file
        if not json_path.exists():
            print(f"⚠️ 파일 없음: {json_file}")
            continue
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📥 {json_file} → {table_name} 마이그레이션 중...")
        
        # 해당 테이블의 컬럼 목록
        columns = column_map.get(table_name, [])
        if not columns:
            print(f"⚠️ 컬럼 매핑 없음: {table_name}")
            continue
        
        for item in data:
            # 주석 블록 스킵
            if '_코드생성규칙' in item or '_버전관리규칙' in item:
                continue
            
            # 컬럼 값 추출
            values = []
            for col in columns:
                val = item.get(col, '')
                # 숫자 필드 처리
                if col in ['material_cost', 'labor_cost', 'expense_cost', '수량', '단위수량', 'labor_ratio']:
                    val = val if val else 0
                values.append(val)
            
            # INSERT 컬럼: project_id + code + 나머지 컬럼
            db_columns = ['project_id', 'code'] + [c for c in columns if c != '코드']
            placeholders = ', '.join(['?' for _ in db_columns])
            column_names = ', '.join(db_columns)
            
            # UPSERT SET 절
            update_cols = [c for c in db_columns if c not in ['project_id', 'code']]
            set_clause = ', '.join([f"{c}=excluded.{c}" for c in update_cols])
            
            cursor.execute(f"""
                INSERT INTO {table_name} ({column_names})
                VALUES ({placeholders})
                ON CONFLICT(project_id, code) DO UPDATE SET
                    {set_clause}
            """, [project_id] + values)
        
        print(f"✅ {len(data)}개 항목 마이그레이션 완료")
    
    conn.commit()
    conn.close()
    print("\n🎉 단가DB 마이그레이션 완료!")


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='단가/수량 데이터베이스 초기화')
    parser.add_argument('--project', type=str, help='마이그레이션할 프로젝트 폴더명 (예: 샘플_1공구)')
    args = parser.parse_args()
    
    print("=" * 60)
    print("단가/수량 데이터베이스 초기화")
    print("=" * 60)
    
    # Step 1: 단가DB 초기화
    if init_unit_price_db():
        verify_unit_price_tables()
    
    # Step 2: 수량DB 초기화
    if init_quantity_db():
        verify_quantity_tables()
    
    # Step 3: projects 테이블 준비
    init_projects_table()
    
    # Step 4: 프로젝트 선택 및 마이그레이션
    if args.project:
        project_name = args.project
        docs_dir = DOCS_BASE_DIR / project_name
        if not docs_dir.exists():
            print(f"\n❌ 프로젝트 폴더 없음: {docs_dir}")
            return
    else:
        # 프로젝트 목록 출력
        projects = list_projects()
        if not projects:
            print("\n⚠️ 마이그레이션할 프로젝트가 없습니다.")
            return
        
        print("\n📁 사용 가능한 프로젝트:")
        for i, name in enumerate(projects, 1):
            print(f"  {i}. {name}")
        
        try:
            choice = input("\n마이그레이션할 프로젝트 번호를 선택하세요: ")
            idx = int(choice) - 1
            if idx < 0 or idx >= len(projects):
                print("❌ 잘못된 선택입니다.")
                return
            project_name = projects[idx]
            docs_dir = DOCS_BASE_DIR / project_name
        except (ValueError, KeyboardInterrupt):
            print("\n❌ 취소되었습니다.")
            return
    
    # 프로젝트 등록 및 ID 발급
    project_id = get_or_create_project(project_name)
    
    # 마이그레이션 실행
    print(f"\n📂 프로젝트 폴더: {docs_dir}")
    migrate_json_to_unit_price(project_id, docs_dir)
    
    print("\n" + "=" * 60)
    print("초기화 완료!")
    print("=" * 60)


if __name__ == '__main__':
    main()
