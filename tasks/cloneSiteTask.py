from task import Task
from dress.data.models import Host, Status

import paramiko

class CloneSiteTask(Task):
    source_host = None
    dest_host = None

    def __init__(self, source_host, dest_host):
        self.source_host = source_host
        self.dest_host = dest_host

    def run(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
                dest_host.ip,
                port=dest_host.port,
                username='root',
                password=dest_host.pwd
        )

        self.copyFiles(ssh)

        ssh.close()

    def copyFiles(self, ssh):
        #stdin, stdout, stderr = ssh.exec_command('command')
        # pull source host site files
        ssh.exec_command(
                'sshpass -p %s scp -o StrictHostKeyChecking=no -p -r root@%s:/home/wwwroot/%s /home/wwwroot/%s' % (
                    source_host.pwd,
                    source_host.ip,
                    source_host.domain,
                    dest_host.domain
                    )
        )
        # pull source host apache config file
        ssh.exec_command(
                'sshpass -p %s scp -o StrictHostKeyChecking=no -p -r root@%s:/usr/local/apache/conf/vhost/%s.conf /usr/local/apache/conf/vhost/%s.conf' % (
                    source_host.pwd,
                    source_host.ip,
                    source_host.domain,
                    dest_host.domain
                    )
        )
        # pull source host nginx config file
        ssh.exec_command(
                'sshpass -p %s scp -o StrictHostKeyChecking=no -p -r root@%s:/usr/local/nginx/conf/vhost/%s.conf /usr/local/nginx/conf/vhost/%s.conf' % (
                    source_host.pwd,
                    source_host.ip,
                    source_host.domain,
                    dest_host.domain
                    )
        )
