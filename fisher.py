from app import create_app # 到某个模块下的函数，变量，都可以引用

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=app.config['DEBUG'])