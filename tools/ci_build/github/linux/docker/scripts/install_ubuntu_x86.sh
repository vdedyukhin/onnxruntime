#!/bin/bash
set -e
while getopts p: parameter_Option
do case "${parameter_Option}"
in
p) PYTHON_VER=${OPTARG};;
esac
done

PYTHON_VER=${PYTHON_VER:=3.5}
DEBIAN_FRONTEND=noninteractive

apt-get update && apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get update && apt-get install -y --no-install-recommends \
        autotools-dev \
        build-essential \
        git apt-transport-https \
        ca-certificates \
        pkg-config \
        wget \
        zlib1g \
        zlib1g-dev \
        libssl-dev \
        curl \
        autoconf \
        sudo \
        gfortran \
        python3-dev \
        language-pack-en \
        libopenblas-dev \
        liblttng-ust0 \
        libcurl3 \
        libssl1.0.0 \
        libkrb5-3 \
        libicu55 \
        aria2 \
        bzip2 \
        unzip \
        zip \
        rsync libunwind8 libpng16-dev \
        python3-setuptools python3-numpy python3-wheel python python3-pip python3-pytest \
        re2c \
        ninja-build

locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8

if [ $PYTHON_VER!="3.5" ]; then
    apt-get install -y --no-install-recommends \
            python${PYTHON_VER} \
            python${PYTHON_VER}-dev
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VER} 1
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 2
    update-alternatives --set python3 /usr/bin/python${PYTHON_VER}
fi

/usr/bin/python${PYTHON_VER} -m pip install --upgrade --force-reinstall numpy==1.15.0
rm -rf /var/lib/apt/lists/*
