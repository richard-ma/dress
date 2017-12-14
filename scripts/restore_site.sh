#!/bin/sh

# restore_site.sh <domain>

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

tar -xJf ${domain}.tar.xz
cd ${domain}

cp ./apache.conf /usr/local/apache/conf/vhost/${domain}.conf

cp ./nginx.conf /usr/local/nginx/conf/vhost/${domain}.conf


# export site files
tar -cpf site.tar /home/wwwroot/${domain}

# export database
# database is in site directory

# compose site
cd ..
tar -cJpf ${domain}.tar.xz ${domain}
