#!/usr/bin/env bash
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

sudo -u vagrant dropdb stormking
sudo -u vagrant psql -e -f dbstormking_create.sql
sudo -u vagrant psql -e -f dbstormking_create_schema.sql
