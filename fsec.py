from fsec import create_app

if __name__ == '__main__':
    # manager.run()
    app = create_app()
    app.run(host='0.0.0.0', port=8000)

