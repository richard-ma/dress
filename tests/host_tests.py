#!/usr/bin/env python

import os
import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from seed import seed_db
#from tests.utils import get_endpoint

class HostControllerTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        os.environ['DRESS_CONFIGURATION'] = 'testing'
        seed_db(self.app)

    def tearDown(self):
        pass

    def test_create_host(self):
        h = Host('testhost')
        h.create()

        query_host = Host.query.filter_by(name='testhost').first()

        self.assertEqual(query_host.name, 'testhost')
        self.assertEqual(query_host.port, 22)
        self.assertIsInstance(query_host.status, Status)
        self.assertEqual(query_host.status.title, 'Prepare')

if __name__ == '__main__':
    unittest.main()
