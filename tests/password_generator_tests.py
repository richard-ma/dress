import unittest
from flask_testing import TestCase
import dress
from dress.utils.generator import PasswordGenerator
from time import sleep

class PasswordGeneratorTestCase(TestCase):

    def create_app(self):
        app = dress.create_app()
        app.config.testing = True

        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_password_generator(self):
        password_len = 32
        password = PasswordGenerator.generat(password_len)
        self.assertEqual(len(password), password_len)

        password1 = PasswordGenerator.generat(password_len)
        sleep(1)
        password2 = PasswordGenerator.generat(password_len)
        self.assertNotEqual(password1, password2)

if __name__ == '__main__':
    unittest.main()
