from dress.vendor.workflow import *
from dress.helper import *

class LnmpaInstallAction(Action):
    def run(self, *data):
        data = data[0]
        data.append("yum install -y wget")
        data.append("wget http://soft.vpser.net/lnmp/lnmp1.5beta.tar.gz -cO lnmp1.5beta.tar.gz")
        data.append("tar zxf lnmp1.5beta.tar.gz")
        data.append("cd lnmp1.5")
        # install MySQL 5.6 PHP 5.6 Apache 2.4
        data.append("LNMP_Auto='y' DBSelect='3' DB_Root_Password='%s' InstallInnodb='y' PHPSelect='5' SelectMalloc='1' ApacheSelect='2' ServerAdmin='admin@%s' ./install.sh lnmpa" % (self.params['db_root_password'], self.params['domain']))
        return data
