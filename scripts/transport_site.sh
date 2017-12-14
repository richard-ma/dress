#!/bin/sh

# transport_site.sh <domain> <dest_ip>

# usage
usage() {
    echo "Usage:"
    echo "${0} <domain> <dest_ip>"

    exit -1
}

# check arguments
if [ $# -lt 2 ]; then
    usage
fi
if [ -z "${1}" ]; then
    usage
fi
if [ -z "${2}" ]; then
    usage
fi

domain=${1}
dest_ip=${2}

# create backup dir
scp -p ${domain}.tar.xz root@${dest_ip}:/root
