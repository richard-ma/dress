# Move site workflow

## backup
`run in source host`
Backup database to `$domain`.sql

### Instruction
/root/$domain.sql

## transport
`run in destination host`
Copy site & files to destination host

### Instruction
* sshpass -p `$dest_host.pwd` scp -o StrictHostKeyChecking=no -p -r root@`$dest_host.ip`:/home/wwwroot/`$source_host.domain` /home/wwwroot/`$dest_host.domain`
* sshpass -p `$dest_host.pwd` scp -o StrictHostKeyChecking=no -p root@`$dest_host.ip`:/usr/local/apache/conf/vhost/`$source_host.domain`.conf /usr/local/apache/conf/vhost/`$dest_host.domain`.conf
* sshpass -p `$dest_host.pwd` scp -o StrictHostKeyChecking=no -p root@`$dest_host.ip`:/usr/local/nginx/conf/vhost/`$source_host.domain`.conf /usr/local/nginx/conf/vhost/`$dest_host.domain`.conf

## restore
`run in destination host`
Create database & Import data

### Instruction
* mysql -u root -e 'create database \``$dest_host.domain`\`;'
* mysql -u root `$dest_host.domain` < /home/wwwroot/`$dest_host.domain`/dacscartb.sql

## release
`run in destination host`
Replace all configurations to fit new domain

### Instruction
* replace /usr/local/apache/conf/vhost/`$domain`.conf configurations
* replace /usr/local/nginx/conf/vhost/`$domain`.conf configurations
* replace /home/wwwroot/`$domain`/config.php
* rename /home/wwwroot/`$domain` -> /home/wwwroot/`$new_domain`
* replace databse `$domain` -> `$new_domain`
* restart lnmp
