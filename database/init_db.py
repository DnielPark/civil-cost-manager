#!/usr/bin/env python3
"""
단가 데이터베이스 초기화 스크립트
- schema.sql 실행하여 11개 테이블 생성
- 기존 docs/*.json 파일 마이그레이션 (선택)
"""

import sqlite3
import json
import os
from pathlib import Path

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / 'civil_cost.db'
SCHEMA_PATH = BASE_DIR / 'database' / 'schema.sql'
DOCS_DIR = BASE_DIR / 'docs'


def init_database():
    """데이터베이스 초기화 및 테이블 생성"""
    print(f"데이터베이스 경로: {DB_PATH}")
    
    # 데이터베이스 연결 (없으면 생성)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 외래키 제약조건 활성화
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # 스키마 실행
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("✅ 스키마 적용 완료 (11개 테이블 생성)")
    else:
        print(f"❌ 스키마 파일을 찾을 수 없습니다: {SCHEMA_PATH}")
        return False
    
    conn.commit()
    conn.close()
    return True


def migrate_json_to_db():
    """docs/*.json 파일을 데이터베이스로 마이그레이션"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 마이그레이션 매핑: JSON 파일명 → 테이블명
    migration_map = {
        '노임.json': '노임단가',
        '경비.json': '경비단가',
        '자재.json': '자재단가_사급',  # 또는 관급, 구분 필요시 수정
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
            # JSON 키를 테이블 컬럼에 매핑
            품명 = item.get('명칭', '')
            규격 = item.get('규격', '')
            단위 = item.get('단위', '')
            
            # 금액 필드 처리 (다양한 키 이름 대응)
            재료비 = item.get('재료비', 0) or 0
            노묵비 = item.get('노묵비', 0) or item.get('단가', 0) or 0
            경비 = item.get('경비', 0) or 0
            합계 = item.get('합계', 0) or item.get('단가', 0) or 0
            비고 = item.get('비고', '')
            
            cursor.execute(f"""
                INSERT INTO {table_name} (품명, 규격, 단위, 재료비, 노묵비, 경비, 합계, 비고)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (품명, 규격, 단위, 재료비, 노묵비, 경비, 합계, 비고))
        
        print(f"✅ {len(data)}개 항목 마이그레이션 완료")
    
    conn.commit()
    conn.close()
    print("\n🎉 마이그레이션 완료!")


def verify_tables():
    """테이블 생성 확인"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("\n📊 생성된 테이블 목록:")
    expected_tables = [
        '일위대가', '품셈단가', '표준시장단가', '견적단가',
        '자재단가_사급', '자재단가_관급', '관급수수료', '관급울반비',
        '경비단가', '노임단가', '실정보고단가'
    ]
    
    for table in expected_tables:
        exists = any(t[0] == table for t in tables)
        status = "✅" if exists else "❌"
        print(f"  {status} {table}")
    
    conn.close()


def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("단가 데이터베이스 초기화")
    print("=" * 50)
    
    # Step 1: 데이터베이스 초기화
    if init_database():
        # Step 2: 테이블 확인
        verify_tables()
        
        # Step 3: 마이그레이션 (선택)
        print("\n📁 마이그레이션할 JSON 파일:")
        json_files = list(DOCS_DIR.glob('*.json'))
        for f in json_files:
            print(f"  - {f.name}")
        
        if json_files:
            response = input("\n마이그레이션을 실행하시겠습니까? (y/n): ")
            if response.lower() == 'y':
                migrate_json_to_db()
        else:
            print("  마이그레이션할 JSON 파일이 없습니다.")
    
    print("\n" + "=" * 50)
    print("초기화 완료!")
    print("=" * 50)


if __name__ == '__main__':
    main()
