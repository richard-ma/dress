class Executor(object):
    def __init__(self):
        pass

    def exec_command(self, command):
        pass

    def exec(self, commands):
        for command in commands:
            self.exec_command(command)

# SSH Executor
import paramiko

class SSHExecutor(Executor):
    def __init__(self, ip, port=22, username='root', password=''):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        self.client = paramiko.SSHClient()
        # ignore ssh host key to .ssh/know_hosts
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
                self.ip,
                port = self.port,
                username = self.username,
                password = self.password
                )

    def close(self):
        self.client.close()

    def exec_command(self, command):
        self.client.exec_command(command)
