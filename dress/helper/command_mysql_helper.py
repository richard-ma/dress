def command_mysql_helper(database_root_password, sql):
    return "mysql -u root -p\'%s\' -e \"%s\"" % (database_root_password,
                                                 sql.replace('`', '\\`')
                                                 )  # fix #1: 将sql语句换为双引号，转义`字符
