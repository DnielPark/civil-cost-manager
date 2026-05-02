"""
API 라우트 - JSON 데이터 제공
"""

from flask import Blueprint, jsonify, request
from database.init_db import get_connection
import sqlite3

api_bp = Blueprint('api', __name__)

# 단가 유형별 테이블 매핑
UNIT_TABLES = {
    'final': 'unit_cost_final',
    'composite': 'unit_cost_composite',
    'standard': 'unit_cost_standard',
    'market': 'unit_cost_market',
    'quote': 'unit_cost_quote',
    'price_info': 'unit_cost_price_info',
    'field_report': 'unit_cost_field_report',
}

# 테이블별 추가 컬럼 (get_unit_prices에서 사용)
TABLE_EXTRA_COLUMNS = {
    'final': ['cost_source', 'source_id'],
    'composite': ['composition_detail'],
    'price_info': ['publisher', 'issue_date'],
}

BASE_COLUMNS = ['id', 'work_name', 'spec', 'unit', 'unit_quantity',
                'material_cost', 'labor_cost', 'expense_cost', 'note']


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
    cursor.execute('INSERT INTO projects (name, location) VALUES (?, ?)',
                   (data['name'], data.get('location')))
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
    """단가 추가 API"""
    if table_type not in UNIT_TABLES:
        return jsonify({'error': '잘못된 단가 유형입니다.'}), 400

    data = request.get_json()
    if not data or 'work_name' not in data or 'spec' not in data:
        return jsonify({'error': '공종명과 규격은 필수입니다.'}), 400

    table = UNIT_TABLES[table_type]
    conn = get_connection()
    cursor = conn.cursor()

    # 공통 필드
    common_fields = {
        'project_id': project_id,
        'work_name': data['work_name'],
        'spec': data['spec'],
        'unit': data.get('unit', ''),
        'unit_quantity': data.get('unit_quantity', 1.0),
        'material_cost': data.get('material_cost', 0),
        'labor_cost': data.get('labor_cost', 0),
        'expense_cost': data.get('expense_cost', 0),
        'note': data.get('note', ''),
    }

    # 테이블별 추가 필드
    extra = {}
    if table_type == 'final':
        extra['cost_source'] = data.get('cost_source', '')
        extra['source_id'] = data.get('source_id')
    elif table_type == 'composite':
        extra['composition_detail'] = data.get('composition_detail', '')
    elif table_type == 'price_info':
        extra['publisher'] = data.get('publisher', '')
        extra['issue_date'] = data.get('issue_date', '')

    all_fields = {**common_fields, **extra}
    columns = ', '.join(all_fields.keys())
    placeholders = ', '.join(['?' for _ in all_fields])
    values = list(all_fields.values())

    try:
        cursor.execute(f'''
            INSERT INTO {table} ({columns})
            VALUES ({placeholders})
        ''', values)
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': new_id, 'message': '추가 완료'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '동일한 공종명+규격이 이미 존재합니다.'}), 409


# --- 단가 수정 API (PUT) ---

@api_bp.route('/unit-prices/<int:project_id>/<table_type>/<int:item_id>', methods=['PUT'])
@safe_db
def update_unit_price(project_id, table_type, item_id):
    """단가 수정 API"""
    if table_type not in UNIT_TABLES:
        return jsonify({'error': '잘못된 단가 유형입니다.'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': '수정할 데이터가 필요합니다.'}), 400

    table = UNIT_TABLES[table_type]
    conn = get_connection()
    cursor = conn.cursor()

    # 해당 ID가 존재하는지 확인
    cursor.execute(f'SELECT id FROM {table} WHERE id = ? AND project_id = ?', (item_id, project_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': '해당 단가를 찾을 수 없습니다.'}), 404

    # 수정 가능한 필드 목록
    editable_fields = [
        'work_name', 'spec', 'unit', 'unit_quantity',
        'material_cost', 'labor_cost', 'expense_cost', 'note'
    ]

    # 테이블별 추가 필드
    if table_type == 'final':
        editable_fields.extend(['cost_source', 'source_id'])
    elif table_type == 'composite':
        editable_fields.append('composition_detail')
    elif table_type == 'price_info':
        editable_fields.extend(['publisher', 'issue_date'])

    # 요청에서 수정할 필드만 추출
    updates = {}
    for field in editable_fields:
        if field in data:
            updates[field] = data[field]

    if not updates:
        conn.close()
        return jsonify({'error': '수정할 필드가 없습니다.'}), 400

    # UPDATE 쿼리 생성
    set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [item_id, project_id]

    cursor.execute(f'''
        UPDATE {table}
        SET {set_clause}
        WHERE id = ? AND project_id = ?
    ''', values)
    conn.commit()
    conn.close()

    return jsonify({'message': '수정 완료'}), 200
