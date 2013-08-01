#!/usr/bin/env bash

if [[ $UID -ne 0 ]]; then
  echo "$0 must be run as root"
  exit 1
fi

#change hosts and hostname
#sed "s/ubuntu/owyhee/" -i /etc/hosts
#sed "s/ubuntu/owyhee/" -i /etc/hostname

# user setup
adduser mansherpa --gecos "manual account for sherpa project" --disabled-password
echo "mansherpa:mansherpa" | chpasswd 
usermod -a -G sudo mansherpa 

#adduser autosherpa --gecos "auto account for sherpa project" --disabled-password
#echo "autosherpa:autosherpa" | chpasswd

# !!!NEEDS TO NOT BE RUN AS ROOT!!!
#sudo su mansherpa
#ssh key
#mkdir ~/.ssh 
#chmod 700 .ssh
#exit 

#ssh-keygen -f .ssh/id_rsa -q -P ""

# global path settings (must prior to creating users) 

# application update and install 

apt-get update
apt-get upgrade -y
apt-get install -y git postgresql-9.1 python3.3 python3.3-dev python3-pip build-essential gdb openssh-server libopenjpeg2 libopenjpeg-dev python3-psycopg2

GRIB_VERSION="1.10.4"
GRIB_LOCATION="grib_api-$GRIB_VERSION"
GRIB_FILE="$GRIB_LOCATION.tar.gz"
GRIB_LIB="lib$GRIB_LOCATION.so"

wget https://software.ecmwf.int/wiki/download/attachments/3473437/$GRIB_FILE 
tar xzvf $GRIB_FILE
cd $GRIB_LOCATION
./configure
make
make install 
ln -s /usr/local/lib/$GRIB_LIB /usr/lib/$GRIB_LIB
pip-3.3 install numpy 
pip-3.3 install pyproj
pip-3.3 install pygrib
cd ..
rm -fr $GRIB_FILE $GRIB_LOCATION

