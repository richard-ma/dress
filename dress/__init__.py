import os
from flask import Flask, render_template, url_for, flash, redirect, request

from flask_nav import Nav
from flask_nav.elements import Navbar, View

from flask_bootstrap import Bootstrap

from dress.config import configure_app
from dress.data.models import db
from dress.data.models import Host

def create_app():
    app = Flask(__name__)

    # load config
    configure_app(app)
    db.init_app(app)

    # flask-bootstrap
    Bootstrap(app)

    # flask-nav
    topbar = Navbar('',
            View('Host', 'host'),
            View('Move', 'move'),
    )
    nav = Nav()
    nav.register_element('top', topbar)
    nav.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('host'))

    # host operation
    @app.route('/host')
    def host():
        hosts = Host.query.all()

        return render_template('host.html', hosts=hosts)

    @app.route('/host/form/')
    @app.route('/host/form/<host_id>')
    def host_form(host_id=None):
        host = None
        if host_id != None:
            host = Host.query.filter_by(id=host_id).first()

        return render_template('host_form.html', host=host)

    @app.route('/host/delete/<host_id>')
    def host_delete(host_id):
        delete_host = Host.query.filter_by(id=host_id).first()
        db.session.delete(delete_host)
        db.session.commit()

        flash('Host #%s %s deleted.' % (delete_host.id, delete_host.name))

        return redirect(url_for('host'))

    @app.route('/host/update/<host_id>', methods=['POST'])
    def host_update(host_id):
        update_host = Host.query.filter_by(id=host_id).first()

        update_host.id = host_id
        update_host.name = request.form['host_name']
        update_host.ip = request.form['host_ip']
        update_host.port = request.form['host_port']
        update_host.pwd = request.form['host_pwd']
        update_host.domain = request.form['host_domain']
        update_host.db_name = request.form['host_db_name']
        update_host.db_pwd = request.form['host_db_pwd']

        db.session.commit()

        flash('Host #%s "%s" updated.' % (update_host.id, update_host.name))

        return redirect(url_for('host'))

    @app.route('/host/add', methods=['POST'])
    def host_add():
        new_host = Host()

        new_host.name = request.form['host_name']
        new_host.ip = request.form['host_ip']
        new_host.port = request.form['host_port']
        new_host.pwd = request.form['host_pwd']
        new_host.domain = request.form['host_domain']
        new_host.db_name = request.form['host_db_name']
        new_host.db_pwd = request.form['host_db_pwd']

        db.session.add(new_host)
        db.session.commit()

        flash('Host #%s "%s" added.' % (new_host.id, new_host.name))

        return redirect(url_for('host'))

    # move operation
    @app.route('/move')
    def move():
        return render_template('move.html')

    # test
    @app.route('/test_flash')
    def test_flash():
        flash('This is flash message')
        return redirect(url_for('index'))

    return app
