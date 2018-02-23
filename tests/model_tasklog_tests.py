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

    def test_create_setting_with_value(self):
        task_name = 'unknown'
        custom_data = {
                'hello': 'world'
        }
        tl = TaskLog(task_name, custom_data)
        tl.create()

        query_tl = TaskLog.query.one()

        self.assertEqual(query_tl.task_name, task_name)
        self.assertEqual(query_tl.custom_data, custom_data)
        self.assertEqual(custom_data['hello'], 'world')

if __name__ == '__main__':
    unittest.main()
