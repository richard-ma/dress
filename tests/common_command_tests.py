import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from manager import seed

from dress.tasks.tasks import CommonCommand

class CommonCommandTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

        self.source_host = Host()
        self.source_host.ip = '1.1.1.1'
        self.source_host.port = 10086
        self.source_host.domain = 'source_domain'
        self.source_host.pwd = 'source_password'
        self.source_host.db_pwd = 'source_database_password'

        self.target_host = Host()
        self.target_host.ip = '2.2.2.2'
        self.target_host.port = 10010
        self.target_host.domain = 'target_domain'
        self.target_host.pwd = 'target_password'
        self.target_host.db_pwd = 'target_database_password'

    def tearDown(self):
        pass

    def test_copy_site(self):
        command_pool = list()

        CommonCommand(command_pool).copy_site(self.source_host, self.target_host)

        self.assertEqual(1, len(command_pool))

        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" root@1.1.1.1:/home/wwwroot/source_domain /home/wwwroot/target_domain" in command_pool[0])

    def test_apache_config(self):
        command_pool = list()

        CommonCommand(command_pool).apache_config(self.source_host, self.target_host)

        self.assertEqual(2, len(command_pool))

        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" root@1.1.1.1:/usr/local/apache/conf/vhost/source_domain.conf /usr/local/apache/conf/vhost/target_domain.conf" in command_pool[0])
        self.assertTrue("sed -i \"s/source_domain/target_domain/g\" /usr/local/apache/conf/vhost/target_domain.conf" in command_pool[1])

    def test_nginx_config(self):
        command_pool = list()

        CommonCommand(command_pool).nginx_config(self.source_host, self.target_host)

        self.assertEqual(2, len(command_pool))

        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" root@1.1.1.1:/usr/local/nginx/conf/vhost/source_domain.conf /usr/local/nginx/conf/vhost/target_domain.conf" in command_pool[0])
        self.assertTrue("sed -i \"s/source_domain/target_domain/g\" /usr/local/nginx/conf/vhost/target_domain.conf" in command_pool[1])

    def test_mysql_create_user(self):
        user_name = 'test_user'
        user_password = 'test_password'

        command_pool = list()

        CommonCommand(command_pool).mysql_create_user(user_name, user_password)

        self.assertEqual(2, len(command_pool))

        self.assertTrue("mysql -u root -e \"CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'test_password';\"" in command_pool[0])
        self.assertTrue("mysql -u root -e \"GRANT USAGE ON * . * TO 'test_user'@'localhost' IDENTIFIED BY 'test_password' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;\"" in command_pool[1])

    def test_mysql_create_database(self):
        database_name = 'test_database'
        user_name = 'test_user'

        command_pool = list()

        CommonCommand(command_pool).mysql_create_database(database_name, user_name)

        self.assertEqual(2, len(command_pool))

        self.assertTrue("mysql -u root -e \"CREATE DATABASE \`test_database\`;\"" in command_pool[0])
        self.assertTrue("mysql -u root -e \"GRANT ALL PRIVILEGES ON \`test_database\` . * TO 'test_user'@'localhost';\"" in command_pool[1])

    def test_mysql_import_data(self):
        command_pool = list()

        CommonCommand(command_pool).mysql_import_data(self.source_host, self.target_host)
        self.assertEqual(2, len(command_pool))

        self.assertTrue("sed -i \"s/source_domain/target_domain/g\" /home/wwwroot/target_domain/dacscartb.sql" in command_pool[0])
        self.assertTrue("mysql -u root target_domain < /home/wwwroot/target_domain/dacscartb.sql" in command_pool[1])

    def test_restart_lnmp(self):
        command_pool = list()

        CommonCommand(command_pool).restart_lnmp()

        self.assertEqual(1, len(command_pool))

        self.assertTrue('lnmp restart' in command_pool[0])

if __name__ == '__main__':
    unittest.main()
