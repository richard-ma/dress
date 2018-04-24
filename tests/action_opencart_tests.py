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

        self.assertEqual(8, len(data))
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
        self.assertTrue(
            "sed -i \"s/define('DB_DATABASE', '.*');/define('DB_DATABASE', 'target_database_name');/g\" /home/wwwroot/target_domain/admin/config.php"
            in data[4])
        self.assertTrue(
            "sed -i \"s/define('DB_USERNAME', '.*');/define('DB_USERNAME', 'target_database_user_name');/g\" /home/wwwroot/target_domain/admin/config.php"
            in data[5])
        self.assertTrue(
            "sed -i \"s/define('DB_PASSWORD', '.*');/define('DB_PASSWORD', 'target_database_password');/g\" /home/wwwroot/target_domain/admin/config.php"
            in data[6])
        self.assertTrue(
            "sed -i \"s/source_domain/target_domain/Ig\" /home/wwwroot/target_domain/admin/config.php"
            in data[7])


    def test_opencart_order_start_id(self):
        action = OpencartOrderStartIdAction(
            target_database_root_password='target_database_root_password',
            table_prefix='table_prefix_',
            order_start_id='order_start_id')
        data = action.run(list())

        self.assertEqual(1, len(data))
        self.assertTrue(
            "mysql -u root -p'target_database_root_password' -e \"ALTER TABLE \`table_prefix_order\` AUTO_INCREMENT = order_start_id;\""
            in data[0])


if __name__ == '__main__':
    unittest.main()
