import unittest
import dress

from dress.actions import *


class MagentoActionTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_magento_clear_cache(self):
        action = MagentoClearCacheAction(target_domain='target_domain')
        data = action.run(list())

        self.assertEqual(2, len(data))
        self.assertTrue("rm -rf /home/wwwroot/target_domain/var/cache/*" in data[0])
        self.assertTrue("rm -rf /home/wwwroot/target_domain/var/session/*" in data[1])

    def test_Magento_config(self):
        action = MagentoConfigAction(
            source_domain='source_domain',
            target_domain='target_domain',
            target_database_name='target_database_name',
            target_database_user_name='target_database_user_name',
            target_database_password='target_database_password')
        data = action.run(list())

        self.assertEqual(4, len(data))
        self.assertTrue(
            "sed -i \"s/\$config\['db_name'\] = '.*';/\$config\['db_name'\] = 'target_database_name';/g\" /home/wwwroot/target_domain/config.local.php"
            in data[0])
        self.assertTrue(
            "sed -i \"s/\$config\['db_user'\] = '.*';/\$config\['db_user'\] = 'target_database_user_name';/g\" /home/wwwroot/target_domain/config.local.php"
            in data[1])
        self.assertTrue(
            "sed -i \"s/\$config\['db_password'\] = '.*';/\$config\['db_password'\] = 'target_database_password';/g\" /home/wwwroot/target_domain/config.local.php"
            in data[2])
        self.assertTrue(
            "sed -i \"s/source_domain/target_domain/Ig\" /home/wwwroot/target_domain/config.local.php"
            in data[3])


if __name__ == '__main__':
    unittest.main()
