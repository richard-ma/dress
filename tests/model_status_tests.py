#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.models import *
from manager import seed

class ModelStatusTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

    def tearDown(self):
        pass

    def test_create_status(self):
        s = Status(title='testStatus')
        s.create()

        query_status = Status.query.filter_by(title='testStatus').first()

        self.assertEqual(query_status.title, 'testStatus')

    def test_update_status(self):
        s = Status(title='testStatus')
        s.create()

        update_status = Status.query.filter_by(title='testStatus').first()
        update_status.update(title='updateStatus')

        self.assertEqual(update_status.title, 'updateStatus')

    def test_delete_status(self):
        s = Status(title='testStatus')
        s.create()

        query_status = Status.query.filter_by(title='testStatus').first()
        self.assertEqual(query_status.title, 'testStatus')

        s.delete()
        self.assertIsNone(Status.query.filter_by(title='testStatus').first())

if __name__ == '__main__':
    unittest.main()
