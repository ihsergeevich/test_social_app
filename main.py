from aiohttp import web

from app.app import create_app

app = create_app()

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8000)
