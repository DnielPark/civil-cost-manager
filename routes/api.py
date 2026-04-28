"""
API 라우트 - JSON 데이터 제공
"""

from flask import Blueprint, jsonify, request
from database.init_db import get_connection

api_bp = Blueprint('api', __name__)


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
    cursor.execute('''
        INSERT INTO projects (name, location, start_date, end_date, budget, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['name'], data.get('location'), data.get('start_date'),
          data.get('end_date'), data.get('budget', 0), data.get('description')))
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': project_id, 'message': '생성 완료'}), 201


@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """프로젝트 상세 API"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    if not project:
        conn.close()
        return jsonify({'error': 'Not found'}), 404

    cursor.execute('SELECT * FROM cost_items WHERE project_id = ? ORDER BY code', (project_id,))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()

    result = dict(project)
    result['items'] = items
    return jsonify(result)


@api_bp.route('/cost-items', methods=['POST'])
def add_cost_item():
    """공사 항목 추가 API"""
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    total = (data.get('quantity', 0) or 0) * (data.get('unit_price', 0) or 0)
    cursor.execute('''
        INSERT INTO cost_items (project_id, parent_id, code, name, unit, quantity, unit_price, total_price, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['project_id'], data.get('parent_id'), data.get('code'),
          data['name'], data.get('unit'), data.get('quantity', 0),
          data.get('unit_price', 0), total, data.get('note')))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': item_id, 'total_price': total, 'message': '추가 완료'}), 201


@api_bp.route('/unit-prices', methods=['GET'])
def get_unit_prices():
    """단가명세서 조회 API"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM unit_price_list ORDER BY id')
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
            'cost_basis': row['cost_basis'],
            'note': row['note']
        })

    return jsonify(prices)
