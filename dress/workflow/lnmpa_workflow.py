from dress.vendor.workflow import *
from dress.helper import *
from dress.actions import *


# Install
# PHP = 5.6
# Mysql = 5.6
# Apache = 2.4


def lnmpa_workflow(**params):
    parsed_params = {
        'db_root_password': params['db_root_password'],
        'domain': params['domain']
    }
    w = Workflow(initData=list()
    ).push(
        LnmpaInstallAction(**parsed_params)
    ).push(
        SshAction(**parsed_params)
    ).execute()


if __name__ == '__main__':
    lnmpa_workflow()
