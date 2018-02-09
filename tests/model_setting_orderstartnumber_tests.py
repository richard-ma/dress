#!/usr/bin/env python

import unittest
import random
from flask_testing import TestCase
import dress
from dress.models import *
from manager import seed


class ModelSettingOrderStartNumberTestCase(TestCase):
    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

    def tearDown(self):
        pass

    def test_get_with_init_value(self):
        obj = SettingOrderStartNumber()
        self.assertEqual(SettingOrderStartNumber.INIT_VALUE, obj.get())

    def test_inc_interval_with_default_interval(self):
        obj = SettingOrderStartNumber()
        old_value = obj.get()
        new_value = obj.inc_interval()
        self.assertEqual(new_value - old_value,
                         SettingOrderStartNumber.DEFAULT_INTERVAL)

    def test_inc_interval_with_custom_interval(self):
        obj = SettingOrderStartNumber()
        custom_interval = 10
        old_value = obj.get()
        new_value = obj.inc_interval(interval=custom_interval)
        self.assertEqual(new_value - old_value, custom_interval)

    def test_reset_with_init_value(self):
        obj = SettingOrderStartNumber()
        for times in range(random.randint(1, 3)):
            obj.inc_interval()
        obj.reset()
        self.assertEqual(SettingOrderStartNumber.INIT_VALUE, obj.get())

    def test_reset_with_custom_value(self):
        obj = SettingOrderStartNumber()
        custom_value = 100
        for times in range(random.randint(1, 3)):
            obj.inc_interval()
        obj.reset(value=custom_value)
        self.assertEqual(custom_value, obj.get())


if __name__ == '__main__':
    unittest.main()
