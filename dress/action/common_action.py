from dress.vendor.workflow import *
from dress.helper import *


class InitAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("screen")
        data.append("yum install -y epel-release")
        data.append("yum install -y sshpass")
        return data


class CopySiteAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("rm -rf /home/wwwroot/%s" %
                    (self.params['target_domain']))  # remove dir
        data.append(
            command_cp_helper(
                self.params['source_password'], self.params['source_user'],
                self.params['source_ip'],
                '/home/wwwroot/%s/' % (self.params['source_domain']),
                '/home/wwwroot/%s/' % (self.params['target_domain'])))
        data.append("chown -R www:www /home/wwwroot/%s" %
                    (self.params['target_domain']))
        return data


class ApacheConfigAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("rm -rf /usr/local/apache/conf/vhost/%s.conf" %
                    (self.params['target_domain']))
        data.append(
            command_cp_helper(self.params['source_password'],
                              self.params['source_user'],
                              self.params['source_ip'],
                              "/usr/local/apache/conf/vhost/%s.conf" %
                              (self.params['source_domain']),
                              "/usr/local/apache/conf/vhost/%s.conf" %
                              (self.params['target_domain'])))
        data.append(
            command_sed_helper(self.params['source_domain'],
                               self.params['target_domain'],
                               "/usr/local/apache/conf/vhost/%s.conf" %
                               (self.params['target_domain'])))
        return data


class NginxConfigAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("rm -rf /usr/local/nginx/conf/vhost/%s.conf" %
                    (self.params['target_domain']))
        data.append(
            command_cp_helper(self.params['source_password'],
                              self.params['source_user'],
                              self.params['source_ip'],
                              "/usr/local/nginx/conf/vhost/%s.conf" %
                              (self.params['source_domain']),
                              "/usr/local/nginx/conf/vhost/%s.conf" %
                              (self.params['target_domain'])))
        data.append(
            command_sed_helper(self.params['source_domain'],
                               self.params['target_domain'],
                               "/usr/local/nginx/conf/vhost/%s.conf" %
                               (self.params['target_domain'])))
        return data


class MysqlCreateUserAction(Action):
    def run(self, *data):
        data = data[0]
        # drop user
        data.append(
            command_mysql_helper(self.params['database_root_password'],
                                 "DROP USER IF EXISTS '%s'@'localhost';" %
                                 (self.params['database_user_name'])))
        # create user
        data.append(
            command_mysql_helper(
                self.params['database_root_password'],
                "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';" %
                (self.params['database_user_name'], self.params['database_password'])))
        # grant privilige
        data.append(
            command_mysql_helper(
                self.params['database_root_password'],
                "GRANT USAGE ON * . * TO '%s'@'localhost' IDENTIFIED BY '%s' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;"
                % (self.params['database_user_name'], self.params['database_password'])))
        return data


class MysqlCreateDatabaseAction(Action):
    def run(self, *data):
        data = data[0]
        # drop database
        data.append(
            command_mysql_helper(self.params['database_root_password'],
                                 "DROP DATABASE IF EXISTS `%s`;" %
                                 (self.params['database_name'])))
        # create database
        data.append(
            command_mysql_helper(self.params['database_root_password'],
                                 "CREATE DATABASE `%s`;" %
                                 (self.params['database_name'])))
        # grant privilige
        data.append(
            command_mysql_helper(
                self.params['database_root_password'],
                "GRANT ALL PRIVILEGES ON `%s` . * TO '%s'@'localhost';" %
                (self.params['database_name'], self.params['database_user_name'])))
        return data


class MysqlImportDataAction(Action):
    def run(self, *data):
        data = data[0]
        data.append(
            command_sed_helper(
                self.params['source_domain'],
                self.params['target_domain'],
                "/home/wwwroot/%s/dacscartb.sql" %
                (self.params['target_domain']),
                ignore_case=True))
        data.append("mysql -u root -p\'%s\' %s < %s" %
                    (self.params['database_root_password'],
                     self.params['database_name'],
                     "/home/wwwroot/%s/dacscartb.sql" %
                     (self.params['target_domain'])))
        return data


class LnmpRestartAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("lnmp restart")
        return data
