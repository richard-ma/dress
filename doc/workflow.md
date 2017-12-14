# Move site workflow

## backup
`run in source host`
Collect all site files, database script and configration files

### Instruction
* create /root/`$domain`
* copy /home/wwwroot/`$domain`/* -> /root/`$domain`/site.tar
* copy /usr/local/apache/conf/vhost/`$domain`.conf -> /root/`$domain`/apache.conf
* copy /usr/local/nginx/conf/vhost/`$domain`.conf -> /root/`$domain`/nginx.conf
* compress /root/`$domain` -> /root/`$domain`.tar.xz

## transport
`run in source host`
Copy site to destination host

### Instruction
* copy /root/`$domain`.tar.xz -> destination_host /root/`$domain`.tar.xz

## restore
`run in destination host`
Restore site to destination host

### Instruction
* uncompress /root/`$domain`.tar.xz -> /root/`$domain`
* copy /root/`$domain`/apache.conf -> /usr/local/apache/conf/vhost/`$domain`.conf
* copy /root/`$domain`/nginx.conf -> /usr/local/nginx/conf/vhost/`$domain`.conf
* unarchive /root/`$domain`/site.tar > /home/wwwroot/`$domain`
* create database
* import data /home/wwwroot/`$domain`/database.sql -> mysql
* restart lnmp

## release
`run in destination host`
Replace all configurations to fit new domain

### Instruction
* replace /usr/local/apache/conf/vhost/`$domain`.conf configurations
* rename /usr/local/apache/conf/vhost/`$domain`.conf -> /usr/local/apache/conf/vhost/`$new_domain`.conf
* replace /usr/local/nginx/conf/vhost/`$domain`.conf configurations
* rename /usr/local/nginx/conf/vhost/`$domain`.conf -> /usr/local/nginx/conf/vhost/`$new_domain`.conf
* replace /home/wwwroot/`$domain`/config.php
* rename /home/wwwroot/`$domain` -> /home/wwwroot/`$new_domain`
* replace databse `$domain` -> `$new_domain`
* restart lnmp
