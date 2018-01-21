import unittest

from dress.helper import command_mysql_helper

class CommandMysqlHelperTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mysql_command(self):
        re = command_mysql_helper("target_database_root_password", "sql_statement")
        self.assertEqual(re, "mysql -u root -p\'target_database_root_password\' -e \"sql_statement\"")

    def test_mysql_command_with_single_quote(self):
        re = command_mysql_helper("target_database_root_password", "this is single 'quote' test")
        self.assertEqual(re, "mysql -u root -p\'target_database_root_password\' -e \"this is single 'quote' test\"")

if __name__ == '__main__':
    unittest.main()
