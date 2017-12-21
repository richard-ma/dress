class Task(object):
    __taskname__ = 'Task'

    def run(self):
        pass

    def message(self, msg):
        print("%s: %s" % (self.__taskname__, msg))

    @classmethod
    def runMessage(func):
        print("[%s] started!" % (self.__taskname__))
        func()
        print("[%s] is done!" % (self.__taskname__))

# CloneSiteTask
from dress.data.models import Host, Status
import dress.utils.executor as executor

class CloneSiteTask(Task):
    __taskname__ = 'Clone Site Task'

    def __init__(self, source_host, dest_host):
        self.source_host = source_host
        self.dest_host = dest_host

        self.dest_ssh = executor.SSHExecutor(
                dest_host.ip,
                # TODO: add default value to host class
                #port = dest_host.port,
                #username = dest_host.username,
                password = dest_host.password
                )

    def run(self):
        commands = list()

        # copy files
        commmand = 'sshpass -p %s scp -o StrictHostKeyChecking=no -p -r root@%s:/home/wwwroot/%s /home/wwwroot/%s' % (
            self.source_host.pwd,
            self.source_host.ip,
            self.source_host.domain,
            self.dest_host.domain)
        commands.append(command)

        command = 'sshpass -p %s scp -o StrictHostKeyChecking=no -p root@%s:/usr/local/apache/conf/vhost/%s.conf /usr/local/apache/conf/vhost/%s.conf' % (
            self.source_host.pwd,
            self.source_host.ip,
            self.source_host.domain,
            self.dest_host.domain)
        commands.append(command)

        command = 'sshpass -p %s scp -o StrictHostKeyChecking=no -p root@%s:/usr/local/nginx/conf/vhost/%s.conf /usr/local/nginx/conf/vhost/%s.conf' % (
            self.source_host.pwd,
            self.source_host.ip,
            self.source_host.domain,
            self.dest_host.domain)
        commands.append(command)

        # restore site
        command = "sed -i \"s/%s/%s/g\" /home/wwwroot/%s/dacscartb.sql" % (
            self.source_host.domain,
            self.dest_host.domain,
            self.dest_host.domain)
        commands.append(command)

        command = "mysql -u root -e 'create database `%s`;'" % (self.dest_host.db_name)
        commands.append(command)

        command = "mysql -u root %s < /home/wwwroot/%s/dacscartb.sql" % (
            self.dest_host.db_name,
            self.dest_host.domain)
        commands.append(command)

        # release site
        command = "sed -i \"s/\$config\['db_name'] = '.*';/\$config\['db_name'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    self.dest_host.db_name,
                    self.dest_host.domain)
        commands.append(command)

        command = "sed -i \"s/\$config\['db_user'] = '.*';/\$config\['db_user'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    'root',
                    self.dest_host.domain)
        commands.append(command)

        command = "sed -i \"s/\$config\['db_password'] = '.*';/\$config\['db_password'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    self.dest_host.db_pwd,
                    self.dest_host.domain)
        commands.append(command)

        command = "sed -i 's/%s/%s/g' /home/wwwroot/%s/config.local.php" % (
                    self.source_host.domain,
                    self.dest_host.domain,
                    self.dest_host.domain)
        commands.append(command)

        command = "sed -i 's/%s/%s/g' /usr/local/apache/conf/vhost/%s.conf" % (
                    self.source_host.domain,
                    self.dest_host.domain,
                    self.dest_host.domain)
        commands.append(command)

        command = "sed -i 's/%s/%s/g' /usr/local/nginx/conf/vhost/%s.conf" % (
                    self.source_host.domain,
                    self.dest_host.domain,
                    self.dest_host.domain)
        commands.append(command)

        command = "rm -rf /home/wwwroot/%s/var/cache/*" % (self.dest_host.domain,)
        commands.append(command)

        command = "lnmp restart"
        commands.append(command)

        self.dest_ssh.connect()
        self.dest_ssh.exec(commands)
        self.dest_ssh.close()
