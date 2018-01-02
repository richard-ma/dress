import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from manager import seed

from dress.tasks.tasks import CscartCommand

class CscartCommandTestCase(TestCase):

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

    def test_clear_cache(self):
        command_pool = list()

        CscartCommand(command_pool).clear_cache(self.target_host)

        self.assertEqual(1, len(command_pool))

        self.assertTrue("rm -rf /home/wwwroot/target_domain/var/cache/*" in command_pool[0])

    def test_cscart_config(self):
        command_pool = list()

        CscartCommand(command_pool).cscart_config(self.source_host, self.target_host, 'target_database_password')

        self.assertEqual(4, len(command_pool))

        self.assertTrue("sed -i \"s/\$config\['db_name'\] = '.*';/\$config\['db_name'\] = 'target_domain';/g\" /home/wwwroot/target_domain/config.local.php" in command_pool[0])
        self.assertTrue("sed -i \"s/\$config\['db_user'\] = '.*';/\$config\['db_user'\] = 'target_domain';/g\" /home/wwwroot/target_domain/config.local.php" in command_pool[1])
        self.assertTrue("sed -i \"s/\$config\['db_password'\] = '.*';/\$config\['db_password'\] = 'target_database_password';/g\" /home/wwwroot/target_domain/config.local.php" in command_pool[2])
        self.assertTrue("sed -i \"s/source_domain/target_domain/Ig\" /home/wwwroot/target_domain/config.local.php" in command_pool[3])

    def test_cscart_orderStartId(self):
        command_pool = list()

        CscartCommand(command_pool).cscart_orderStartId(self.target_host, 'table_prefix_', 'order_start_id')

        self.assertEqual(1, len(command_pool))

        self.assertTrue("mysql -u root -p'target_database_password' -e \"UPDATE \`target_domain\`.\`table_prefix_settings_objects\` SET \`value\` = 'order_start_id' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 62;\"" in command_pool[0])

if __name__ == '__main__':
    unittest.main()
