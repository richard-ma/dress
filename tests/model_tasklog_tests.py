#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.models import *
from manager import seed

class ModelTaskLogTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

    def tearDown(self):
        pass

    def test_create_setting_with_default_value(self):
        tl = TaskLog()
        tl.create()

        query_tl = TaskLog.query.all().first()

        self.assertEqual(query_tl.task_name, 'unknown')
        self.assertEqual(query_tl.custom_data, dict())

if __name__ == '__main__':
    unittest.main()
