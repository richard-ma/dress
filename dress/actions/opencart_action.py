from dress.vendor.workflow import *
from dress.helper import *


class OpencartConfigAction(Action):
    def run(self, *data):
        data = data[0]
        data.append(
            command_sed_helper("define('DB_DATABASE', '.*');",
                               "define('DB_DATABASE', '%s');" %
                               (self.params['target_database_name']),
                               "/home/wwwroot/%s/config.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper("define('DB_USERNAME', '.*');",
                               "define('DB_USERNAME', '%s');" %
                               (self.params['target_database_user_name']),
                               "/home/wwwroot/%s/config.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper("define('DB_PASSWORD', '.*');",
                               "define('DB_PASSWORD', '%s');" %
                               (self.params['target_database_password']),
                               "/home/wwwroot/%s/config.php" %
                               (self.params['target_domain'])))
        data.append(
            command_sed_helper(
                self.params['source_domain'],
                self.params['target_domain'],
                "/home/wwwroot/%s/config.php" %
                (self.params['target_domain']),
                ignore_case=True))
        return data
