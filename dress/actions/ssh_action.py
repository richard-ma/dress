from dress.vendor.workflow import *
from dress.helper import *
import paramiko
import time


class SshAction(Action):
    def __init__(self, **kwargs):
        super(SshAction, self).__init__(**kwargs)
        self.client = paramiko.SSHClient()
        # ignore ssh host key to .ssh/know_hosts
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
            self.params['ssh_ip'],
            port=self.params['ssh_port'],
            username=self.params['ssh_username'],
            password=self.params['ssh_password'])
        channel = self.client.invoke_shell()
        channel.settimeout(3600)
        self.channel = channel

    def close(self):
        self.client.close()

    def screen_exec(self, command):
        self.channel.send("{}\n".format(command))
        flag = False
        retVal = ""
        while not flag:
            time.sleep(1)
            try:
                buffByte = self.channel.recv(9999)
                buff = buffByte.decode()
                retVal = retVal + buff
                gotit = buff.find('#')
                if gotit != -1:
                    flag = True
            except:
                flag = True
        return retVal

    # unused
    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        print('output:' + ''.join(stdout.readlines()))
        print('error:' + ''.join(stderr.readlines()))
        # log command response
        return stdin, stdout, stderr

    def run(self, *data):
        data = data[0]
        try:
            self.connect()
            self.screen_exec("screen -S dress -X quit")
            self.screen_exec("screen -S dress")
            for command in data:
                self.screen_exec(command)
        except paramiko.SSHException as e:
            # log command response
            print("error accourd")
        finally:
            self.close()
        return True  # The end of workflow
