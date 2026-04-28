"""
API 라우트 - JSON 데이터 제공
"""

from flask import Blueprint, jsonify, request
from database.init_db import get_connection

api_bp = Blueprint('api', __name__)

# 단가 유형별 테이블 매핑
UNIT_TABLES = {
    'composite': 'unit_cost_composite',
    'standard': 'unit_cost_standard',
    'market': 'unit_cost_market',
    'quote': 'unit_cost_quote',
}


@api_bp.route('/projects', methods=['GET'])
def list_projects():
    """프로젝트 목록 API"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(projects)


@api_bp.route('/projects', methods=['POST'])
def create_project():
    """프로젝트 생성 API"""
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (name, location) VALUES (?, ?)',
                   (data['name'], data.get('location')))
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': project_id, 'message': '생성 완료'}), 201


@api_bp.route('/unit-prices/<int:project_id>/<table_type>', methods=['GET'])
def get_unit_prices(project_id, table_type):
    """단가명세표 조회 API"""
    if table_type not in UNIT_TABLES:
        return jsonify({'error': 'Invalid table type'}), 400

    table = UNIT_TABLES[table_type]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE project_id = ? ORDER BY id', (project_id,))
    rows = cursor.fetchall()
    conn.close()

    prices = []
    for row in rows:
        prices.append({
            'id': row['id'],
            'work_name': row['work_name'],
            'spec': row['spec'],
            'unit': row['unit'],
            'unit_quantity': row['unit_quantity'],
            'material_cost': row['material_cost'],
            'labor_cost': row['labor_cost'],
            'expense_cost': row['expense_cost'],
            'note': row['note'],
        })

    return jsonify(prices)


@api_bp.route('/unit-prices/<int:project_id>', methods=['GET'])
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
