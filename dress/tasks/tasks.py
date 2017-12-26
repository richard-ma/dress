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
        app.logger.debug("[%s][APPEND] %s" % (self.__class__, command))

        return self

    def scp(self, source_ip, source_path, target_path, source_user='root', source_password=''):
        command = 'sshpass -p \'%s\' scp -o StrictHostKeyChecking=no -p -r %s@%s:%s %s' % (
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
        command = "mysql -u root -e '%s" % (sql)

        return self._command_pool_append(command)

    def command(self, command):

        return self._command_pool_append(command)

# common command
class CommonCommand(Command):
    def copy_site(self, source_host: Host, target_host: Host):
        self.scp( # copy site files
                source_ip=source_host.ip,
                source_user='root',
                source_password=source_host.pwd,
                source_path="/home/wwwroot/%s" % (source_host.domain),
                target_path="/home/wwwroot/%s" % (target_host.domain))

        return self

    def apache_config(self, source_host: Host, target_host: Host):
        self.scp( # copy config file
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
        self.scp( # copy config file
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
                "GRANT USAGE ON * . * TO '%s'@'localhost' IDENTIFIED BY '%s' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;" % (
                user_name,
                user_password))

        return self

    def mysql_create_database(self, database_name, user_name):
        self.sql( # create database
                "create database `%s`;" % (database_name)
        ).sql( # grant privilige
                "GRANT ALL PRIVILEGES ON `%s` . * TO '%s'@'localhost';" % (
                database_name,
                user_name))

        return self

    def restart_lnmp(self):
        self.command('lnmp restart')

        return self

# Tasks
class Task(object):
    def run(self):
        pass

# CloneSiteTask
class CloneSiteTask(Task):
    def __init__(self, source_host, target_host):
        self.source_host = source_host
        self.target_host = target_host

        self.target_ssh = executor.SSHExecutor(
                target_host.ip,
                # TODO: add default value to host class
                port = 22, #port = target_host.port,
                username = 'root', #username = target_host.username,
                password = target_host.pwd)

    def run(self):
        site_database_user_name = self.target_host.domain
        site_database_name = self.target_host.domain
        site_database_password = generator.PasswordGenerator.generat(32)

        command_pool = list()

        command = CommonCommand(command_pool)
        command.copy_site(self.source_host, self.target_host)
        command.apache_config(self.source_host, self.target_host)
        command.nginx_config(self.source_host, self.target_host)
        command.mysql_create_user(site_database_user_name, site_database_password)
        command.mysql_create_database(site_database_name, site_database_user_name)

        print('\r\n'.join(command_pool))
        return

        commands = list()

        # copy files
        command = 'sshpass -p \'%s\' scp -o StrictHostKeyChecking=no -p -r root@%s:/home/wwwroot/%s /home/wwwroot/%s' % (
                self.source_host.pwd,
                self.source_host.ip,
                self.source_host.domain,
                self.target_host.domain)
        commands.append(command)

        command = 'sshpass -p \'%s\' scp -o StrictHostKeyChecking=no -p root@%s:/usr/local/apache/conf/vhost/%s.conf /usr/local/apache/conf/vhost/%s.conf' % (
            self.source_host.pwd,
            self.source_host.ip,
            self.source_host.domain,
            self.target_host.domain)
        commands.append(command)

        command = 'sshpass -p \'%s\' scp -o StrictHostKeyChecking=no -p root@%s:/usr/local/nginx/conf/vhost/%s.conf /usr/local/nginx/conf/vhost/%s.conf' % (
            self.source_host.pwd,
            self.source_host.ip,
            self.source_host.domain,
            self.target_host.domain)
        commands.append(command)

        # restore site
        command = "sed -i \"s/%s/%s/g\" /home/wwwroot/%s/dacscartb.sql" % (
            self.source_host.domain,
            self.target_host.domain,
            self.target_host.domain)
        commands.append(command)

        command = "mysql -u root -e 'CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';'" % (
                self.target_host.domain,
                site_database_password)
        commands.append(command)

        command = "mysql -u root -e 'GRANT USAGE ON * . * TO '%s'@'localhost' IDENTIFIED BY '%s' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;'" % (
                self.target_host.domain,
                site_database_password)
        commands.append(command)

        command = "mysql -u root -e 'create database `%s`;'" % (self.target_host.domain)
        commands.append(command)

        command = "mysql -u root -e 'GRANT ALL PRIVILEGES ON `%s` . * TO '%s'@'localhost';'" % (
                self.target_host.domain,
                self.target_host.domain)
        commands.append(command)

        command = "mysql -u root %s < /home/wwwroot/%s/dacscartb.sql" % (
            self.target_host.domain,
            self.target_host.domain)
        commands.append(command)

        # release site
        command = "sed -i \"s/\$config\['db_name'] = '.*';/\$config\['db_name'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    self.source_host.domain,
                    self.target_host.domain)
        commands.append(command)

        command = "sed -i \"s/\$config\['db_user'] = '.*';/\$config\['db_user'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    'root',
                    self.target_host.domain)
        commands.append(command)

        command = "sed -i \"s/\$config\['db_password'] = '.*';/\$config\['db_password'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    site_database_password,
                    self.target_host.domain)
        commands.append(command)

        command = "sed -i 's/%s/%s/g' /home/wwwroot/%s/config.local.php" % (
                    self.source_host.domain,
                    self.target_host.domain,
                    self.target_host.domain)
        commands.append(command)

        command = "sed -i 's/%s/%s/g' /usr/local/apache/conf/vhost/%s.conf" % (
                    self.source_host.domain,
                    self.target_host.domain,
                    self.target_host.domain)
        commands.append(command)

        command = "sed -i 's/%s/%s/g' /usr/local/nginx/conf/vhost/%s.conf" % (
                    self.source_host.domain,
                    self.target_host.domain,
                    self.target_host.domain)
        commands.append(command)

        command = "rm -rf /home/wwwroot/%s/var/cache/*" % (self.target_host.domain,)
        commands.append(command)

        command = "lnmp restart"
        commands.append(command)

        self.target_ssh.connect()
        self.target_ssh.exec(commands)
        self.target_ssh.close()

        self.target_host.status = Status.query.filter_by(title='Business').first()
