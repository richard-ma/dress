from dress.vendor.workflow import *
from dress.helper import *


class MagentoClearCacheAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("rm -rf /home/wwwroot/%s/var/cache/*" %
                    (self.params['target_domain']))
        data.append("rm -rf /home/wwwroot/%s/var/session/*" %
                    (self.params['target_domain']))
        return data


class MagentoConfigAction(Action):
    def run(self, *data):
        data = data[0]
        data.append(
            command_sed_helper("'dbname' => '.*',",
                               "'dbname' => '%s'," %
                               (self.params['target_database_name']),
                               "/home/wwwroot/%s/app/etc/env.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper("'username' => '.*',",
                               "'username' => '%s'," %
                               (self.params['target_database_user_name']),
                               "/home/wwwroot/%s/app/etc/env.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper("'password' => '.*',",
                               "'password' => '%s'," %
                               (self.params['target_database_password']),
                               "/home/wwwroot/%s/app/etc/env.php" %
                               (self.params['target_domain'])))
        return data
