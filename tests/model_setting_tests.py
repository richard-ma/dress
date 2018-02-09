#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.models import *
from manager import seed

class ModelSettingTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

    def tearDown(self):
        pass

    def test_create_setting(self):
        s = Setting(name='testSetting', value='testValue')
        s.create()

        query_setting = Setting.query.filter_by(name='testSetting').first()

        self.assertEqual(query_setting.name, 'testSetting')
        self.assertEqual(query_setting.value, 'testValue')

    def test_update_setting(self):
        s = Setting(name='testSetting', value='testValue')
        s.create()

        update_setting = Setting.query.filter_by(name='testSetting').first()
        update_setting.update(value='updateValue')

        self.assertEqual(update_setting.name, 'testSetting')
        self.assertEqual(update_setting.value, 'updateValue')

    def test_delete_setting(self):
        s = Setting(name='testSetting', value='testValue')
        s.create()

        query_setting = Setting.query.filter_by(name='testSetting').first()
        self.assertEqual(query_setting.name, 'testSetting')
        self.assertEqual(query_setting.value, 'testValue')

        s.delete()
        self.assertIsNone(Setting.query.filter_by(name='testSetting').first())

if __name__ == '__main__':
    unittest.main()
