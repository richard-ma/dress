#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from seed import seed_db
#from tests.utils import get_endpoint

class HostTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
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

    def test_update_host(self):
        h = Host('testhost')
        h.create()
        update_host = Host.query.filter_by(name='testhost').first()

        new_status = Status.query.filter_by(title='Business').first()
        update_host.update(
                name=update_host.name,
                ip=update_host.ip,
                port=update_host.port,
                domain='test.domain',
                pwd=update_host.pwd,
                db_name=update_host.db_name,
                db_pwd=update_host.db_pwd,
                status=new_status.id)
        self.assertEqual('test.domain', update_host.domain)
        self.assertEqual(new_status.title, update_host.status.title)

    def test_delete_host(self):
        h = Host('testhost')
        h.create()

        # host created
        query_host = Host.query.filter_by(name='testhost').first()
        self.assertEqual(query_host.status.title, 'Prepare')

        # delete host
        h.delete()
        self.assertIsNone(Host.query.filter_by(name='testhost').first())

if __name__ == '__main__':
    unittest.main()
