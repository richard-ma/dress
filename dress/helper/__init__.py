__all__ = ['command_cp_helper', 'command_sed_helper', 'command_mysql_helper']

def command_cp_helper(source_password, source_user, source_ip, source_path,
                      target_path):
    return "sshpass -p \'%s\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" %s@%s:%s %s" % (
        source_password, source_user, source_ip, source_path, target_path)


def command_sed_helper(source, target, filename, ignore_case=False):
    return "sed -i \"s/%s/%s/%sg\" %s" % (
            source,
            target,
            'I' if ignore_case else '',
            filename)


def command_mysql_helper(database_root_password, sql):
    return "mysql -u root -p\'%s\' -e \"%s\"" % (database_root_password,
                                                 sql.replace('`', '\\`')
                                                 )  # fix #1: 将sql语句换为双引号，转义`字符
