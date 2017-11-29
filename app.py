from flask import render_template
from flask_pluginengine import PluginFlask, PluginEngine

# flask plugin engine
app = PluginFlask(__name__)

app.config['PLUGINENGINE_NAMESPACE'] = 'dress'
app.config['PLUGINENGINE_PLUGINS'] = ['dress_plugin']

plugin_engine = PluginEngine(app=app)
plugin_engine.load_plugins(app)
active_plugins = plugin_engine.get_active_plugins(app=app).values()

for plugin in active_plugins:
    with plugin.plugin_context():
        app.register_blueprint(plugin.get_blueprint())

# flask-bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(app)

# flask-nav
from flask_nav import Nav
from flask_nav.elements import Navbar, View
topbar = Navbar('',
        View('Home', 'index'),
)
nav = Nav()
nav.register_element('top', topbar)
nav.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', plugins=active_plugins)

if __name__ == '__main__':
    app.run()
