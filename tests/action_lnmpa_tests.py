import unittest
import dress

from dress.actions import *


class ActionLnmpaTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lnmpa_install(self):
        action = LnmpaInstallAction(
            db_root_password='db_root_password',
            domain='domain.com',
        )
        data = action.run(list())

        self.assertEqual(5, len(data))
        self.assertTrue("yum install -y wget" in data[0])
        self.assertTrue("wget http://soft.vpser.net/lnmp/lnmp1.5beta.tar.gz -cO lnmp1.5beta.tar.gz" in data[1])
        self.assertTrue("tar zxf lnmp1.5beta.tar.gz" in data[2])
        self.assertTrue("cd lnmp1.5" in data[3])
        self.assertTrue("LNMP_Auto='y' DBSelect='3' DB_Root_Password='db_root_password' InstallInnodb='y' PHPSelect='5' SelectMalloc='1' ApacheSelect='2' ServerAdmin='admin@domain.com' ./install.sh lnmpa" in data[4])


if __name__ == '__main__':
    unittest.main()
