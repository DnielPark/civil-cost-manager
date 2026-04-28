"""
Civil Cost Manager - 설정 파일
환경별 설정 관리 (개발/운영)
"""

import os
from pathlib import Path

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent


class Config:
    """기본 설정"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-later'

    # 데이터베이스
    DATABASE_PATH = str(BASE_DIR / 'civil_cost.db')

    # 서버
    HOST = '127.0.0.1'
    PORT = 8080

    # 업로드 (2주차에 사용 예정)
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}


class DevelopmentConfig(Config):
    """개발 환경"""
    DEBUG = True


class ProductionConfig(Config):
    """운영 환경"""
    DEBUG = False


# 환경별 설정 선택
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
