from flask import Flask, render_template, url_for, flash, redirect, request

from flask_nav import Nav
from flask_nav.elements import Navbar, View

from flask_bootstrap import Bootstrap

from dress.config import configure_app
from dress.data.models import db, Host, Status

from concurrent.futures import ThreadPoolExecutor

def create_app():
    app = Flask(__name__)

    # load config
    configure_app(app)
    db.init_app(app)

    # create task executor
    executor = ThreadPoolExecutor(app.config['TASK_POOL_SIZE'])

    # Bootstrap flask-bootstrap
    Bootstrap(app)

    # Navbar flask-nav
    topbar = Navbar('',
            View('Host', 'host'),
            View('Clone', 'task_clone_site_form'),
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
        status = Status.query.all()

        return render_template('host_form.html', host=host, status=status)

    @app.route('/host/delete/<host_id>')
    def host_delete(host_id):
        delete_host = Host.query.filter_by(id=host_id).first()
        delete_host.delete()

        flash('Host #%s %s deleted.' % (delete_host.id, delete_host.name()))

        return redirect(url_for('host'))

    @app.route('/host/update/<host_id>', methods=['POST'])
    def host_update(host_id):
        update_host = Host.query.filter_by(id=host_id).first()

        id = host_id
        ip = request.form['host_ip']
        port = request.form['host_port']
        domain = request.form['host_domain']
        pwd = request.form['host_pwd']
        db_pwd = request.form['host_db_pwd']
        memo = request.form['host_memo']
        status = request.form['host_status']

        update_host.update(ip, port, domain, pwd, db_pwd, memo, status)

        flash('Host #%s "%s" updated.' % (update_host.id, update_host.name()))

        return redirect(url_for('host'))

    @app.route('/host/add', methods=['POST'])
    def host_add():
        ip = request.form['host_ip']
        port = request.form['host_port']
        domain = request.form['host_domain']
        pwd = request.form['host_pwd']
        db_pwd = request.form['host_db_pwd']
        memo = request.form['host_memo']
        status = request.form['host_status']

        new_host = Host(ip, port, domain, pwd, db_pwd, memo, status)
        new_host = new_host.create()

        flash('Host #%s "%s" added.' % (new_host.id, new_host.name()))

        return redirect(url_for('host'))

    # Tasks

    # clone site task
    @app.route('/task/clone_site/form')
    def task_clone_site_form():
        hosts = Host.query.all()

        return render_template('task_clone_site_form.html', hosts=hosts)

    # clone site task
    @app.route('/task/clone_site', methods=['POST'])
    def task_clone_site():
        app.logger.debug('site_type: %s' % (request.form['site_type']))
        app.logger.debug('source_host_id: %s' % (request.form['source_host_id']))
        app.logger.debug('target_host_id: %s' % (request.form['target_host_id']))

        site_type = request.form['site_type'] or 'cscart' # defautl value: cscart
        source_host_id = request.form['source_host_id']
        target_host_id = request.form['target_host_id']

        source_host = Host.query.filter_by(id=source_host_id).first()
        target_host = Host.query.filter_by(id=target_host_id).first()

        if not isinstance(source_host, Host):
            flash("Source Host Not Found!")
            return redirect(url_for('/task/clone_site/form'))
        if not isinstance(target_host, Host):
            flash("Target Host Not Found!")
            return redirect(url_for('/task/clone_site/form'))

        # log "source %s, target %s!" % (source_host.name(), target_host.name())
        executor.submit(task_clone_site_exec, source_host, target_host, site_type)

        flash("Clone Task Is Running In Background. Please Wait...")

        return redirect(url_for('task_clone_site_form'))

    def task_clone_site_exec(source_host: Host, target_host: Host, site_type):
        from dress.tasks.tasks import CloneSiteTask
        task = CloneSiteTask(source_host, target_host, site_type)
        task.run()

    # test
    @app.route('/test_flash')
    def test_flash():
        flash('This is flash message')
        return redirect(url_for('index'))

    @app.route('/test')
    def test_task():
        executor.submit(some_long_task1)
        executor.submit(some_long_task2, 'hello', 123)
        return 'launched!'

    def some_long_task1():
        from time import sleep
        print("Task #1 started!")
        sleep(10)
        print("Task #1 is done!")

    def some_long_task2(arg1, arg2):
        from time import sleep
        print("Task #2 started with args %s %s!" % (arg1, arg2))
        sleep(5)
        print("Task #2 is done!")

    return app

app = create_app()
