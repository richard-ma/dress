#!/bin/sh

# backup_site.sh <domain>

# usage
usage() {
    echo "Usage:"
    echo "${0} <domain>"

    exit -1
}

# check arguments
if [ $# -eq 0 ]; then
    usage
fi
if [ -z "${1}" ]; then
    usage
fi

domain=${1}

# create backup dir
mkdir ${domain} 
cd ${domain}

# export site files
tar -cpf site.tar /home/wwwroot/${domain}

# export database
# database is in site directory

# export apache config file
cp /usr/local/apache/conf/vhost/${domain}.conf ./apache.conf

# export nginx config file
cp /usr/local/nginx/conf/vhost/${domain}.conf ./nginx.conf

# compose site
cd ..
tar -cJpf ${domain}.tar.xz ${domain}
