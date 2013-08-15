# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import psycopg2


## This class manages all the database logic.  This includes connecting, logging, stored procedures, etc.
#  It is expected to be called primarily to store data coming in from the blender class.  Best guess is that
#  this class will be called with multiple threads.  The postgresql connection is thread safe and therefore
#  should be the only class variable.  (A cursor should be opened "locally" for each read/write)
class RecordKeeper:

    ## This is thread safe and is slow to create so BP's are to share this amongst threads.
    dbConnection = None

    ## Sets the connection string to be used in opening and closing the db connection
    #  Format: "dbname=test user=postgres password=something"
    #  see: http://initd.org/psycopg/docs/module.html
    def __init__(self, connection_string):
        self.connection_string = connection_string

    ## Gets a connection to the database. From Psycopg2 best practices: Creating a connection can be slow
    # (think of SSL over TCP) so the best practice is to create a single connection and keep it open as long
    # as required. It is also good practice to rollback or commit frequently (even after a single SELECT statement)
    # to make sure the backend is never left "idle in transaction".  Connections are thread safe and can be
    # shared across multiple threads.
    # todo: figure out error handling here.  Haven't found in docs yet.
    def openDbConnection(self, connection_string):
        self.dbConnection = psycopg2.connect(connection_string)


    # ----------------------------------- Procedures ----------------------------------------
    # My gut tells me that for now the best way to store our queries and insertions are as functions.
    # This will make changes easier and allow flexibility early until we get our design nailed down.

    



