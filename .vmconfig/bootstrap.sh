#!/usr/bin/env bash
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

# this script takes about 20 minutes to run

if [ -f "/var/vagrant_provision" ]; then 
  echo "Provisioner already ran once"
  exit 0
fi

if [[ $UID -ne 0 ]]; then
  echo "$0 must be run as root"
  exit 1
fi

VAGRANT_DIR="/vagrant"
POSTGIS="postgis-2.0.3"

#change hosts and hostname DO IN Vagrantfile is using Vagrant
#sed "s/vagrant-ubuntu-raring-64/owyhee/" -i /etc/hosts
#sed "s/vagrant-ubuntu-raring-64/owyhee/" -i /etc/hostname

##########################################################################
# add user mansherpa
adduser mansherpa --gecos "manual account for sherpa project" --disabled-password
echo "mansherpa:mansherpa" | chpasswd 
usermod -a -G sudo mansherpa 

# add user susherpa
adduser susherpa --gecos "admin account for sherpa project" --disabled-password
echo "susherpa:susherpa" | chpasswd 
usermod -a -G sudo susherpa 

# add user autosherpa
adduser autosherpa --gecos "auto account for sherpa project" --disabled-password
echo "autosherpa:autosherpa" | chpasswd

# global path settings (must prior to creating users) 
#nothing yet

# application update and install 
##########################################################################
apt-get update
apt-get upgrade -y
apt-get install -y git postgresql-9.1 postgresql-server-dev-9.1 libxml2-dev libgeos-dev libproj-dev libjson0-dev xsltproc docbook-xsl docbook-mathml libgdal-dev python3.3 python3.3-dev python3-pip build-essential gdb openssh-server libopenjpeg2 libopenjpeg-dev python3-psycopg2 libpython3-dbg libpython3.3-dbg python3-dbg python3-psycopg2-dbg python3.3-dbg tree postgresql-contrib-9.1 python3-scipy python3-scipy-dbg python3-numpy python3-numpy-dbg
sed "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" -i /etc/postgresql/9.1/main/postgresql.conf
sed 's/^host.*/host\tall\t\tall\t\tall\t\t\tmd5/' -i /etc/postgresql/9.1/main/pg_hba.conf
###########################################################################
cd $VAGRANT_DIR
wget http://download.osgeo.org/postgis/source/$POSTGIS.tar.gz
tar xfvz $POSTGIS.tar.gz
cd $POSTGIS
./configure
make
make install
ldconfig
make comments-install
make clean
cd ..
rm -fr $POSTGIS $POSTGIS.tar.gz

ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/shp2pgsql
ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/pgsql2shp
ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/raster2pgsql

###########################################################################
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
make clean
cd ..
rm -fr $GRIB_FILE $GRIB_LOCATION

ln -s /usr/local/lib/$GRIB_LIB /usr/lib/$GRIB_LIB
#pip-3.3 install numpy 
pip-3.3 install pyproj
pip-3.3 install pygrib

##########################################################################
cd $VAGRANT_DIR
sudo -u postgres psql -e -f dbusersetup.sql
sudo -u postgres psql -e -f dbstormking_create.sql
sudo -u susherpa psql -e -f dbstormking_create_schema.sql
service postgresql restart

# next TEST ONLY
mkdir -p /grib/tmp
chown vagrant /grib/tmp
chgrp vagrant /grib/tmp

touch /var/vagrant_provision
