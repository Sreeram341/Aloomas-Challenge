############################################################################################
#
# File Name : Data_Capture.py
# Author : Sreeram Pulavarthi
# Date: 05-21-2018
# Description of File:  Retrieves data from the engagements URL,
#                       Creates PSV file by extracting data from URL by updating offset
#                       Inserts data into database
#                       Retrieves the query results and displays data
#############################################################################################

import requests as r
import json
import datetime as dt
# Import Data Access Layer
import Json_DAL as DAL

# Initialize Variables

# File to be generated out with pipe separated value
OutFile = "jsonConverted.psv"

# Open the file in write mode and append header
OF = open(OutFile, "w")

Header = "Id|PortalId|Active|CreatedTime|OwnerId|CreatedBy|Type\n"

# write Header to file

OF.write(Header)

# initialize the URL
engagement_url = "https://api.hubapi.com/engagements/v1/engagements/paged?hapikey=demo&limit=200&offset="


class engagementsCapture():
    # Constructor for the class
    def __init__(self):
        # initialize the Data access layer class
        self.dal = DAL.JsonDAL()

    # convert the unix timstamp format to readable data
    def convertTime(self, time):
        s = time / 1000.0
        return dt.datetime.fromtimestamp(s).strftime('%Y-%m-%d')

    def showValues(self):
        # Queries the data inserted in db and prints the values accordingly
        self.dal.getDataQuery()

    # create function to extract engagements out of httpResponse and add it to file object

    def extract_data(self, offset):
        # get the http response
        httpResponse = r.get(engagement_url + str(offset))

        # convert to Json object on the response received form URL
        jsonData = json.loads(httpResponse.content)

        # Check if data end or not
        x = jsonData['hasMore']
        new_offset = jsonData['offset']

        if x == True: # If response from the URL is good continue
            print("Data is being loaded into table and file, please wait for the results", "\n")

            for i in jsonData['results']: # Extract values from the Json file and write it into a PSV file
                x = i['engagement']
                # print(x)
                Id = x['id']
                PortalId = x['portalId']
                Active = (1 if x['active'] else 0)
                CreatedTime = self.convertTime(x['createdAt'])
                if "ownerId" in x:
                    OwnerId = x['ownerId']
                else:
                    OwnerId = 0
                if "createdBy" in x:
                    CreatedBy = x['createdBy']
                else:
                    CreatedBy = 0

                Type = x['type']

                # Creates single line string to output file
                NewLine = str(Id) + "|" + str(PortalId) + "|" + str(Active) + "|" + CreatedTime + "|" + str(
                    OwnerId) + "|" + str(CreatedBy) + "|" + Type + "\n"

                # Creates a dictionary file to insert records into SQL
                Row_dict = {'Id': Id, 'PortalId': PortalId, 'Active': Active, 'CreatedTime': CreatedTime, 'OwnerId': OwnerId, 'CreatedBy': CreatedBy, 'Type': Type}

                # Function call to DAL
                self.dal.insert_data(Row_dict)

                # Appending each line extracted from Json file
                OF.write(NewLine)

            self.extract_data(new_offset)
        else:
            print("No Data/Response from the URL")


if __name__ == '__main__':
    ec = engagementsCapture()
    ec.extract_data(3981023) # Begin fetching the data from the offset value
    ec.showValues()
