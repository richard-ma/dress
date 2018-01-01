import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from manager import seed

from dress.tasks.tasks import Command

class CommandTestCase(TestCase):

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

    def test_cp_command_with_all_parameters(self):
        command_pool = list()

        Command(command_pool).cp(
                source_ip=self.source_host.ip,
                source_user="source_user",
                source_password=self.source_host.pwd,
                source_path="source_path",
                target_path="target_path")

        self.assertEqual(1, len(command_pool))

        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" source_user@1.1.1.1:source_path target_path" in command_pool[0])

    def test_cp_command_with_default_parameters(self):
        command_pool = list()

        Command(command_pool).cp(
                source_ip=self.source_host.ip,
                source_path="source_path",
                target_path="target_path")

        self.assertEqual(1, len(command_pool))

        self.assertTrue("sshpass -p \'\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" root@1.1.1.1:source_path target_path" in command_pool[0])

    def test_sed_command(self):
        command_pool = list()

        Command(command_pool).sed(
                source="source",
                target="target",
                filename="filename")
        self.assertEqual(1, len(command_pool))

        self.assertTrue("sed -i 's/source/target/g' filename" in command_pool[0])

    def test_sql_command(self):
        command_pool = list()

        Command(command_pool).sql(self.target_host.db_pwd, sql="sql_statement")
        self.assertEqual(1, len(command_pool))
        self.assertTrue("mysql -u root -p\'target_database_password\' -e \"sql_statement\"" in command_pool[0])

    def test_sql_command_with_single_quote(self):
        command_pool = list()

        Command(command_pool).sql(self.target_host.db_pwd, sql="this is single 'quote' test")
        self.assertEqual(1, len(command_pool))
        self.assertTrue("mysql -u root -p\'target_database_password\' -e \"this is single 'quote' test\"" in command_pool[0])

    def test_command_command(self):
        command = 'command'

        command_pool = list()

        Command(command_pool).command(command)
        self.assertEqual(1, len(command_pool))
        self.assertTrue(command in command_pool[0])

if __name__ == '__main__':
    unittest.main()
