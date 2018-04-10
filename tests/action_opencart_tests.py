import unittest
import dress

from dress.actions import *


class ActionOpencartTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_opencart_config(self):
        action = OpencartConfigAction(
            source_domain='source_domain',
            target_domain='target_domain',
            target_database_name='target_database_name',
            target_database_user_name='target_database_user_name',
            target_database_password='target_database_password')
        data = action.run(list())

        self.assertEqual(4, len(data))
        self.assertTrue(
            "sed -i \"s/define('DB_DATABASE', '.*');/define('DB_DATABASE', 'target_database_name');/g\" /home/wwwroot/target_domain/config.php"
            in data[0])
        self.assertTrue(
            "sed -i \"s/define('DB_USERNAME', '.*');/define('DB_USERNAME', 'target_database_user_name');/g\" /home/wwwroot/target_domain/config.php"
            in data[1])
        self.assertTrue(
            "sed -i \"s/define('DB_PASSWORD', '.*');/define('DB_PASSWORD', 'target_database_password');/g\" /home/wwwroot/target_domain/config.php"
            in data[2])
        self.assertTrue(
            "sed -i \"s/source_domain/target_domain/Ig\" /home/wwwroot/target_domain/config.php"
            in data[3])

if __name__ == '__main__':
    unittest.main()
