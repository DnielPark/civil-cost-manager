import sys
sys.path.insert(0, '.')
from app import app

if __name__ == '__main__':
    import os
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    app.run(host='127.0.0.1', port=5000, debug=False)
