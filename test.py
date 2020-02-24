from flask import Flask
from flask import Blueprint

app = Flask(__name__)

web = Blueprint('web', __name__, url_prefix='/ss')


@web.route('book/helloworld')
def helloworld():
    return 'abcdef'
app.register_blueprint(web)

if __name__ == '__main__':
    app.run(port=81, host='0.0.0.0', debug=False)