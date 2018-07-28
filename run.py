import os
os.environ["DATABASE_URL"] = 'mysql://root:password@localhost/market'
os.environ["APP_SETTINGS"] = 'development'

from app.views import app

if __name__ == '__main__':
    app.run()
