#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.data.models import Status
from seed import seed_db
#from tests.utils import get_endpoint

class StatusTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed_db(self.app)

    def tearDown(self):
        pass

    def test_create_status(self):
        s = Status(title='testStatus')
        s.create()

        query_status = Status.query.filter_by(title='testStatus').first()

        self.assertEqual(query_status.title, 'testStatus')

    def test_update_title(self):
        s = Status(title='testStatus')
        s.create()

        update_status = Status.query.filter_by(title='testStatus').first()
        update_status.title = 'updateStatus'

        self.assertEqual(update_status.title, 'updateStatus')

    def test_create_status(self):
        s = Status(title='testStatus')
        s.create()

        query_status = Status.query.filter_by(title='testStatus').first()
        self.assertEqual(query_status.title, 'testStatus')

        s.delete()
        self.assertIsNone(Status.query.filter_by(title='testStatus').first())

if __name__ == '__main__':
    unittest.main()