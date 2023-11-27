import pandas as pd

# custom modules
from utils import datetimeutils
from readers import csvreader
from visuals import datavisualizer, pdfcreator
import transaction

def main():
    inputFile = "./data/example.csv"
    print(f"Processing csv file {inputFile}")

    # read input
    df = csvreader.Read_Csv_File(inputFile)
    print(f"Dataset shape {df.shape}")

    # get dataframe meta data
    # time span
    columns = df.columns
    minDate = df[columns[0]].min()
    maxDate = df[columns[0]].max()
    months = datetimeutils.Get_Months_In_Range(minDate, maxDate)

    sheet1 = transaction.BalanceSheet("test")
    sheet1.Register_Transactions(df)
    print(f"Total income {sheet1.Get_Total_Income(): .2f}")
    print(f"Total expenditure {sheet1.Get_Total_Expenditure(): .2f}")

    visualizer = datavisualizer.DataVisualizer(sheet1.m_incomeList, sheet1.m_expenditureList)

    # Scenario 1: every month on its own, detailed (categorized) or summarized
    ### visualize the different months
    # for imonth in months:
    #     visualizer.Plot_Monthly_Balance(imonth)

    # visualizer.Plot_Monthly_Balance(months[2])

    # Scenario 2: overview for months over a range, detailed or summarized
    ## visualize all months
    # visualizer.Plot_Summary(months)

    # Scenario 3: overview how much we spend vs how much we earn
    # visualizer.Plot_General_Balance()



    # Scenario 4: detailed monthly balance
    pdfCreator = pdfcreator.PdfCreator("test.pdf")
    for imonth in months[:1]:
        visualizer.Plot_Monthly_Balance_Detailed(imonth)
        pdfCreator.Save_Current_Figure_To_Pdf()
        pdfCreator.Add_Page()
    pdfCreator.Finalize()




if __name__ == "__main__":
    main()
