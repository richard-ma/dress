import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from seed import seed_db

from dress.tasks.tasks import CommonCommand

class CommonCommandTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed_db(self.app)

        self.source_host = Host()
        self.source_host.ip = '233.233.233.233'
        self.source_host.port = 10086
        self.source_host.domain = 'source.domain'
        self.source_host.pwd = 'source_password'
        self.source_host.db_pwd = 'source database password'

        self.target_host = Host()
        self.target_host.ip = '222.222.222.222'
        self.target_host.port = 10010
        self.target_host.domain = 'target.domain'
        self.target_host.pwd = 'target_password'
        self.target_host.db_pwd = 'target database password'

    def tearDown(self):
        pass

    def test_copy_site_command(self):
        command_pool = list()

        CommonCommand(command_pool).copy_site_command(self.source_host, self.target_host)

        self.assertEqual(1, len(command_pool))
        self.assertTrue('scp' in command_pool[0])
        self.assertTrue('%s@%s' % ('root', self.source_host.ip) in command_pool[0])
        self.assertTrue(self.source_host.pwd in command_pool[0])
        self.assertTrue('/home/wwwroot/%s' % (self.source_host.domain) in command_pool[0])
        self.assertTrue('/home/wwwroot/%s' % (self.target_host.domain) in command_pool[0])

    def test_apache_config_command(self):
        command_pool = list()

        CommonCommand(command_pool).apache_config_command(self.source_host, self.target_host)

        self.assertEqual(2, len(command_pool))

        self.assertTrue('scp' in command_pool[0])
        self.assertTrue('%s@%s' % ('root', self.source_host.ip) in command_pool[0])
        self.assertTrue(self.source_host.pwd in command_pool[0])
        self.assertTrue('/usr/local/apache/conf/vhost/%s.conf' % (self.source_host.domain) in command_pool[0])
        self.assertTrue('/usr/local/apache/conf/vhost/%s.conf' % (self.target_host.domain) in command_pool[0])

        self.assertTrue('sed -i' in command_pool[1])
        self.assertTrue('%s/%s' % (self.source_host.domain, self.target_host.domain) in command_pool[1])
        self.assertTrue('/usr/local/apache/conf/vhost/%s.conf' % (self.target_host.domain) in command_pool[1])

    def test_nginx_config_command(self):
        command_pool = list()

        CommonCommand(command_pool).nginx_config_command(self.source_host, self.target_host)

        self.assertEqual(2, len(command_pool))

        self.assertTrue('scp' in command_pool[0])
        self.assertTrue('%s@%s' % ('root', self.source_host.ip) in command_pool[0])
        self.assertTrue(self.source_host.pwd in command_pool[0])
        self.assertTrue('/usr/local/nginx/conf/vhost/%s.conf' % (self.source_host.domain) in command_pool[0])
        self.assertTrue('/usr/local/nginx/conf/vhost/%s.conf' % (self.target_host.domain) in command_pool[0])

        self.assertTrue('sed -i' in command_pool[1])
        self.assertTrue('%s/%s' % (self.source_host.domain, self.target_host.domain) in command_pool[1])
        self.assertTrue('/usr/local/nginx/conf/vhost/%s.conf' % (self.target_host.domain) in command_pool[1])

    def test_mysql_create_user_command(self):
        user_name = 'test user'
        user_password = 'test password'

        command_pool = list()

        CommonCommand(command_pool).mysql_create_user_command(user_name, user_password)

        self.assertEqual(2, len(command_pool))

        self.assertTrue('mysql' in command_pool[0])
        self.assertTrue('\'%s\'@\'localhost\'' % (user_name) in command_pool[0])
        self.assertTrue(user_password in command_pool[0])

        self.assertTrue('mysql' in command_pool[1])
        self.assertTrue('\'%s\'@\'localhost\'' % (user_name) in command_pool[1])
        self.assertTrue(user_password in command_pool[1])

    def test_mysql_create_database_command(self):
        database_name = 'test database'
        user_name = 'test user'

        command_pool = list()

        CommonCommand(command_pool).mysql_create_database_command(database_name, user_name)

        self.assertEqual(2, len(command_pool))

        self.assertTrue('mysql' in command_pool[0])
        self.assertTrue(database_name in command_pool[0])

        self.assertTrue('mysql' in command_pool[1])
        self.assertTrue('\'%s\'@\'localhost\'' % (user_name) in command_pool[1])
        self.assertTrue(database_name in command_pool[1])

if __name__ == '__main__':
    unittest.main()
