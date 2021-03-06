#!/usr/bin/env bash
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

# after it comepletes open vim
# :BundleList
# :BundleInstall 
# tada all complete...

USER="vagrant"
HOME_DIR="/home/$USER"

##########################################################################
#VIM STUFF / EVENTUALLY EXCLUDE FROM THIS SCRIPT 
cd vimrc
sudo -u $USER mkdir -p $HOME_DIR/.vim/bundle/vundle
sudo -u $USER cp .vimrc $HOME_DIR/.vimrc
sudo -u $USER git clone https://github.com/gmarik/vundle.git $HOME_DIR/.vim/bundle/vundle
sudo -u $USER wget https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf
sudo -u $USER wget https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
sudo -u $USER mkdir $HOME_DIR/.fonts
sudo -u $USER mv PowerlineSymbols.otf $HOME_DIR/.fonts/.
fc-cache -vf $HOME_DIR/.fonts 
sudo -u $USER mkdir -p $HOME_DIR/.config/fontconfig/conf.d
sudo -u $USER mv 10-powerline-symbols.conf $HOME_DIR/.config/fontconfig/conf.d/.
cd ..

