from dress.vendor.workflow import *
from dress.helper import *
import paramiko


class SshAction(Action):
    def __init__(**kwargs):
        super(**kwargs)
        self.client = paramiko.SSHClient()
        # ignore ssh host key to .ssh/know_hosts
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
            self.params['ssh_ip'],
            port=self.params['ssh_port'],
            username=self.params['ssh_username'],
            password=self.params['ssh_password'])

    def close(self):
        self.client.close()

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        # log command response

    def run(self, *data):
        commands = data[0]
        self.connect()
        try:
            self.connect()
            for command in commands:
                # log command response
                self.exec_command(command)
        except paramiko.SSHException as e:
            # log command response
            pass
        finally:
            self.close()
        return commands
