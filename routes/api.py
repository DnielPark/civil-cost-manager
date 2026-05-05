"""
API 라우트 - JSON 데이터 제공
"""

from flask import Blueprint, jsonify, request
from database.init_db import get_connection
import sqlite3

api_bp = Blueprint('api', __name__)

# 단가 유형별 테이블 매핑
UNIT_TABLES = {
    '품셈단가': '품셈단가',
    '일위대가': '일위대가',
    '견적단가': '견적단가',
    '자재단가_사급': '자재단가_사급',
    '자재단가_관급': '자재단가_관급',
    '경비단가': '경비단가',
    '노임단가': '노임단가',
    '표준시장단가': '표준시장단가',
    '관급수수료': '관급수수료',
    'gov_tc': 'gov_tc',
    '실정보고단가': '실정보고단가',
}

# 테이블별 추가 컬럼 (get_unit_prices에서 사용)
TABLE_EXTRA_COLUMNS = {
    '일위대가': ['단위수량', '구성내역'],
    '자재단가_관급': ['검수일자'],
    '노임단가': ['단가기준'],
    '표준시장단가': ['labor_ratio', '적용일자'],
    '관급수수료': ['수량', '계약번호'],
    'gov_tc': ['수량', '계약번호'],
    '실정보고단가': ['버전', '실정보고걸명'],
}

BASE_COLUMNS = ['id', 'project_id', 'code', '품명', '규격', '단위',
                'material_cost', 'labor_cost', 'expense_cost', '비고',
                '생성일시']


def safe_db(func):
    """DB 에러 핸들링 데코레이터"""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return jsonify({'error': '데이터베이스 오류', 'detail': str(e)}), 500
        except Exception as e:
            return jsonify({'error': '서버 오류', 'detail': str(e)}), 500
    return wrapper


@api_bp.route('/projects', methods=['GET'])
@safe_db
def list_projects():
    """프로젝트 목록 API"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(projects)


@api_bp.route('/projects', methods=['POST'])
@safe_db
def create_project():
    """프로젝트 생성 API"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': '프로젝트 이름이 필요합니다.'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (name) VALUES (?)',
                   (data['name'],))
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': project_id, 'message': '생성 완료'}), 201


@api_bp.route('/unit-prices/<int:project_id>/<table_type>', methods=['GET'])
@safe_db
def get_unit_prices(project_id, table_type):
    """단가명세표 조회 API"""
    if table_type not in UNIT_TABLES:
        return jsonify({'error': '잘못된 단가 유형입니다.'}), 400

    table = UNIT_TABLES[table_type]
    extra_cols = TABLE_EXTRA_COLUMNS.get(table_type, [])
    all_cols = BASE_COLUMNS + extra_cols

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE project_id = ? ORDER BY id', (project_id,))
    rows = cursor.fetchall()
    conn.close()

    prices = []
    for row in rows:
        item = {}
        for col in all_cols:
            try:
                item[col] = row[col]
            except (KeyError, IndexError):
                item[col] = None
        prices.append(item)

    return jsonify(prices)


@api_bp.route('/unit-prices/<int:project_id>', methods=['GET'])
@safe_db
def get_all_unit_prices(project_id):
    """프로젝트의 모든 단가 데이터 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    result = {}

    for key, table in UNIT_TABLES.items():
        cursor.execute(f'SELECT * FROM {table} WHERE project_id = ? ORDER BY id', (project_id,))
        rows = cursor.fetchall()
        result[key] = [dict(row) for row in rows]

    conn.close()
    return jsonify(result)


# --- 단가 추가 API (POST) ---

@api_bp.route('/unit-prices/<int:project_id>/<table_type>', methods=['POST'])
@safe_db
def add_unit_price(project_id, table_type):
    """단가 추가 API - 추후 구현 예정"""
    return jsonify({'error': '단가 추가 API는 추후 구현 예정입니다.'}), 501


# --- 단가 수정 API (PUT) ---

@api_bp.route('/unit-prices/<int:project_id>/<table_type>/<int:item_id>', methods=['PUT'])
@safe_db
def update_unit_price(project_id, table_type, item_id):
    """단가 수정 API - 추후 구현 예정"""
    return jsonify({'error': '단가 수정 API는 추후 구현 예정입니다.'}), 501
