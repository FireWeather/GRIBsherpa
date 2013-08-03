#!/usr/bin/env bash

if [[ $UID -ne 0 ]]; then
  echo "$0 must be run as root"
  exit 1
fi

#change hosts and hostname
#sed "s/vagrant-ubuntu-raring-64/owyhee/" -i /etc/hosts
#sed "s/vagrant-ubuntu-raring-64/owyhee/" -i /etc/hostname

# add user mansherpa
adduser mansherpa --gecos "manual account for sherpa project" --disabled-password
echo "mansherpa:mansherpa" | chpasswd 
usermod -a -G sudo mansherpa 

# add user susherpa
adduser susherpa --gecos "admin account for sherpa project" --disabled-password
echo "susherpa:susherpa" | chpasswd 
usermod -a -G sudo susherpa 

# add user 
#adduser autosherpa --gecos "auto account for sherpa project" --disabled-password
#echo "autosherpa:autosherpa" | chpasswd

# global path settings (must prior to creating users) 
#nothing yet

# application update and install 

apt-get update
apt-get upgrade -y
apt-get install -y git postgresql-9.1 python3.3 python3.3-dev python3-pip build-essential gdb openssh-server libopenjpeg2 libopenjpeg-dev python3-psycopg2 postgis libpython3-dbg libpython3.3-dbg python3-dbg python3-psycopg2-dbg python3.3-dbg

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
sudo -u postgres createuser -s -d -r susherpa

#NOT FOR PRODUCTION / DEV USE ONLY
sudo -u postgres createuser -s -d -r vagrant

#VIM STUFF / EVENTUALLY EXCLUDE FROM THIS SCRIPT 
cd vimrc
sudo -u vagrant cp .vimrc ~/.vimrc
sudo -u vagrant git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
sudo -u vagrant wget https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf
sudo -u vagrant wget https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
sudo -u vagrant mkdir ~/.fonts
sudo -u vagrant mv PowerlineSymbols.otf ~/.fonts/.
sudo -u vagrant fc-cache -vf ~/.fonts 
sudo -u vagrant mkdir -p ~/.config/fontconfig/conf.d
sudo -u vagrant mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/.
cd ..

# next TEST ONLY
mkdir /grib/tmp
chown vagrant /grib/tmp
chgrp vagrant /grib/tmp


