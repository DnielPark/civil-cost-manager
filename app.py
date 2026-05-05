"""
Civil Cost Manager - Flask 메인 애플리케이션
토목 공사비 관리 웹 애플리케이션
"""

from flask import Flask, render_template
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

# 라우트 블루프린트 등록
from routes.main import main_bp
from routes.api import api_bp

app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message='페이지를 찾을 수 없습니다.'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', message='서버 오류가 발생했습니다.'), 500

if __name__ == '__main__':
    # DB 스키마 초기화 (테이블 없으면 생성)
    from database.init_db import init_unit_price_db, init_quantity_db, init_projects_table
    init_unit_price_db()
    init_quantity_db()
    init_projects_table()

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
