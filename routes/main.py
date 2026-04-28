"""
메인 페이지 라우트
"""

from flask import Blueprint, render_template
from database.init_db import get_connection

main_bp = Blueprint('main', __name__)

# 단가 유형별 정보
UNIT_TYPES = {
    'composite': {'title': '일위대가 목록표', 'table': 'unit_cost_composite'},
    'standard': {'title': '품셈단가 목록표', 'table': 'unit_cost_standard'},
    'market': {'title': '표준시장단가 목록표', 'table': 'unit_cost_market'},
    'quote': {'title': '견적단가 목록표', 'table': 'unit_cost_quote'},
}


def get_project(project_id):
    """프로젝트 정보 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    conn.close()
    return project


def get_counts(project_id):
    """각 단가 테이블의 건수 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    counts = {}
    for key, info in UNIT_TYPES.items():
        cursor.execute(f'SELECT COUNT(*) as cnt FROM {info["table"]} WHERE project_id = ?', (project_id,))
        row = cursor.fetchone()
        counts[key] = row['cnt'] if row else 0
    conn.close()
    return counts


@main_bp.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@main_bp.route('/unit-prices/<int:project_id>')
def unit_prices_dashboard(project_id):
    """단가명세표 대시보드 - 4개 카테고리 선택"""
    project = get_project(project_id)
    if not project:
        return render_template('error.html', message='프로젝트를 찾을 수 없습니다.'), 404

    counts = get_counts(project_id)
    return render_template('unit_prices_dashboard.html', project=project, counts=counts)


@main_bp.route('/unit-prices/<int:project_id>/<cost_type>')
def unit_price_list(project_id, cost_type):
    """개별 단가 목록표 (공통 템플릿)"""
    if cost_type not in UNIT_TYPES:
        return render_template('error.html', message='잘못된 단가 유형입니다.'), 404

    project = get_project(project_id)
    if not project:
        return render_template('error.html', message='프로젝트를 찾을 수 없습니다.'), 404

    info = UNIT_TYPES[cost_type]
    return render_template('unit_price_list.html',
                           project=project,
                           cost_type=cost_type,
                           title=info['title'])
