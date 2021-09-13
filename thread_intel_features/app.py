import os

from thread_intel_features.setup import setup_app

app = setup_app()

if __name__ == '__main__':
    try:
        PORT = int(os.environ.get('PORT', 3000))
    except:
        PORT = 3000

    try:
        DEBUG = bool(os.environ.get('DEBUG', True))
    except:
        DEBUG = True

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
