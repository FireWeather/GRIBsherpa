# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import psycopg2
import lib.logger
import socket

## This class manages all the database logic.  This includes connecting, logging, stored procedures, etc.
#  It is expected to be called primarily to store data coming in from the blender class.  Best guess is that
#  this class will be called with multiple threads.  The postgresql connection is thread safe. A cursor should be
#  opened "locally" for each read/write)
class RecordKeeper:

    ## The is the database connection that will be opened and closed and used by the methods below
    dbConnection = None


    ## This accepts "connection_string".  It appends the host to the connection_string.
    #  Format of connection_string should be: "dbname=stormking user=susherpa password=susherpa"
    def __init__(self, connection_string):
        self.log = lib.logger
        self.connection_string = self.__appendHostTo(connection_string)


    ## Opens a connection to the database.  Creating a connection is slow and so this should be kept open if multiple
    #  transactions will take place.  Connections are threadsafe and so it does not matter if there are multiple
    #  RecordKeeper classes each with their own connection.  From the docs: It is also good practice to rollback or
    #  commit frequently (even after a single SELECT statement to make sure the backend is never left "idle in
    #  transaction".  Connections are thread safe and can be
    #  If the connection can't be opened, failure is logged and then the error is passed up...
    def openDbConnection(self):
        try:
            self.dbConnection = psycopg2.connect(self.connection_string)
        except psycopg2.OperationalError as err:
            self.log.write.error("In RecordKeeper, Error opening the db connection with: " + self.connection_string +
                                 " The error received was: " + err)
            raise err


    ## Once you're all done using the database, close the connection.
    def closeDbConnection(self):
        self.dbConnection.close()


    # ----------------------------------- Procedures ----------------------------------------
    # My gut tells me that for now the best way to store our queries and insertions are as functions.
    # This will make changes easier and allow flexibility early until we get our design nailed down.

    ## Used for inserting grid points
    #  Gets a cursor, executes stored proc based on params, closes cursor
    def insertGridPoints(self, region_num, region_ref_num, national_ref_num, location, table):
        assert(self.dbConnection is not None) # Todo: decide on how to handle errors
        cursor = self.dbConnection.cursor()
        cursor.execute("INSERT INTO {4} (region_number, region_ref_number, national_ref_number, location) "
                       "VALUES ({0}, {1}, {2}, {3})".format(region_num, region_ref_num, national_ref_num, location, table))
        cursor.close()



    # -------------------------------- Private -------------------------------------

    ## This uses the "socket" library to get the current IP address of the computer.  It appends this
    #  to the connection_string.  Without the host I was having trouble connecting to the database.
    def __appendHostTo(self, connection_string):
        ipAddress = socket.gethostbyname(socket.gethostname())
        self.log.write.info("In RecordKeeper, IP address is: " + str(ipAddress))
        return connection_string + "host=" + str(ipAddress)