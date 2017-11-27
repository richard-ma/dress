from flask import Flask
from flask import render_template

app = Flask(__name__)

# flask-bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(app)

# flask-nav
from flask_nav import Nav
from flask_nav.elements import Navbar, View
topbar = Navbar('',
        View('Home', 'index'),
        View('Your Account', 'hello'),
)
nav = Nav()
nav.register_element('top', topbar)
nav.init_app(app)

@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/hello')
def hello():
    return 'hello'
