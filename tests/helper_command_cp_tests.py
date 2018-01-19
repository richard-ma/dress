from unittest import TestCase

from dress.helper import command_cp_helper

class CommandCpHelperTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cp_command_helper(self):
        re = command_cp_helper(
                "source_password",
                "source_user",
                "source_ip",
                "source_path",
                "target_path")
        self.assertEqual(re, "sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" source_user@source_ip:source_path target_path")

if __name__ == '__main__':
    unittest.main()
