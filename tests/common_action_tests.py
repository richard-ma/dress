import unittest
import dress

from dress.actions import *

class CommonActionTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        action = InitAction()
        data = action.run(list())

        self.assertEqual(2, len(data))
        #self.assertTrue("screen" in data[0])
        self.assertTrue("yum install -y epel-release" in data[0])
        self.assertTrue("yum install -y sshpass" in data[1])

    def test_copy_site(self):
        action = CopySiteAction(
                source_password='source_password',
                source_ip='source_ip',
                source_user='source_user',
                source_domain='source_domain',
                target_domain='target_domain',
                )
        data = action.run(list())

        self.assertEqual(3, len(data))
        self.assertTrue("rm -rf /home/wwwroot/target_domain" in data[0])
        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" source_user@source_ip:/home/wwwroot/source_domain/ /home/wwwroot/target_domain" in data[1])
        self.assertTrue("chown -R www:www /home/wwwroot/target_domain" in data[2])

    def test_apache_config(self):
        action = ApacheConfigAction(
                source_password='source_password',
                source_ip='source_ip',
                source_user='source_user',
                source_domain='source_domain',
                target_domain='target_domain')
        data = action.run(list())

        self.assertEqual(3, len(data))
        self.assertTrue("rm -rf /usr/local/apache/conf/vhost/target_domain.conf" in data[0])
        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" source_user@source_ip:/usr/local/apache/conf/vhost/source_domain.conf /usr/local/apache/conf/vhost/target_domain.conf" in data[1])
        self.assertTrue("sed -i \"s/source_domain/target_domain/g\" /usr/local/apache/conf/vhost/target_domain.conf" in data[2])

    def test_nginx_config(self):
        action = NginxConfigAction(
                source_password='source_password',
                source_ip='source_ip',
                source_user='source_user',
                source_domain='source_domain',
                target_domain='target_domain')
        data = action.run(list())

        self.assertEqual(3, len(data))
        self.assertTrue("rm -rf /usr/local/nginx/conf/vhost/target_domain.conf" in data[0])
        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" source_user@source_ip:/usr/local/nginx/conf/vhost/source_domain.conf /usr/local/nginx/conf/vhost/target_domain.conf" in data[1])
        self.assertTrue("sed -i \"s/source_domain/target_domain/g\" /usr/local/nginx/conf/vhost/target_domain.conf" in data[2])

    def test_mysql_create_user(self):
        action = MysqlCreateUserAction(
                database_root_password='database_root_password',
                database_user_name='database_user_name',
                database_password='database_password')
        data = action.run(list())

        self.assertEqual(3, len(data))
        self.assertTrue("mysql -u root -p\'database_root_password\' -e \"DROP USER 'database_user_name'@'localhost';\"" in data[0])
        # mysql version >= 5.7
        #self.assertTrue("mysql -u root -p\'database_root_password\' -e \"DROP USER IF EXISTS 'database_user_name'@'localhost';\"" in data[0])
        self.assertTrue("mysql -u root -p\'database_root_password\' -e \"CREATE USER 'database_user_name'@'localhost' IDENTIFIED BY 'database_password';\"" in data[1])
        self.assertTrue("mysql -u root -p\'database_root_password\' -e \"GRANT USAGE ON * . * TO 'database_user_name'@'localhost' IDENTIFIED BY 'database_password' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;\"" in data[2])

    def test_mysql_create_database(self):
        action = MysqlCreateDatabaseAction(
                database_root_password='database_root_password',
                database_user_name='database_user_name',
                database_name='database_name')
        data = action.run(list())

        self.assertEqual(3, len(data))
        self.assertTrue("mysql -u root -p\'database_root_password\' -e \"DROP DATABASE IF EXISTS \`database_name\`;\"" in data[0])
        self.assertTrue("mysql -u root -p\'database_root_password\' -e \"CREATE DATABASE \`database_name\`;\"" in data[1])
        self.assertTrue("mysql -u root -p\'database_root_password\' -e \"GRANT ALL PRIVILEGES ON \`database_name\` . * TO 'database_user_name'@'localhost';\"" in data[2])

    def test_mysql_import_data(self):
        action = MysqlImportDataAction(
                database_root_password='database_root_password',
                database_name='database_name',
                source_domain='source_domain',
                target_domain='target_domain',
                data_file_name='data_file_name')
        data = action.run(list())

        self.assertEqual(2, len(data))
        self.assertTrue("sed -i \"s/source_domain/target_domain/Ig\" data_file_name" in data[0])
        self.assertTrue("mysql -u root -p\'database_root_password\' database_name < data_file_name" in data[1])

    def test_restart_lnmp(self):
        action = LnmpRestartAction()
        data = action.run(list())

        self.assertEqual(1, len(data))
        self.assertTrue('lnmp restart' in data[0])

if __name__ == '__main__':
    unittest.main()
