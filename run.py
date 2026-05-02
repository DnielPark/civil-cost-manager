import sys
sys.path.insert(0, '.')
from app import app
from config import DevelopmentConfig

if __name__ == '__main__':
    app.run(host=DevelopmentConfig.HOST, port=DevelopmentConfig.PORT, debug=DevelopmentConfig.DEBUG)
