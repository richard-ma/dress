#!/bin/sh

# transport_site.sh <domain> <dest_ip> <dest_ssh_password>

# usage
usage() {
    echo "Usage:"
    echo "${0} <domain> <dest_ip> <dest_ssh_password>"

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

domain=${1}
dest_ip=${2}
dest_ssh_password=${3}

sshpass -p ${dest_ssh_password} scp -o StrictHostKeyChecking=no -p ${domain}.tar root@${dest_ip}:/root
