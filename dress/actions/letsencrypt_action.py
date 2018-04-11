from dress.vendor.workflow import *
from dress.helper import *


class LetsencryptAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("rm -rf /etc/letsencrypt/live/%s" %
                    (self.params['target_domain']))  # remove dir
        data.append(
            command_cp_helper(
                self.params['source_password'], self.params['source_user'],
                self.params['source_ip'],
                '/etc/letsencrypt/live/%s/' % (self.params['source_domain']),
                '/etc/letsencrypt/live/%s/' % (self.params['target_domain'])))
        return data
