import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime

# custom modules
from utils import datetimeutils, plotutils
import transaction

def Get_Time_Indices_In_Range(timeData, startDate, endDate):
    # Convert dates to numerical values for comparison
    numericDates = np.array([(date - timeData[0]).total_seconds() for date in timeData])
    startNumeric = (startDate - timeData[0]).total_seconds()
    endNumeric = (endDate - timeData[0]).total_seconds()
    
    # Find the indices that lie between the two dates
    indices = np.where((numericDates >= startNumeric) & (numericDates <= endNumeric))[0]
    return indices

class CategoryPlotter:
    def __init__(self, expenditureDates_p):
        self.uniqueDates = np.unique(expenditureDates_p)
        self.categoryDict = {}

    def Register_Category(self, expenditureList_p, name_p):
        entries = [ item for item in expenditureList_p if item.category == name_p ]
        amounts = [ np.abs(item.amount) for item in entries]
        dates = [ item.executionDate for item in entries ]
        
        dateMapping = [ np.where(self.uniqueDates == item)[0][0] for item in dates ]
        mappedAmounts = np.zeros(len(self.uniqueDates))
        for i,iEntry in enumerate(dateMapping):
            mappedAmounts[iEntry] += amounts[i]

        self.categoryDict[name_p.Get_Label()] = mappedAmounts 

    def Populate_Plot(self, ax_p, monthYearString_p):

        # customPalette = sns.color_palette("tab20c",18)
        customPalette = plotutils.Get_Custom_Colormap()

        totalSum = 0
        bottom = np.zeros(len(self.uniqueDates))
        for i, (setLabel, setData) in enumerate(self.categoryDict.items()):
            sum = np.sum(setData)
            totalSum += sum
            p = ax_p.bar(self.uniqueDates, setData, width=0.8, align='center', label=f"{setLabel}:{sum:8.2f}€", bottom=bottom, color=customPalette[i])
            bottom += setData
        ax_p.set_title(f"{monthYearString_p}: expenditure {totalSum: 8.2f}€")

class DataVisualizer:
    def __init__(self, incomeList, expenditureList):
        self.incomeDates = np.array([ item.executionDate for item in incomeList])
        self.income = np.abs(np.array([ item.amount for item in incomeList]))
        self.expenditureDates = np.array([ item.executionDate for item in expenditureList])
        self.expenditure = np.abs(np.array([ item.amount for item in expenditureList]))
        self.expenditureList = np.array(expenditureList)

        numIncEntries = self.income.shape[0]
        numExpEntries = self.expenditure.shape[0]

        self.fastTimeArray = []
        self.interpolationIndices = []
        if (numExpEntries > numIncEntries):

            # Convert datetime objects to numerical values for interpolation
            self.fastTimeArray = np.array([(date - self.incomeDates[0]).total_seconds() for date in self.incomeDates])
            self.baseTime = self.incomeDates[0]
            self.interpolationIndices = np.array([ self.Get_Time_Index(date) for date in self.expenditureDates ])

    def Get_Time_Index(self, targetTime):
        maxLength = self.fastTimeArray.shape[0]
        index = np.searchsorted(self.fastTimeArray, (targetTime - self.baseTime).total_seconds())
        if index >= maxLength:
            index = maxLength - 1
        return index

    def Interpolate_Arrray(self, array):
        return np.array([ array[idx] for idx in self.interpolationIndices ])

    def Plot_General_Balance(self):

        cumulativeIncome = np.cumsum(self.income)
        cumulativeExpenditure = np.cumsum(self.expenditure)
        f, ax = plt.subplots()

        ax.plot(self.incomeDates, cumulativeIncome)
        ax.plot(self.expenditureDates, cumulativeExpenditure)
        # balance = self.Interpolate_Arrray(cumulativeIncome) - cumulativeExpenditure
        # ax.plot(self.expenditureDates, balance)

        # plot settings
        ax.xaxis.set_major_formatter(plotutils.Get_Date_Formatter())
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def Plot_Monthly_Balance(self, monthYearString_p):

        # Specify the two dates
        startDate, endDate = datetimeutils.Get_Month_Bounds(monthYearString_p)
        startDate = startDate.date()
        endDate = endDate.date()
        
        expIndices = Get_Time_Indices_In_Range(self.expenditureDates, startDate, endDate) 
        incIndices = Get_Time_Indices_In_Range(self.incomeDates, startDate, endDate) 

        f, ax = plt.subplots()
        # ax.plot(self.expenditureDates[indices], self.expenditure[indices])
        ax.bar(self.expenditureDates[expIndices], self.expenditure[expIndices], align='center', width=0.8, color='r')
        ax.bar(self.incomeDates[incIndices], self.income[incIndices], align='center', width=0.8, color='g')
        ax.set_title(f"{monthYearString_p}")

        # plot settings
        # ax.xaxis.set_major_formatter(plotutils.Get_Date_Formatter())
        # ax.set_yscale('log')
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def Plot_Monthly_Balance_Detailed(self, monthYearString_p):

        # Specify the two dates
        startDate, endDate = datetimeutils.Get_Month_Bounds(monthYearString_p)
        startDate = startDate.date()
        endDate = endDate.date()
        
        expIndices = Get_Time_Indices_In_Range(self.expenditureDates, startDate, endDate) 
        incIndices = Get_Time_Indices_In_Range(self.incomeDates, startDate, endDate) 

        # sort
        categorizer = transaction.Categorizer()
        categorizer.Categorize(self.expenditureList[expIndices]) 

        categoryPlotter = CategoryPlotter(self.expenditureDates[expIndices])

        f, ax = plt.subplots()

        # register categories
        for enumItem in transaction.Catergories:
            categoryPlotter.Register_Category(self.expenditureList[expIndices], enumItem)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.RENT)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.GROCERIES)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.DM)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.COMMUNICATION)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.TRAVEL)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.AMAZON)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.UTILITIES)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.INSURANCE)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.SPORTS)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.SAVINGS)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.DONATIONS)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.EATINGOUT)
        # categoryPlotter.Register_Category(self.expenditureList[expIndices], transaction.Catergories.NONE)
        categoryPlotter.Populate_Plot(ax, monthYearString_p)
        # ax.set_yscale('log')

        ## plot settings
        # Retrieve existing legend handles and labels
        # handles, labels = plt.gca().get_legend_handles_labels()
        
        # newHandle = mpatches.Patch(color='gray', label='RENT', alpha=0.5)
        
        # Add the new handle to the beginning of the handles list
        # labels.insert(0, "RENT")
        # handles.insert(0, newHandle)
        
        # Update the legend with the modified handles and labels
        # legend = plt.legend(handles, labels)
        # plt.setp(legend.get_texts()[0], color = "gray")

        plt.xticks(rotation=45, ha='right')
        monthBounds = datetimeutils.Get_Extended_Month_Bounds(monthYearString_p)
        ax.set_xlim(monthBounds[0], monthBounds[1])
        print(monthBounds)

        plt.legend()
        # plt.show()


    def Plot_Summary(self, months_p):

        f, ax = plt.subplots()
        expenditureList = []
        incomeList = []

        for imonth in months_p:
            startDate, endDate = datetimeutils.Get_Month_Bounds(imonth)
            startDate = startDate.date()
            endDate = endDate.date()
            
            expIndices = Get_Time_Indices_In_Range(self.expenditureDates, startDate, endDate) 
            incIndices = Get_Time_Indices_In_Range(self.incomeDates, startDate, endDate) 

            expenditureList.append(np.sum(self.expenditure[expIndices]))
            incomeList.append(np.sum(self.income[incIndices]))

        # plot settings
        xAxis = np.arange(len(months_p))

        ax.bar(xAxis - 0.2, expenditureList, 0.4, label = 'Expenditure')
        ax.bar(xAxis + 0.2, incomeList, 0.4, label = 'Income')
        plt.xticks(xAxis, months_p, rotation=45, ha='right')
        plt.legend()
        plt.show()

