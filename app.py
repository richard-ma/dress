from flask import Flask
from flask import render_template

from flask_nav import Nav
from flask_nav.elements import Navbar, View

from flask_bootstrap import Bootstrap

app = Flask(__name__)

# flask plugin engine
#from flask_pluginengine import PluginFlask, PluginEngine
'''
app = PluginFlask(__name__)

app.config['PLUGINENGINE_NAMESPACE'] = 'dress'
app.config['PLUGINENGINE_PLUGINS'] = ['dress_plugin']

plugin_engine = PluginEngine(app=app)
plugin_engine.load_plugins(app)
active_plugins = plugin_engine.get_active_plugins(app=app).values()

for plugin in active_plugins:
    with plugin.plugin_context():
        app.register_blueprint(plugin.get_blueprint())

'''
# flask-bootstrap
Bootstrap(app)

# flask-nav
topbar = Navbar('',
        View('Home', 'index'),
        View('Host', 'host'),
        View('Move', 'move'),
)
nav = Nav()
nav.register_element('top', topbar)
nav.init_app(app)

# flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///host.db'
db = SQLAlchemy(app)

class Host(db.Model):
    __tablename__ = 'host'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ip = db.Column(db.String(32))
    port = db.Column(db.Integer)
    domain = db.Column(db.String(32))
    pwd = db.Column(db.String(32))
    db_name = db.Column(db.String(32))
    db_pwd = db.Column(db.String(32))

@app.route('/')
def index():
    return render_template('index.html')

# host operation
@app.route('/host')
def host():
    hosts = Host.query.all()

    return render_template('host.html', hosts=hosts)

@app.route('/host/add')
def host_add():
    host = Host()
    host.name = 'new host'
    db.session.add(host)
    db.session.commit()

    return 'added'

# move operation
@app.route('/move')
def move():
    return render_template('move.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
