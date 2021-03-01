from app import app

if __name__ == '__main__':
    app.run(ssl_context=('cert/cert.pem', 'cert/key.pem'), port=8000, use_reloader=False)
