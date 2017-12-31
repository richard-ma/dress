from dress import app

from dress.data.models import Host, Status
import dress.utils.executor as executor
import dress.utils.generator as generator

class Command(object):
    def __init__(self, command_pool: list):
        self.command_pool = command_pool

    def generate(self):
        pass

    def _command_pool_append(self, command):
        self.command_pool.append(command)
        app.logger.debug("[APPEND] %s" % (command))

        return self

    def cp(self, source_ip, source_path, target_path, source_user='root', source_password=''):
        command = "sshpass -p \'%s\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" %s@%s:%s %s" % (
                source_password,
                source_user,
                source_ip,
                source_path,
                target_path)

        return self._command_pool_append(command)

    def sed(self, source, target, filename):
        command = "sed -i \"s/%s/%s/g\" %s" % (
            source,
            target,
            filename)

        return self._command_pool_append(command)

    def sql(self, sql):
        command = "mysql -u root -e \"%s\"" % (sql.replace('`', '\\`')) # fix #1: 将sql语句换为双引号，转义`字符

        return self._command_pool_append(command)

    def command(self, command):

        return self._command_pool_append(command)

# common command
class CommonCommand(Command):
    def init(self):
        self.command(
                "yum install -y epel-release"
        ).command(
                "yum install -y sshpass"
        )

        return self

    def copy_site(self, source_host: Host, target_host: Host):
        self.cp( # copy site files
                source_ip=source_host.ip,
                source_user='root',
                source_password=source_host.pwd,
                source_path="/home/wwwroot/%s" % (source_host.domain),
                target_path="/home/wwwroot/%s" % (target_host.domain))

        return self

    def apache_config(self, source_host: Host, target_host: Host):
        self.cp( # copy config file
                source_ip=source_host.ip,
                source_user='root',
                source_password=source_host.pwd,
                source_path="/usr/local/apache/conf/vhost/%s.conf" % (source_host.domain),
                target_path="/usr/local/apache/conf/vhost/%s.conf" % (target_host.domain)
        ).sed( # replace domain
                source_host.domain,
                target_host.domain,
                "/usr/local/apache/conf/vhost/%s.conf" % (target_host.domain))

        return self

    def nginx_config(self, source_host: Host, target_host: Host):
        self.cp( # copy config file
                source_ip=source_host.ip,
                source_user='root',
                source_password=source_host.pwd,
                source_path="/usr/local/nginx/conf/vhost/%s.conf" % (source_host.domain),
                target_path="/usr/local/nginx/conf/vhost/%s.conf" % (target_host.domain)
        ).sed( # replace domain
                source_host.domain,
                target_host.domain,
                "/usr/local/nginx/conf/vhost/%s.conf" % (target_host.domain))

        return self

    def mysql_create_user(self, user_name, user_password):
        self.sql( # create user
                "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';" % (
                user_name,
                user_password)
        ).sql( # grant privilige
                "GRANT USAGE ON * . * TO '%s'@'localhost' IDENTIFIED BY '%s' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;" % (
                user_name,
                user_password))

        return self

    def mysql_create_database(self, database_name, user_name):
        self.sql( # create database
                "CREATE DATABASE `%s`;" % (database_name)
        ).sql( # grant privilige
                "GRANT ALL PRIVILEGES ON `%s` . * TO '%s'@'localhost';" % (
                database_name,
                user_name))

        return self

    def mysql_import_data(self, source_host: Host, target_host: Host):
        filename = "/home/wwwroot/%s/dacscartb.sql" % (
                target_host.domain
        )
        database_name = target_host.domain

        self.sed(source_host.domain,
                target_host.domain,
                filename
        ).command("mysql -u root %s < %s" % (
            database_name,
            filename)
        )

        return self

    def restart_lnmp(self):
        self.command('lnmp restart')

        return self

class CscartCommand(Command):
    def clear_cache(self, target_host: Host):
        self.command("rm -rf /home/wwwroot/%s/var/cache/*" % (target_host.domain))

        return self

    def cscart_config(self, source_host: Host, target_host: Host, database_password):
        self.sed(
                "\$config\['db_name'\] = '.*';",
                "\$config\['db_name'\] = '%s';" % (target_host.domain),
                "/home/wwwroot/%s/config.local.php" % (target_host.domain)
        ).sed(
                "\$config\['db_user'\] = '.*';",
                "\$config\['db_user'\] = '%s';" % (target_host.domain),
                "/home/wwwroot/%s/config.local.php" % (target_host.domain)
        ).sed(
                "\$config\['db_password'\] = '.*';",
                "\$config\['db_password'\] = '%s';" % (database_password),
                "/home/wwwroot/%s/config.local.php" % (target_host.domain)
        ).sed(
                source_host.domain,
                target_host.domain,
                "/home/wwwroot/%s/config.local.php" % (target_host.domain)
        )

        return self

# Tasks
class Task(object):
    def run(self):
        pass

class DelayTask(Task):
    def run(self):
        from time import sleep
        app.logger.debug("Timer start")
        for i in range(10):
            app.logger.debug("Timer %d" % (i))
            sleep(1)

# CloneSiteTask
class CloneSiteTask(Task):
    def __init__(self, source_host, target_host, site_type):
        self.site_type = site_type
        self.source_host = source_host
        self.target_host = target_host

        self.target_ssh = executor.SSHExecutor(
                target_host.ip,
                # TODO: add default value to host class
                port = 22, #port = target_host.port,
                username = 'root', #username = target_host.username,
                password = target_host.pwd)

    def run(self):
        app.logger.debug("%s is running." % (self.__class__.__name__))

        site_database_user_name = self.target_host.domain
        site_database_name = self.target_host.domain
        site_database_password = generator.PasswordGenerator.generat(32)

        command_pool = list()

        command = CommonCommand(command_pool)

        app.logger.debug("Appending commands.")
        # prepare environment
        command.init()
        command.copy_site(self.source_host, self.target_host)
        command.apache_config(self.source_host, self.target_host)
        command.nginx_config(self.source_host, self.target_host)
        command.mysql_create_user(site_database_user_name, site_database_password)
        command.mysql_create_database(site_database_name, site_database_user_name)
        command.mysql_import_data(self.source_host, self.target_host)

        if self.site_type == 'cscart':
            # update cscart config
            app.logger.debug('cscart mode')
            cscart_command = CscartCommand(command_pool)
            cscart_command.cscart_config(self.source_host, self.target_host, site_database_password)
            cscart_command.clear_cache(self.target_host)
        elif self.site_type == 'magento':
            app.logger.debug('magento mode')
        elif self.site_type == 'opencart':
            app.logger.debug('opencart mode')
        else:
            app.logger.debug('error mode')

        # restart services
        command.restart_lnmp()

        app.logger.debug("Exectuing commands.")
        self.target_ssh.connect()
        self.target_ssh.exec(command_pool)
        self.target_ssh.close()

        # update host status
        app.logger.debug("Updating host status.")
        self.target_host.updateStatus(Status.BUSINESS)
