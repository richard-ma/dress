import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from dress.tasks.tasks import CloneSiteTask
from manager import seed

class CloneSiteTaskTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

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

    def test_clone_site_task(self):
        command_pool = list()

        #task = CloneSiteTask(self.source_host, self.target_host).run()
        # todo
        return True

if __name__ == '__main__':
    unittest.main()
