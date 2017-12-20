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

import paramiko

class CloneSiteTask(Task):
    __taskname__ = 'Clone Site Task'

    source_host = None
    dest_host = None

    def __init__(self, source_host, dest_host):
        self.source_host = source_host
        self.dest_host = dest_host

    def run(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
                self.dest_host.ip,
                port=self.dest_host.port,
                username='root',
                password=self.dest_host.pwd
        )

        #self.copyFiles(ssh)
        self.restore(ssh)
        self.release(ssh)

        ssh.close()

    def copyFiles(self, ssh):
        #stdin, stdout, stderr = ssh.exec_command('command')
        # pull source host site files
        stdin, stdout, stderr = ssh.exec_command(
                'sshpass -p %s scp -o StrictHostKeyChecking=no -p -r root@%s:/home/wwwroot/%s /home/wwwroot/%s' % (
                    self.source_host.pwd,
                    self.source_host.ip,
                    self.source_host.domain,
                    self.dest_host.domain
                    )
        )
        self.message(command + " - " + stdout + ":" + stderr)
        # pull source host apache config file
        stdin, stdout, stderr = ssh.exec_command(
                'sshpass -p %s scp -o StrictHostKeyChecking=no -p root@%s:/usr/local/apache/conf/vhost/%s.conf /usr/local/apache/conf/vhost/%s.conf' % (
                    self.source_host.pwd,
                    self.source_host.ip,
                    self.source_host.domain,
                    self.dest_host.domain
                    )
        )
        self.message(command + " - " + stdout + ":" + stderr)
        # pull source host nginx config file
        stdin, stdout, stderr = ssh.exec_command(
                'sshpass -p %s scp -o StrictHostKeyChecking=no -p root@%s:/usr/local/nginx/conf/vhost/%s.conf /usr/local/nginx/conf/vhost/%s.conf' % (
                    self.source_host.pwd,
                    self.source_host.ip,
                    self.source_host.domain,
                    self.dest_host.domain,
                    )
        )
        self.message(command + " - " + stdout + ":" + stderr)
        # pull source host database sql file

    def restore(self, ssh):
        # create database
        stdin, stdout, stderr = command = "mysql -u root -e 'create database `%s`;'" % (
                    self.dest_host.db_name,
                    )
        ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)

        # replace domain in data
        command = "sed -i \"s/%s/%s/g\" /home/wwwroot/%s/dacscartb.sql" % (
                    self.source_host.domain,
                    self.dest_host.domain,
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)

        # import data
        command = "mysql -u root %s < /home/wwwroot/%s/dacscartb.sql" % (
                    self.dest_host.db_name,
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)

    def release(self, ssh):
        # release cscart config file
        command = "sed -i \"s/\$config\['db_name'] = '.*';/\$config\['db_name'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    self.dest_host.db_name,
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)
        command = "sed -i \"s/\$config\['db_user'] = '.*';/\$config\['db_user'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    'root',
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)
        command = "sed -i \"s/\$config\['db_password'] = '.*';/\$config\['db_password'\] = '%s';/g\" /home/wwwroot/%s/config.local.php" % (
                    self.dest_host.db_pwd,
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)

        # release apache config file
        command = "sed -i 's/%s/%s/g' /usr/local/apache/conf/vhost/%s.conf" % (
                    self.source_host.domain,
                    self.dest_host.domain,
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)

        # release nginx config file
        command = "sed -i 's/%s/%s/g' /usr/local/nginx/conf/vhost/%s.conf" % (
                    self.source_host.domain,
                    self.dest_host.domain,
                    self.dest_host.domain,
                    )
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)

        # restart lnmp
        command = "lnmp restart"
        stdin, stdout, stderr = ssh.exec_command(command)
        self.message(command + " - " + stdout + ":" + stderr)
