from dress.vendor.workflow import *
from dress.helper import *
from dress.actions import *


# Env Version
# PHP >= 5.6
# Mysql >= 5.6
# Apache >= 2.2
#


def magento_workflow(**params):
    target_database_password = generator_password_helper(32)
    data_file_name = "/home/wwwroot/%s/d%sb.sql" % (
            params['target_domain'],
            params['source_domain'].split('.')[0])

    parsed_params = {
        'logger': params['logger'],
        'source_domain': params['source_domain'],
        'source_ip': params['source_ip'],
        'source_port': params['source_port'],
        'source_user': 'root',
        'source_password': params['source_password'],
        'target_domain': params['target_domain'],
        'target_ip': params['target_ip'],
        'target_port': params['target_port'],
        'target_user': 'root',
        'target_password': params['target_password'],
        'target_database_root_password': params['target_database_root_password'],
        'target_database_user_name': params['target_domain'],
        'target_database_password': target_database_password,
        'target_database_name': params['target_domain'],  # target_domain
        'database_root_password': params['target_database_root_password'],  # target_database_root_password
        'database_user_name': params['target_domain'],  # target_domain
        'database_password': target_database_password,  # target_database_password
        'database_name': params['target_domain'],  # target_domain
        'data_file_name': data_file_name,
        'table_prefix': 'cscart_',  # table prefix
        'order_start_id': params['order_start_id'] if 'order_start_id' in params.keys() else None,  # order_start_id
        'ssh_ip': params['target_ip'],  # target_ip
        'ssh_port': params['target_port'],  # target_port always 22
        'ssh_username': 'root',  # target_user_name always root
        'ssh_password': params['target_password'],  # target_password
    }
    w = Workflow(initData=list()
    ).push(
        InitAction(**parsed_params)
    ).push(
        CopySiteAction(**parsed_params)
    ).push(
        ApacheConfigAction(**parsed_params)
    ).push(
        NginxConfigAction(**parsed_params)
    ).push(
        MysqlCreateUserAction(**parsed_params)
    ).push(
        MysqlCreateDatabaseAction(**parsed_params)
    ).push(
        MysqlImportDataAction(**parsed_params)
    ).push(
        MagentoClearCacheAction(**parsed_params)
    ).push(
        MagentoConfigAction(**parsed_params)
    ).push(
        LnmpRestartAction(**parsed_params)
    ).push(
        SshAction(**parsed_params)
    ).execute()


if __name__ == '__main__':
    magento_workflow()
