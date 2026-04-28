"""
메인 페이지 라우트
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@main_bp.route('/projects')
def projects():
    """프로젝트 목록 페이지"""
    return render_template('projects.html')


@main_bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """프로젝트 상세 페이지"""
    return render_template('project_detail.html', project_id=project_id)


@main_bp.route('/unit-prices')
def unit_prices():
    """단가명세서 페이지"""
    return render_template('unit_prices.html')
