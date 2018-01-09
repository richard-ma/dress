#!/usr/bin/env python

import unittest
from flask_testing import TestCase
import dress
from dress.utils.generator import OrderStartNumberGenerator
from dress.data.models import Setting
from manager import seed

class OrderStartNumberGeneratorTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        seed()

    def tearDown(self):
        pass

    def test_orderstartnumbergenerator(self):
        start_number = 1000
        OrderStartNumberGenerator.reset(start_number)
        OrderStartNumberGenerator.reset()
        self.assertEqual(Setting.ORDER_START_NUMBER_VALUE, Setting.query.filter_by(name=Setting.ORDER_START_NUMBER_NAME).first().value)

        start_number = 1000
        OrderStartNumberGenerator.reset(start_number)
        self.assertEqual(start_number, int(Setting.query.filter_by(name=Setting.ORDER_START_NUMBER_NAME).first().value))

        new_start_number = OrderStartNumberGenerator.generate(interval=800)
        self.assertEqual(new_start_number, start_number+800)

if __name__ == '__main__':
    unittest.main()
