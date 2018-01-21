from dress.vendor.workflow import *

from dress.action import *

def cscart_workflow(**params):
    #params = {
            #'source_domain':                    'source_domain',
            #'source_ip':                        'source_ip',
            #'source_user':                      'root',
            #'source_password':                  'source_password',
            #'target_domain':                    'target_doamin',
            #'target_ip':                        'target_ip',
            #'target_user':                      'root',
            #'target_password':                  'target_password',
            #'target_database_root_password':    'target_database_root_password',
            #'target_database_user_name':        'target_database_user_name',
            #'target_database_password':         'target_database_password',
            #'target_database_name':             'target_database_name',
            #'database_root_password':           'database_root_password',  # target_database_root_password
            #'database_user_name':               'database_user_name',      # target_domain
            #'database_password':                'database_password',       # target_database_password
            #'database_name':                    'database_name',           # target_domain
            #'table_prefix':                     'table_prefix_',           # table prefix
            #'order_start_id':                   1,                         # order_start_id
            #'smtp_host':                        'smtp_host',               # smtp_host
            #'smtp_user_name':                   'smtp_user_name',          # smtp_user_name
            #'smtp_user_password':               'smtp_user_password'       # smtp_user_password
    #}
    w = Workflow(initData=list()
    ).push(InitAction(**params)
    ).push(CopySiteAction(**params)
    ).push(ApacheConfigAction(**params)
    ).push(NginxConfigAction(**params)
    ).push(MysqlCreateUserAction(**params)
    ).push(MysqlCreateDatabaseAction(**params)
    ).push(MysqlImportDataAction(**params)
    ).push(CscartClearCacheAction(**params)
    ).push(CscartConfigAction(**params)
    ).push(CscartOrderStartIdAction(**params)
    ).push(CscartSmtpSettingAction(**params)
    ).push(LnmpRestartAction(**params)
    ).push(DebugAction()
    ).execute()

if __name__ == '__main__':
    cscart_workflow()
