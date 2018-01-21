def command_cp_helper(source_password, source_user, source_ip, source_path,
                      target_path):
    return "sshpass -p \'%s\' rsync -aze \"ssh -o StrictHostKeyChecking=no\" %s@%s:%s %s" % (
        source_password, source_user, source_ip, source_path, target_path)
