"""
메인 페이지 라우트
"""

from flask import Blueprint, render_template
from database.init_db import get_connection

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@main_bp.route('/projects')
def projects():
    """프로젝트 목록 페이지"""
    return render_template('projects.html')


@main_bp.route('/unit-prices/<int:project_id>')
def unit_prices_dashboard(project_id):
    """단가명세표 대시보드"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    conn.close()

    if not project:
        return render_template('error.html', message='프로젝트를 찾을 수 없습니다.'), 404

    return render_template('unit_prices_dashboard.html', project=project)
