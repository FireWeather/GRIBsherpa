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


class Database:

    def __init__(self, db_name=None, db_user=None, db_password=None):

        connection_string = "dbname=" + db_name
        connection_string += " user=" + db_user
        connection_string += " password=" + db_password
        connection_string += " host=" + str(socket.gethostbyname(socket.gethostname()))

        self.connection_string = connection_string
        self.open_connection()

    def open_connection(self):
        try:
            db_connection = psycopg2.connect(self.connection_string)
            self.db_connection = db_connection

        except psycopg2.OperationalError as err:
            sys.stderr.write("Error opening the db connection with: " + str(self.connection_string) +
                             ", The error received was: " + str(err))
            raise err

    def close_connection(self):
        if self.db_connection is None:
            sys.stderr.write("No existing connection to close")
            return
        else:
            self.db_connection.close()

    def get_cursor(self):
        if self.db_connection is None:
            print("No existing connection to attain cursor")
            return

        connection = self.db_connection

        return

    def populate_simple(self, full_table_name, file_handle, headers):
        if self.db_connection is None:
            self.open_connection()

        cursor = self.db_connection.cursor()
        cursor.copy_from(file_handle, full_table_name, sep=',', columns=headers)

        self.db_connection.commit()



def append_string(key, value):
    return str(key + value + " ")


