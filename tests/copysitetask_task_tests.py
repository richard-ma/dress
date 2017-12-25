#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from dress.tasks.tasks import CopySiteTask
from seed import seed_db

class CopySiteTaskTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed_db(self.app)

    def tearDown(self):
        pass

    def test_copy_site_task(self):
        command_pool = list()
        task = CopySiteTask(command_pool)

        source_host = Host.query.filter_by(id=1).first()
        target_host = Host.query.filter_by(id=2).first()
        task.run(source_host, target_host)

        self.assertTrue(len(command_pool) > 0)
        self.assertTrue(source_host.pwd in command_pool[0])
        self.assertTrue(source_host.ip in command_pool[0])
        self.assertTrue(source_host.domain in command_pool[0])
        self.assertTrue(target_host.domain in command_pool[0])

if __name__ == '__main__':
    unittest.main()
