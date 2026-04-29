#!/usr/bin/env python3
"""
단가/수량 데이터베이스 초기화 스크립트
- unit_price.db: 12개 단가 테이블
- quantity.db: 수량내역 + 수량이력 (차수 관리)
"""

import sqlite3
import json
import os
from pathlib import Path

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / 'database'
DOCS_DIR = BASE_DIR / 'docs'

UNIT_PRICE_DB = DB_DIR / 'unit_price.db'
QUANTITY_DB = DB_DIR / 'quantity.db'

SCHEMA_UNIT_PRICE = DB_DIR / 'schema_unit_price.sql'
SCHEMA_QUANTITY = DB_DIR / 'schema_quantity.sql'


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
        '자재단가_사급', '자재단가_관급', '관급수수료', 'TC목록',
        '경비단가', '노임단가', '실정보고단가'
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


def migrate_json_to_unit_price():
    """docs/*.json 파일을 단가DB로 마이그레이션"""
    conn = sqlite3.connect(UNIT_PRICE_DB)
    cursor = conn.cursor()
    
    # 마이그레이션 매핑: JSON 파일명 → 테이블명
    migration_map = {
        '노임.json': '노임단가',
        '경비.json': '경비단가',
        '자재.json': '자재단가_사급',
    }
    
    for json_file, table_name in migration_map.items():
        json_path = DOCS_DIR / json_file
        if not json_path.exists():
            print(f"⚠️ 파일 없음: {json_file}")
            continue
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📥 {json_file} → {table_name} 마이그레이션 중...")
        
        for item in data:
            품명 = item.get('명칭', '')
            규격 = item.get('규격', '')
            단위 = item.get('단위', '')
            
            # 금액 필드 처리
            재료비 = item.get('재료비', 0) or 0
            노무비 = item.get('노무비', 0) or item.get('단가', 0) or 0
            경비 = item.get('경비', 0) or 0
            합계 = item.get('합계', 0) or item.get('단가', 0) or 0
            비고 = item.get('비고', '')
            
            cursor.execute(f"""
                INSERT INTO {table_name} (품명, 규격, 단위, 재료비, 노무비, 경비, 합계, 비고)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (품명, 규격, 단위, 재료비, 노무비, 경비, 합계, 비고))
        
        print(f"✅ {len(data)}개 항목 마이그레이션 완료")
    
    conn.commit()
    conn.close()
    print("\n🎉 단가DB 마이그레이션 완료!")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("단가/수량 데이터베이스 초기화")
    print("=" * 60)
    
    # Step 1: 단가DB 초기화
    if init_unit_price_db():
        verify_unit_price_tables()
    
    # Step 2: 수량DB 초기화
    if init_quantity_db():
        verify_quantity_tables()
    
    # Step 3: 마이그레이션 (선택)
    print("\n📁 마이그레이션할 JSON 파일:")
    json_files = list(DOCS_DIR.glob('*.json'))
    for f in json_files:
        print(f"  - {f.name}")
    
    if json_files:
        response = input("\n마이그레이션을 실행하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            migrate_json_to_unit_price()
    else:
        print("  마이그레이션할 JSON 파일이 없습니다.")
    
    print("\n" + "=" * 60)
    print("초기화 완료!")
    print("=" * 60)


if __name__ == '__main__':
    main()
