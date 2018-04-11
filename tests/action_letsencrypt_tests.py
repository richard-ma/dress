import unittest
import dress

from dress.actions import *

class ActionLetsencryptTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_letsencrypt(self):
        action = LetsencryptAction(
                source_password='source_password',
                source_ip='source_ip',
                source_user='source_user',
                source_domain='source_domain',
                target_domain='target_domain',
                )
        data = action.run(list())

        self.assertEqual(2, len(data))
        self.assertTrue("rm -rf /etc/letsencrypt/live/target_domain" in data[0])
        self.assertTrue("sshpass -p \'source_password\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" source_user@source_ip:/etc/letsencrypt/live/source_domain/ /etc/letsencrypt/live/target_domain" in data[1])

if __name__ == '__main__':
    unittest.main()
