############################################################################################
#
# File Name : Json_DAL.py
# Author : Sreeram Pulavarthi
# Date: 05-21-2018
# Description of File:  Creates a database connection and creates the methods to insert data and
#                       retrieve data from database
#
#############################################################################################

import mysql.connector as ms
import Rolling_Average as RA

# Initialize connection

Username = "tester"
Password = "tester1"
Hostname = "127.0.0.1"
Database = "sys"


class JsonDAL():

    # Constructor for the current class
    def __init__(self):
        self.is_conn_open = False
        # Creates the object of helper class
        self.ra = RA.convertTORollAvg()
        self.__connect_()

    # Private Method connect to the database
    def __connect_(self):
        if not self.is_conn_open:
            self.conn = ms.connect(user=Username, password=Password, host=Hostname, database=Database)

            # To create a new row factory

            # To create new cursor
            self.SQL_CUR = self.conn.cursor()

            self.is_conn_open = True

    # Insert data read from Json file from end point link

    def insert_data(self, rowDict):

        # print(rowDict)

        insertStmt = """INSERT INTO Engagement_Data (Id,PortalId,Active,CreatedTime,OwnerId,CreatedBy,Type)
                     VALUES(%(Id)s,%(PortalId)s,%(Active)s,%(CreatedTime)s,%(OwnerId)s,%(CreatedBy)s,
                     %(Type)s)"""
        try:
            self.SQL_CUR.execute(insertStmt, rowDict)
            self.conn.commit()

            # Checks for duplicate entry
        except ms.IntegrityError as err:
            print("Error: {}".format(err))

    def getDataQuery(self):

        selectStmt = """
                            SELECT TYPE,CAST(CREATEDTIME AS CHAR),COUNT(ID) AS CNT
                            FROM Engagement_Data
                            GROUP BY TYPE,CREATEDTIME 
                            ORDER BY 1 ASC, 2 DESC       
                        """

        try:
            self.SQL_CUR.execute(selectStmt)
            self.ra.getValu(self.SQL_CUR.fetchall())

            # Checks for any sort of data error any raises exception
        except ms.DataError as err:
            print("Error: {}".format(err))

    # Private Method disconnect to the database
    def close_connection(self):
        if self.is_conn_open:
            self.conn.shutdown()
            self.is_conn_open = False

    # Destructor for the class object
    def __del__(self):
        self.close_connection()
