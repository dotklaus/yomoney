import pandas as pd

# custom modules
from utils import datetimeutils

def print_list_items(lst):
    for index, item in enumerate(lst):
        print(f"Item {index + 0}: {item}")


def Get_CSV_Metadata(filePath_p : str):
    try:
        with open(filePath_p, 'r', encoding='ISO-8859-1') as file:
            for i, line in enumerate(file,1):
                if i == 5:
                    return line
                    break
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {e}"

def DB_Process_CSV_Headers(filePath_p : str):

    headers = str(Get_CSV_Metadata(filePath_p)).split(";")
    creditIndex = headers.index("Credit")
    debitIndex = headers.index("Debit")

    return creditIndex, debitIndex 

def Read_Csv_File(filePath):

    # works for Deutsche Bank csv
    # df = pd.read_csv(filePath, skiprows=4, delimiter=";", skipfooter=1, engine='python')
    # encoding = 'latin-1'

    encoding = 'ISO-8859-1'
    creditIndex, debitIndex = DB_Process_CSV_Headers(filePath)
    df = pd.read_csv(filePath, skiprows=4, delimiter=";", skipfooter=1, encoding=encoding, engine='python')

    # format first two columns to dates
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], format='mixed').dt.date
    df.iloc[:,1] = pd.to_datetime(df.iloc[:,1], format='mixed').dt.date
    # df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], format='%d.%m.%Y').dt.date
    # df.iloc[:,1] = pd.to_datetime(df.iloc[:,1], format='%d.%m.%Y').dt.date

    # get some metedata
    firstDate = df.iloc[:,0:1].min()
    lasteDate = df.iloc[:,0:1].max()

    timeInterval = datetimeutils.Get_Months_In_Range(firstDate[0],lasteDate[0])

    # clean up columns
    columns = df.columns
    # print_list_items(columns)
    inPaymentsColID = columns[creditIndex]
    outPaymentsColID = columns[debitIndex]

    # german mode deutsche bank
    # df[inPaymentsColID] = df[inPaymentsColID].str.replace('.','').str.replace(',','.').fillna(0).astype(float)
    # df[outPaymentsColID] = df[outPaymentsColID].str.replace('.','').str.replace(',','.').fillna(0).astype(float)

    # englisch mode
    df[inPaymentsColID] = df[inPaymentsColID].str.replace(',','').fillna(0).astype(float)
    df[outPaymentsColID] = df[outPaymentsColID].str.replace(',','').fillna(0).astype(float)

    return df


