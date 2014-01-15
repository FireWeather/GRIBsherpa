# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import psycopg2
import lib.logger
import socket
import re

## This class manages all the database logic.  This includes connecting, logging, stored procedures, etc.
#  It is expected to be called primarily to store data coming in from the blender class.  Best guess is that
#  this class will be called with multiple threads.  The postgresql connection is thread safe. A cursor should be
#  opened "locally" for each read/write)
class RecordKeeper:

    ## The is the database connection that will be opened and closed and used by the methods below
    dbConnection = None
    index = None

    ## This accepts "connection_string".  It appends the host to the connection_string.
    #  Format of connection_string should be: "dbname=stormking user=susherpa password=susherpa"
    def __init__(self, connection_string):
        self.log = lib.logger
        self.connection_string = self.__appendHostTo(connection_string)
        self.index = 1;


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

    ## Used for inserting grid points
    #  Gets a cursor, executes stored proc based on params, closes cursor
    def insertGridPoints(self, region_num, region_ref_num, national_ref_num, location, table):
        assert(self.dbConnection is not None) # Todo: decide on how to handle errors
        cursor = self.dbConnection.cursor()
        cursor.execute("INSERT INTO {4} (region_number, region_ref_number, national_ref_number, location) "
                       "VALUES ({0}, {1}, {2}, {3})".format(region_num, region_ref_num, national_ref_num, location, table))
        # Todo: add cursor.commit() here?
        cursor.close()

    # TODO document
    def insertRegionData(self, cde):
        dictOfCSVData = cde.getCSVDict()
        assert(self.dbConnection is not None)
        cur = self.dbConnection.cursor()

        for i in dictOfCSVData:
            SQL = "INSERT INTO region (region_name, region_abbv, fs_region_num) VALUES (%s, %s, %s);"
            data = (i.get('fullName'), i.get('abbreviation'), i.get('fsRegion'), )
            cur.execute(SQL, data)

        self.dbConnection.commit()
        cur.close()

    #TODO: can this be made to insert data for all regions instead of just one? Should we have all regions in there?
    def insertGeoData(self, cde, region, grid=None):
        dictOfCSVData = cde.getCSVDict()
        assert(self.dbConnection is not None)
        cur = self.dbConnection.cursor();

        for i in dictOfCSVData:
            SQL = "SELECT region_pkey FROM region WHERE region_abbv = (%s);"
            data = (region, )
            cur.execute(SQL, data)
            # print(cur.fetchall())
            region_pkey = cur.fetchone()

            pointDataLat = i.get('lat')
            pointDataLon = i.get('long')

            if grid is None:
                SQL = "INSERT INTO model_grid_points (region_pkey, region_ref_number, national_ref_number, " \
                      "location) VALUES (%s, %s, %s, ST_GeographyFromText(%s));"

                print(str(region_pkey) + ' ' + str(i.get('id')) + ' ' + str(self.index) + ' ' + str('POINT(' + pointDataLon + ' ' + pointDataLat + ')'))
                data = (region_pkey, i.get('id'), self.index, 'POINT(' + pointDataLon + ' ' + pointDataLat + ')', )
            else:
                SQL = "INSERT INTO model_grid_points (region_pkey, region_ref_number, national_ref_number, " \
                      "location, regional_grid) VALUES (%s, %s, %s, ST_GeographyFromText(%s), %s);"

                print(str(region_pkey))
                print(str(i.get('id')))
                print(str(self.index))
                print(str('POINT(' + pointDataLon + ' ' + pointDataLat + ')'))
                print(str(grid))
                print(str(region_pkey) + ' ' + str(i.get('id')) + ' ' + str(self.index) + ' ' + str('POINT(' + pointDataLon + ' ' + pointDataLat + ')') + ' ' + str(grid))
                print('\n')
                data = (region_pkey, i.get('id'), self.index, 'POINT(' + pointDataLon + ' ' + pointDataLat + ')', grid, )

            cur.execute(SQL, data)
            self.index += 1

        self.dbConnection.commit();
        cur.close()

    #TODO: Once posgGIS is working, remove this function and start using above version
    def insertGeoDataDummy(self, cde, region, grid=None):
        dictOfCSVData = cde.getCSVDict()
        assert(self.dbConnection is not None)
        cur = self.dbConnection.cursor();

        dummyIndex = 1
        for i in dictOfCSVData:
            SQL = "SELECT region_pkey FROM region WHERE region_abbv = 'NWCC';"
            #data = region
            cur.execute(SQL)
            # print(cur.fetchall())
            region_pkey = cur.fetchone()

            pointDataLat = i.get('lat')
            pointDataLon = i.get('long')

            if grid is None:
                SQL = "INSERT INTO model_grid_points (region_pkey, region_ref_number, national_ref_number, " \
                      "location) VALUES (%s, %s, %s, %s);"

                print(str(region_pkey) + ' ' + str(i.get('id')) + ' ' + str(self.index) + ' ' + str('POINT(' + pointDataLon + ' ' + pointDataLat + ')'))
                data = (region_pkey, i.get('id'), self.index, dummyIndex)
                dummyIndex += 1
            else:
                SQL = "INSERT INTO model_grid_points (region_pkey, region_ref_number, national_ref_number, " \
                      "location, regional_grid) VALUES (%s, %s, %s, ST_GeographyFromText(%s), %s);"

                print(str(region_pkey))
                print(str(i.get('id')))
                print(str(self.index))
                print(str('POINT(' + pointDataLon + ' ' + pointDataLat + ')'))
                print(str(grid))
                print(str(region_pkey) + ' ' + str(i.get('id')) + ' ' + str(self.index) + ' ' + str('POINT(' + pointDataLon + ' ' + pointDataLat + ')') + ' ' + str(grid))
                print('\n')
                data = (region_pkey, i.get('id'), self.index, 'POINT(' + pointDataLon + ' ' + pointDataLat + ')', grid, )

            cur.execute(SQL, data)
            self.index += 1

        self.dbConnection.commit();
        cur.close()

    ## This is used for inserting "general" data.
    #  tableName    string - the name of the table
    #  columns      array[string] - column names
    #  values       array[Any] - values to enter
    #  Note: types defined in array will be what's entered into database. This
    #  may or may not cause a problem if you're trying to insert odd or very
    #  specific types.
    def generalInsert(self, tableName, columns, values):
        sql = "INSERT INTO " + tableName + " ("
        assert(self.dbConnection is not None)
        cur = self.dbConnection.cursor()

        # build sql string from params. the column predicate works here because column names duplicates can't exist
        for i in columns:
            if i == columns[-1]:
                sql += i + ") VALUES ("
            else:
                sql += i + ", "
        for i in values:
            sql += self.__singleParens(i) + ", "
        # Once the string is build, strip off extra comma and whitespace and add closing parens. We have to do it this
        # way vs. the column predicate way as above because duplicate values may exist (and are allowed).
        sql = sql[0:-2] + ");"

        # Execute and catches errors, logging and moving on. This is primarily for duplicate entry attempts.
        try:
            cur.execute(sql)
        except Exception as e:
            self.log.write.error("In RecordKeeper: error while inserting - " + str(e))
            print(str(e))
            cur.close()

        self.dbConnection.commit()
        cur.close()


    def sql(self, sql):
        optionalReturn = None
        assert(self.dbConnection is not None)
        cur = self.dbConnection.cursor()

        try:
            cur.execute(sql)
            if sql.find("INSERT INTO") < 0:
                optionalReturn = cur.fetchall()
        except Exception as e:
            self.log.write.error("In RecordKeeper: error while inserting manually - " + str(e))
            print(str(e))
        self.dbConnection.commit()
        cur.close()
        return optionalReturn


    # -------------------------------- Private -------------------------------------

    ## This uses the "socket" library to get the current IP address of the computer.  It appends this
    #  to the connection_string.  Without the host I was having trouble connecting to the database.
    def __appendHostTo(self, connection_string):
        ipAddress = socket.gethostbyname(socket.gethostname())
        self.log.write.info("In RecordKeeper, IP address is: " + str(ipAddress))
        return connection_string + " host=" + str(ipAddress)

    ## This assists with building SQL strings from user input. It transforms the object being passed in
    #  into a string and verifies that it is enclosed in single quotes.
    def __singleParens(self, intOrStr):
        toRet = str(intOrStr)
        if re.match('^\'.*\'$', toRet) is not None:
            return toRet
        else:
            return "'" + toRet + "'"