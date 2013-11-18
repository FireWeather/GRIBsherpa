#!/usr/bin/env bash
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

sudo -u postgres dropdb stormking
sudo -u postgres psql -e -f dbstormking_create.sql
sudo -u susherpa psql -e -f dbstormking_create_schema.sql
