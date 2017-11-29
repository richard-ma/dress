from flask import render_template
from flask_pluginengine import Plugin, PluginBlueprint, current_plugin

plugin_blueprint = PluginBlueprint('dress', __name__)

@plugin_blueprint.route('/move')
def move_plugin():
    return render_template('dress_plugin:index.html', plugin=current_plugin)

class DressPlugin(Plugin):
    def get_blueprint(self):
        return plugin_blueprint
