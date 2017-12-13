#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from seed import seed_db
#from tests.utils import get_endpoint

class HostControllerTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed_db(self.app)

    def tearDown(self):
        pass

    def test_all_host_url(self):
        result = self.client.get('/host')
        self.assertEqual(200, result.status_code)
        self.assertTrue(b'Host' in result.data)
        result = self.client.get('/host/form/')
        self.assertEqual(200, result.status_code)
        self.assertTrue(b'Add Host' in result.data)

if __name__ == '__main__':
    unittest.main()
