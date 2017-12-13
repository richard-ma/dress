#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.data.models import db, Host, Status
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

    def test_host_url(self):
        result = self.client.get('/host')
        self.assertEqual(200, result.status_code)
        self.assertTrue(b'Host' in result.data)

    def test_add_host_url(self):
        result = self.client.get('/host/form/')
        self.assertEqual(200, result.status_code)
        self.assertTrue(b'Add Host' in result.data)

    def test_update_host_url(self):
        host = Host.query.all()[0]

        result = self.client.get('/host/form/%d' % (host.id))
        self.assertEqual(200, result.status_code)
        self.assertTrue(b'Update Host' in result.data)

    def test_add_host_operation(self):
        host_name = 'uniqueNameHost'
        host = Host(name=host_name)
        result = self.client.post(
                '/host/add',
                data=dict(
                    host_name=host.name,
                    host_ip=host.ip,
                    host_port=host.port,
                    host_domain=host.domain,
                    host_pwd=host.pwd,
                    host_db_name=host.db_name,
                    host_db_pwd=host.db_pwd,
                    host_status=host.status.id,
                ), follow_redirects=True)
        print(result.data)
        self.assertTrue(b'added' in result.data)
        self.assertTrue(host_name in result.data)

if __name__ == '__main__':
    unittest.main()
