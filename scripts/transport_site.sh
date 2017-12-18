#!/bin/sh

# pull source host site to dest host
# transport_site.sh <source_domain> <dest_domain> <source_host_ip> <source_host_ssh_password>

# usage
usage() {
    echo "Usage:"
    echo "${0} <source_domain> <dest_domain> <source_host_ip> <source_host_ssh_password>"

    exit -1
}

# check arguments
if [ $# -lt 3 ]; then
    usage
fi
if [ -z "${1}" ]; then
    usage
fi
if [ -z "${2}" ]; then
    usage
fi
if [ -z "${3}" ]; then
    usage
fi
if [ -z "${4}" ]; then
    usage
fi

source_domain=${1}
dest_domain=${2}
source_host_ip=${3}
source_host_ssh_password=${4}

# copy site files
sshpass -p ${source_host_ssh_password} scp -o StrictHostKeyChecking=no -p -r root@${source_host_ip}:/home/wwwroot/${source_domain} /home/wwwroot/${dest_domain}
# copy apache configration
sshpass -p ${source_host_ssh_password} scp -o StrictHostKeyChecking=no -p root@${source_host_ip}:/usr/local/apache/conf/vhost/${source_domain}.conf /usr/local/apache/conf/vhost/${dest_domain}.conf
# copy nginx configration
sshpass -p ${source_host_ssh_password} scp -o StrictHostKeyChecking=no -p root@${source_host_ip}:/usr/local/nginx/conf/vhost/${source_domain}.conf /usr/local/nginx/conf/vhost/${dest_domain}.conf
# copy database (Optional)
