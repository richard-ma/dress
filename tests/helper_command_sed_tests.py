import unittest

from dress.helper import command_sed_helper

class CommandSedHelperTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sed_command(self):
        re = command_sed_helper(
                "source",
                "target",
                "filename")
        self.assertEqual(re, "sed -i \"s/source/target/g\" filename")

    def test_sed_with_ignore_case(self):
        re = command_sed_helper(
                "source",
                "target",
                "filename",
                ignore_case=True)
        self.assertEqual(re, "sed -i \"s/source/target/Ig\" filename")

if __name__ == '__main__':
    unittest.main()
