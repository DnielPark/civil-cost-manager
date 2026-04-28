import sys
sys.path.insert(0, '.')
from app import app
from config import Config

if __name__ == '__main__':
    import os
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
