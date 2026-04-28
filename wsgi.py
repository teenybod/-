"""
WSGI 入口文件，供 Gunicorn / 宝塔 Python 项目管理器使用
启动命令：gunicorn -w 1 -b 127.0.0.1:8000 wsgi:app
"""
from app import app

if __name__ == "__main__":
    app.run()
