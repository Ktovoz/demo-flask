from app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app('development')

# 添加代理支持
# 注意：仅在实际使用代理时启用此功能
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 