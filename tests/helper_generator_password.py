import unittest

from dress.helper import *

class GeneratorPasswordHelperTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generator_password_helper(self):
        password_len = 32
        password = generator_password_helper(password_len)
        self.assertEqual(password_len, len(password))

        password1 = generator_password_helper(password_len)
        password2 = generator_password_helper(password_len)
        self.assertNotEqual(password1, password2)

if __name__ == '__main__':
    unittest.main()
