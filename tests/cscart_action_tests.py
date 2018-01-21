import unittest
import dress

from dress.actions import *


class CscartActionTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cscart_clear_cache(self):
        action = CscartClearCacheAction(target_domain='target_domain')
        data = action.run(list())

        self.assertEqual(1, len(data))
        self.assertTrue(
            "rm -rf /home/wwwroot/target_domain/var/cache/*" in data[0])


    def test_cscart_config(self):
        action = CscartConfigAction(
                source_domain='source_domain',
                target_domain='target_domain',
                target_database_name='target_database_name',
                target_database_user_name='target_database_user_name',
                target_database_password='target_database_password')
        data = action.run(list())

        self.assertEqual(4, len(data))
        self.assertTrue("sed -i \"s/\$config\['db_name'\] = '.*';/\$config\['db_name'\] = 'target_database_name';/g\" /home/wwwroot/target_domain/config.local.php" in data[0])
        self.assertTrue("sed -i \"s/\$config\['db_user'\] = '.*';/\$config\['db_user'\] = 'target_database_user_name';/g\" /home/wwwroot/target_domain/config.local.php" in data[1])
        self.assertTrue("sed -i \"s/\$config\['db_password'\] = '.*';/\$config\['db_password'\] = 'target_database_password';/g\" /home/wwwroot/target_domain/config.local.php" in data[2])
        self.assertTrue("sed -i \"s/source_domain/target_domain/Ig\" /home/wwwroot/target_domain/config.local.php" in data[3])

    def test_cscart_order_start_id(self):
        action = CscartOrderStartIdAction(
                target_database_root_password='target_database_root_password',
                target_database_name='target_database_name',
                table_prefix='table_prefix_',
                order_start_id='order_start_id')
        data = action.run(list())

        self.assertEqual(1, len(data))
        self.assertTrue("mysql -u root -p'target_database_root_password' -e \"UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'order_start_id' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 62;\"" in data[0])

    def test_cscart_smtp_setting(self):
        action = CscartSmtpSettingAction(
                target_database_root_password='target_database_root_password',
                target_database_name='target_database_name',
                table_prefix='table_prefix_',
                smtp_host='smtp_host',
                smtp_user_name='smtp_user_name',
                smtp_user_password='smtp_user_password')
        data = action.run(list())

        self.assertEqual(3, len(data))
        self.assertTrue("mysql -u root -p'target_database_root_password' -e \"UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'smtp_host' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 109;\"" in data[0])
        self.assertTrue("mysql -u root -p'target_database_root_password' -e \"UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'smtp_user_name' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 111;\"" in data[1])
        self.assertTrue("mysql -u root -p'target_database_root_password' -e \"UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'smtp_user_password' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 112;\"" in data[2])

if __name__ == '__main__':
    unittest.main()
