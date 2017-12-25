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
        host_ip = '233.233.233.233'
        host_port = 10086
        host_domain = 'host.domain'
        host_pwd = 'hostpwd'
        host_db_pwd = 'db_pwd'
        host_memo = 'memo'
        status = Status.query.all()[0]

        result = self.client.post(
                '/host/add',
                data=dict(
                    host_ip=host_ip,
                    host_port=host_port,
                    host_domain=host_domain,
                    host_pwd=host_pwd,
                    host_db_pwd=host_db_pwd,
                    host_memo=host_memo,
                    host_status=status.id,
                ), follow_redirects=True)

        self.assertTrue(b'added' in result.data)
        self.assertTrue(bytes(host_ip, encoding='utf-8') in result.data)
        self.assertTrue(bytes(str(host_port), encoding='utf-8') in result.data)
        self.assertTrue(bytes(host_domain, encoding='utf-8') in result.data)
        self.assertTrue(bytes(host_memo, encoding='utf-8') in result.data)

    def test_delete_host_operation(self):

        new_host = Host()
        new_host.create()

        host_id = Host.query.filter_by(id=new_host.id).first().id

        result = self.client.get(
                '/host/delete/%d' % (host_id),
                follow_redirects=True)

        self.assertTrue(b'deleted' in result.data)
        self.assertIsNone(Host.query.filter_by(id=new_host.id).first())

    def test_update_host_operation(self):

        new_host = Host()
        new_host.create()

        new_host_ip = '192.168.1.1'
        new_host_port = 22
        new_host_domain = 'new.test.domain'
        new_host_pwd = 'new pwd'
        new_host_db_pwd = 'new db pwd'
        new_host_memo = 'new memo'

        host = Host.query.filter_by(id=new_host.id).first()
        host_id = host.id

        result = self.client.post(
                '/host/update/%d' % (host_id),
                data=dict(
                    host_ip=new_host_ip,
                    host_port=new_host_port,
                    host_domain=new_host_domain,
                    host_pwd=new_host_pwd,
                    host_db_pwd=new_host_db_pwd,
                    host_memo=new_host_memo,
                    host_status=host.status.id,
                ), follow_redirects=True)

        self.assertTrue(b'updated' in result.data)
        self.assertTrue(bytes(new_host_ip, encoding='utf-8') in result.data)
        self.assertTrue(bytes(str(new_host_port), encoding='utf-8') in result.data)
        self.assertTrue(bytes(new_host_domain, encoding='utf-8') in result.data)
        self.assertTrue(bytes(new_host_memo, encoding='utf-8') in result.data)

if __name__ == '__main__':
    unittest.main()
