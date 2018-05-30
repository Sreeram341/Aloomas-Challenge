############################################################################################
#
# File Name : Rolling Average.py
# Author : Sreeram Pulavarthi
# Date: 05-22-2018
# Description of File:  Fetches the data from the SQL and converts the break down result to average
#                       retrieve data from database
#
#############################################################################################

import tkinter as tk
import datetime as dt
import tkinter.ttk as ttk


class convertTORollAvg():

    def __init__(self):
        self.newDict = {}
        self.insideKey = {}
        self.results = []

    def getValu(self, SQLresult): # gets the result set from database

        # Initialize variables
        self.toBeConv = SQLresult

        # Convert the list of values received from SQL query to Window query for finding the rolling average
        for i in self.toBeConv:
            key = i[0]
            valu = [{i[1]: i[2]}]
            if key in self.newDict: # If already key is present just add it
                self.newDict[key] += valu
            else: # If no key is available for the Type in current dictonary insert new key it
                self.newDict[key] = valu
        self.returnValu()



    def returnValu(self):

        print("###################################################################################################")
        print('{0:20} | {1:15} | {2:22} | {3:20}'.format("TYPE", "DATE", "NUMBER OF ENGAGEMENTS", "ROLLING 2 WEEK AVERAGE"))
        print("###################################################################################################")
        # Change the stored dictionary set to perform rolling average
        for jj in self.newDict.keys():

            Key = jj
            # Initialize variables
            DATES = list()
            COUNTS = list()
            dateFlatList = []
            countsFlatList = []
            properDateFrmt = []

            j = self.newDict[Key]

            for ii in range(len(j)):
                DATES.append(j[ii].keys())
                COUNTS.append(j[ii].values())
            for convertDateList in DATES:
                for dates in convertDateList:
                    dateFlatList.append(dates)
                    properDateFrmt.append(dt.datetime.strptime(dates, '%Y-%m-%d'))
            for convertCountList in COUNTS:
                for cnts in convertCountList:
                    countsFlatList.append(cnts)

            # Main logic which slides for previous 14 days for every Date

            for strtCntr in range(len(dateFlatList)):
                # Initalize variables for each Type from Dictionary
                avgCntr = 0
                CNTVAR = 0

                for dtt in range(14):  # Loops through all the days from 0-14
                    """
                    Below logic checks in the list of aggregated count's per day received from the SQL query and 
                    performs the rolling 2 weeks average count's of  for each day
                    """
                    # If the date is present in the query set received then get the corresponding value from counts list
                    requiredRangeDate = properDateFrmt[strtCntr] - dt.timedelta(days=dtt) # Current day - 14 days
                    if requiredRangeDate in properDateFrmt:
                        avgCntr += 1
                        CNTVAR += countsFlatList[properDateFrmt.index(requiredRangeDate)]
                        """ # checking wether the window is sliding in a proper way or not
                        print("Current Date is ", properDateFrmt[strtCntr]," loop Date is ", requiredRangeDate, " found in main list at position ",
                        properDateFrmt.index(requiredRangeDate),
                              "and the count value is ", countsFlatList[properDateFrmt.index(requiredRangeDate)])
                        """
                rollingAvg = CNTVAR / avgCntr

                self.results.append([Key, dateFlatList[strtCntr], countsFlatList[strtCntr], round(rollingAvg, 2)])

                print('{0:20} | {1:15} | {2:22d} | {3:20f}'.format(Key, dateFlatList[strtCntr], countsFlatList[strtCntr], round(rollingAvg, 2)))
                # print("break", "\n")
            # Clear all the values in the list for every run
            properDateFrmt.clear()
            countsFlatList.clear()
            dateFlatList.clear()
            DATES.clear()
            COUNTS.clear()

        self.gui_init()

    def gui_init(self):

        self.wind = tk.Tk()

        self.wind.title("Query Results")

        self.grd = tk.Frame(self.wind)

        self.grd.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        self.treeview = ttk.Treeview(self.grd)

        self.treeview['columns'] = ('TYPE', 'DATA', "NUMBER OF ENGAGEMENTS", "ROLLING 2 WEEK AVERAGE")

        self.treeview['displaycolumns'] = ('DATA', "NUMBER OF ENGAGEMENTS", "ROLLING 2 WEEK AVERAGE")

        self.treeview.heading('#0', text='TYPE')

        self.treeview.heading('DATA', text="DATA")

        self.treeview.heading('NUMBER OF ENGAGEMENTS', text='NUMBER OF ENGAGEMENTS')

        self.treeview.heading('ROLLING 2 WEEK AVERAGE', text='ROLLING 2 WEEK AVERAGE')

        self.treeview.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for data in self.results:
            self.treeview.insert('', tk.END, text=data[0], values=(data[0],data[1], data[2], data[3]))

        # Start the display window
        self.wind.mainloop()

    # Destructor for the class object
    def __del__(self):
        self.results.clear()