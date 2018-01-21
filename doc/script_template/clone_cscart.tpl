screen
yum install -y epel-release
yum install -y sshpass
rm -rf /home/wwwroot/target_doamin
sshpass -p 'source_password' rsync -aze "ssh -o StrictHostKeyChecking=no" root@source_ip:/home/wwwroot/source_domain/ /home/wwwroot/target_doamin/
chown -R www:www /home/wwwroot/target_doamin
rm -rf /usr/local/apache/conf/vhost/target_doamin.conf
sshpass -p 'source_password' rsync -aze "ssh -o StrictHostKeyChecking=no" root@source_ip:/usr/local/apache/conf/vhost/source_domain.conf /usr/local/apache/conf/vhost/target_doamin.conf
sed -i "s/source_domain/target_doamin/g" /usr/local/apache/conf/vhost/target_doamin.conf
rm -rf /usr/local/nginx/conf/vhost/target_doamin.conf
sshpass -p 'source_password' rsync -aze "ssh -o StrictHostKeyChecking=no" root@source_ip:/usr/local/nginx/conf/vhost/source_domain.conf /usr/local/nginx/conf/vhost/target_doamin.conf
sed -i "s/source_domain/target_doamin/g" /usr/local/nginx/conf/vhost/target_doamin.conf
mysql -u root -p'database_root_password' -e "DROP USER IF EXISTS 'database_user_name'@'localhost';"
mysql -u root -p'database_root_password' -e "CREATE USER 'database_user_name'@'localhost' IDENTIFIED BY 'database_password';"
mysql -u root -p'database_root_password' -e "GRANT USAGE ON * . * TO 'database_user_name'@'localhost' IDENTIFIED BY 'database_password' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;"
mysql -u root -p'database_root_password' -e "DROP DATABASE IF EXISTS \`database_name\`;"
mysql -u root -p'database_root_password' -e "CREATE DATABASE \`database_name\`;"
mysql -u root -p'database_root_password' -e "GRANT ALL PRIVILEGES ON \`database_name\` . * TO 'database_user_name'@'localhost';"
sed -i "s/source_domain/target_doamin/Ig" /home/wwwroot/target_doamin/dacscartb.sql
mysql -u root -p'database_root_password' database_name < /home/wwwroot/target_doamin/dacscartb.sql
rm -rf /home/wwwroot/target_doamin/var/cache/*
sed -i "s/\$config\['db_name'\] = '.*';/\$config\['db_name'\] = 'target_database_name';/g" /home/wwwroot/target_doamin/config.local.php
sed -i "s/\$config\['db_user'\] = '.*';/\$config\['db_user'\] = 'target_database_user_name';/g" /home/wwwroot/target_doamin/config.local.php
sed -i "s/\$config\['db_password'\] = '.*';/\$config\['db_password'\] = 'target_database_password';/g" /home/wwwroot/target_doamin/config.local.php
sed -i "s/source_domain/target_doamin/Ig" /home/wwwroot/target_doamin/config.local.php
mysql -u root -p'target_database_root_password' -e "UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = '1' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 62;"
mysql -u root -p'target_database_root_password' -e "UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'smtp_host' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 109;"
mysql -u root -p'target_database_root_password' -e "UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'smtp_user_name' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 111;"
mysql -u root -p'target_database_root_password' -e "UPDATE \`target_database_name\`.\`table_prefix_settings_objects\` SET \`value\` = 'smtp_user_password' WHERE \`table_prefix_settings_objects\`.\`object_id\` = 112;"
lnmp restart
