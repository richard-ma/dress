#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Host, Status
from manager import seed
#from tests.utils import get_endpoint

class HostTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

    def tearDown(self):
        pass

    def test_create_host(self):
        h = Host()
        h.create()

        query_host = Host.query.filter_by(id=h.id).first()

        self.assertEqual(query_host.port, 22)
        self.assertIsInstance(query_host.status, Status)
        self.assertEqual(query_host.status.title, Status.PREPARE)

    def test_update_host(self):
        h = Host()
        h.create()
        update_host = Host.query.filter_by(id=h.id).first()

        new_status = Status.query.filter_by(title=Status.BUSINESS).first()
        update_host.update(
                ip=update_host.ip,
                port=update_host.port,
                domain='test.domain',
                pwd=update_host.pwd,
                db_pwd=update_host.db_pwd,
                memo=update_host.memo,
                status=new_status.id)
        self.assertEqual('test.domain', update_host.domain)
        self.assertEqual(new_status.title, update_host.status.title)

    def test_delete_host(self):
        h = Host('testhost')
        h.create()

        # host created
        query_host = Host.query.filter_by(id=h.id).first()
        self.assertEqual(query_host.status.title, Status.PREPARE)

        # delete host
        h.delete()
        self.assertIsNone(Host.query.filter_by(id=h.id).first())

if __name__ == '__main__':
    unittest.main()
