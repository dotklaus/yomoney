from datetime import date
from enum import Enum

# custom modules
from utils import mathutils

class TransactionType(Enum):
    INCOME = 1
    EXPENDITURE = 2
    TRANSFER = 3

    def __str__(self):
        return f'{self.name}: {self.value}'
    
class Catergories(Enum):
    MISC = 1
    RENT = 2
    SAVINGS = 3
    INSURANCE = 4
    GROCERIES = 5
    DM = 6
    ATM = 7
    TRAVEL = 8
    CHEMIST = 9
    COMMUNICATION = 9
    AMAZON = 10
    UTILITIES = 11
    SPORTS = 12
    DONATIONS = 13
    BANK = 14
    EATINGOUT = 15

    def __str__(self):
        return f'{self.name}: {self.value}'
    
    def Get_Label(self):
        return f'{self.name}'

class BalanceSheet:
    def __init__(self, name :str):
        self.m_name = name
        self.m_id = 1
        self.m_incomeList = []
        self.m_expenditureList = []

    def Register_Transactions(self, dataframe):    

        numberOfRows = dataframe.shape[0]
        columns = dataframe.columns

        dataframe = dataframe.sort_values(by=columns[0], ascending=True)
        
        for index, row in dataframe.iterrows():
            transaction = Create_Transaction(row, columns)

            if transaction.transactionType == TransactionType.INCOME:
                self.m_incomeList.append(transaction)
            if transaction.transactionType == TransactionType.EXPENDITURE:
                self.m_expenditureList.append(transaction)

    def Get_Total_Income(self):    
        totalIncome = 0.0;
        for iTransaction in self.m_incomeList:
            totalIncome += iTransaction.amount
        return totalIncome

    def Get_Total_Expenditure(self):    
        totalExpenditure = 0.0;
        for iTransaction in self.m_expenditureList:
            totalExpenditure += iTransaction.amount
        return totalExpenditure

class Transaction:
    def __init__(self, name: str, amount: float, transactionType: TransactionType, beneficiary: str, executionDate: date, paymentDetails: str):
        self.name = name
        self.amount = amount
        self.transactionType = transactionType
        self.beneficiary = beneficiary
        self.paymentDetails = paymentDetails
        self.executionDate = executionDate
        self.searchString = str(beneficiary) + str(paymentDetails)
        self.category = Catergories.MISC
    
    def display_transaction(self):
        print("Name:", self.name)
        print("Amount:", self.amount)
        print("Type:", self.transactionType)
        print("Beneficiary:", self.beneficiary)
        print("Payment Details:", self.paymentDetails)
        print("Execution Date:", self.execution_date)
        print("Category:", self.category)

    def __str__(self):
        return f"Name = {self.name}, Amount = {self.amount}, Type = {self.transactionType}, Beneficiary = {self.beneficiary}, PaymentDetails = {self.paymentDetails}"


def Create_Transaction(dfRow, dfColumns):

    colNames = [ i for i in dfColumns ]
    dateIndex = colNames.index("Booking date")
    creditIndex = colNames.index("Credit")
    debitIndex = colNames.index("Debit")
    beneficiaryIndex = colNames.index("Beneficiary / Originator")
    paymentDetailsIndex = colNames.index("Payment Details")

    date = dfRow[dfColumns[dateIndex]]  
    expenditure = dfRow[dfColumns[debitIndex]]  
    income = dfRow[dfColumns[creditIndex]]  
    beneficiary = dfRow[dfColumns[beneficiaryIndex]]
    paymentDetails = dfRow[dfColumns[paymentDetailsIndex]]

    # categorize the transaction Type
    if mathutils.Check_Equal(expenditure, 0.0) :
        assert(income > 0.0)
        return Transaction("income", income, TransactionType.INCOME, beneficiary, date, paymentDetails)

    if mathutils.Check_Equal(income, 0.0) :
        assert(expenditure < 0.0)
        return Transaction("expenditure", expenditure, TransactionType.EXPENDITURE, beneficiary, date, paymentDetails)
    

def Get_Item_Category(string_p, dict_p):
    for key in dict_p.keys():
        if key in string_p:
            # print(string_p, dict_p[key])
            return dict_p[key]
    # print(string_p)
    return Catergories.MISC

class Categorizer:
    def __init__(self):
        self.categorized = 0
        self.uncategorized = 0

        self.categoryDictionary = {"rewe" : Catergories.GROCERIES,
                                   "kaufland" : Catergories.GROCERIES,
                                   "edeka" : Catergories.GROCERIES,
                                   "aldi" : Catergories.GROCERIES,
                                   "denns bio" : Catergories.GROCERIES,
                                   "dm fil" : Catergories.DM,
                                   "allguth" : Catergories.TRAVEL,
                                   "tankautomat" : Catergories.TRAVEL,
                                   "jet dankt" : Catergories.TRAVEL,
                                   "avia" : Catergories.TRAVEL,
                                   "swmmvg" : Catergories.TRAVEL,
                                   "docmorris" : Catergories.CHEMIST,
                                   "winsim" : Catergories.COMMUNICATION,
                                   "vodafone": Catergories.COMMUNICATION,
                                   "spotify": Catergories.COMMUNICATION,
                                   "siedlungsbau bayern": Catergories.RENT,
                                   "amazon": Catergories.AMAZON,
                                   "eswe": Catergories.UTILITIES,
                                   "gothaer": Catergories.INSURANCE,
                                   "axa versicherung": Catergories.INSURANCE,
                                   "sparkassen direktversicherung": Catergories.INSURANCE,
                                   "kp sport": Catergories.SPORTS,
                                   "freie evangelische": Catergories.DONATIONS,
                                   "dauerauftrag etf": Catergories.SAVINGS,
                                   "restaurant": Catergories.EATINGOUT,
                                   "lieferandobes": Catergories.EATINGOUT,
                                   "riedmair gmbh": Catergories.EATINGOUT,
                                   }

    def Categorize(self, expenditureList):
        for item in expenditureList:
            item.category = Get_Item_Category(item.searchString.lower(), self.categoryDictionary)


