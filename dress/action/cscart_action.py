from dress.vendor.workflow import *
from dress.helper import *


class CscartClearCacheAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("rm -rf /home/wwwroot/%s/var/cache/*" %
                    (self.params['target_domain']))
        return data


class CscartConfigAction(Action):
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


class CscartOrderStartIdAction(Action):
    def run(self, *data):
        data = data[0]
        data.append(
            command_mysql_helper(
                self.params['target_database_root_password'],
                "UPDATE `%s`.`%ssettings_objects` SET `value` = '%s' WHERE `%ssettings_objects`.`object_id` = 62;"
                % (self.params['target_database_name'], self.params['table_prefix'],
                   self.params['order_start_id'],
                   self.params['table_prefix'])))
        return data


class CscartSmtpSettingAction(Action):
    def run(self, *data):
        data = data[0]
        data.append(
            command_mysql_helper(
                self.params['target_database_root_password'],
                "UPDATE `%s`.`%ssettings_objects` SET `value` = '%s' WHERE `%ssettings_objects`.`object_id` = 109;"
                % (self.params['target_database_name'], self.params['table_prefix'],
                   self.params['smtp_host'], self.params['table_prefix'])))
        data.append(
            command_mysql_helper(
                self.params['target_database_root_password'],
                "UPDATE `%s`.`%ssettings_objects` SET `value` = '%s' WHERE `%ssettings_objects`.`object_id` = 111;"
                % (self.params['target_database_name'], self.params['table_prefix'],
                   self.params['smtp_user_name'],
                   self.params['table_prefix'])))
        data.append(
            command_mysql_helper(
                self.params['target_database_root_password'],
                "UPDATE `%s`.`%ssettings_objects` SET `value` = '%s' WHERE `%ssettings_objects`.`object_id` = 112;"
                % (self.params['target_database_name'], self.params['table_prefix'],
                   self.params['smtp_user_password'],
                   self.params['table_prefix'])))
        return data
