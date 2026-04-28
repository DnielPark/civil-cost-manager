"""
Civil Cost Manager - Flask 메인 애플리케이션
토목 공사비 관리 웹 애플리케이션
"""

import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

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
    # DB 초기화
    from database.init_db import init_database
    init_database()

    app.run(host='127.0.0.1', port=5000, debug=True)
