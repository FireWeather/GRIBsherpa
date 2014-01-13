#! /usr/bin/env python3

# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import psycopg2
import socket
import sys


class Database(object):

    def __init__(self, db_name=None, db_user=None, db_password=None):
        if db_name is not None and db_user is not None and db_password is not None:
            self.setup_connection(db_name, db_user, db_password)

    def setup_connection(self, db_name, db_user, db_password):
        self.connection_string = ""
        self.connection_string += self.__append_string("dbname=", db_name)
        self.connection_string += self.__append_string("user=", db_user)
        self.connection_string += self.__append_string("password=", db_password)
        self.connection_string += self.__append_string("host=", str(socket.gethostbyname(socket.gethostname() ) ) )

    def open_connection(self):
        try:
            self.db_connection = psycopg2.connect(self.connection_string)
        except psycopg2.OperationalError as err:
            sys.stderr.write("Error opening the db connection with: " + str(self.connection_string) +
                             ", The error received was: " + str(err))
            raise err

    def close_connection(self):
        if self.db_connection is None:
            sys.stderr.write("No connection to close")
            return
        else:
            self.db_connection.close()

    def __append_string(self, key, value):
        return key + value + " "


