import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from seed import seed_db

from dress.tasks.tasks import Command

class CommandTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed_db(self.app)

    def tearDown(self):
        pass

    def test_scp_command_with_all_parameters(self):
        source_ip = '233.233.233.233'
        source_path = 'source_path'
        target_path = 'target_path'
        source_user = 'source_user'
        source_password = 'source_password'

        command_pool = list()

        Command(command_pool).scp(
                source_ip,
                source_path,
                target_path,
                source_user,
                source_password)

        self.assertEqual(1, len(command_pool))
        self.assertTrue('scp' in command_pool[0])
        self.assertTrue('%s@%s' % (source_user, source_ip) in command_pool[0])
        self.assertTrue(source_password in command_pool[0])
        self.assertTrue(source_path in command_pool[0])
        self.assertTrue(target_path in command_pool[0])

    def test_scp_command_with_default_parameters(self):
        source_ip = '233.233.233.233'
        source_path = 'source_path'
        target_path = 'target_path'

        command_pool = list()

        Command(command_pool).scp(
                source_ip,
                source_path,
                target_path)

        self.assertEqual(1, len(command_pool))
        self.assertTrue('scp' in command_pool[0])
        self.assertTrue('%s@%s' % ('root', source_ip) in command_pool[0])
        self.assertTrue(source_path in command_pool[0])
        self.assertTrue(target_path in command_pool[0])

    def test_sed_command(self):
        source = 'source'
        target = 'target'
        filename = 'filename'

        command_pool = list()

        Command(command_pool).sed(
                source,
                target,
                filename)
        self.assertEqual(1, len(command_pool))
        self.assertTrue('sed -i' in command_pool[0])
        self.assertTrue('%s/%s' % (source, target) in command_pool[0])
        self.assertTrue(filename in command_pool[0])

    def test_sql_command(self):
        sql = 'sql satement'

        command_pool = list()

        Command(command_pool).sql(sql)
        self.assertEqual(1, len(command_pool))
        self.assertTrue('mysql -u root -e' in command_pool[0])
        self.assertTrue(sql in command_pool[0])

    def test_command_command(self):
        command = 'command'

        command_pool = list()

        Command(command_pool).command(command)
        self.assertEqual(1, len(command_pool))
        self.assertTrue(command in command_pool[0])

if __name__ == '__main__':
    unittest.main()
