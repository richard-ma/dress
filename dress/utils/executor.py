from dress import app

class Executor(object):
    def __init__(self):
        pass

    def exec_command(self, command):
        pass

    def exec(self, commands):
        pass

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

    def exec(self, commands):
        try:
            self.connect()
            for command in commands:
                app.logger.debug("[EXECUTING] " % (command))
                self.exec_command(command)
        except paramiko.SSHException as e:
            app.logger.error("[ERROR] " + command)
            app.logger.error(e.message)
        finally:
            self.close()

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        print(stdout.readlines())
        print(stderr.readlines())
