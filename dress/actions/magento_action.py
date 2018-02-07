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
            command_sed_helper("\$config\['db_name'\] = '.*';",
                               "\$config\['db_name'\] = '%s';" %
                               (self.params['target_database_name']),
                               "/home/wwwroot/%s/config.local.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper("\$config\['db_user'\] = '.*';",
                               "\$config\['db_user'\] = '%s';" %
                               (self.params['target_database_user_name']),
                               "/home/wwwroot/%s/config.local.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper("\$config\['db_password'\] = '.*';",
                               "\$config\['db_password'\] = '%s';" %
                               (self.params['target_database_password']),
                               "/home/wwwroot/%s/config.local.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper(
                self.params['source_domain'],
                self.params['target_domain'],
                "/home/wwwroot/%s/config.local.php" %
                (self.params['target_domain']),
                ignore_case=True))
        return data
