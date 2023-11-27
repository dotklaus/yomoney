from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

def Get_Months_In_Range(startDate, endDate):
    months = []
    currentDate = startDate.replace(day=1)

    while currentDate <= endDate:
        months.append(currentDate.strftime("%B %Y"))
        currentDate += relativedelta(months=1)

    return months

def Get_Month_Bounds(monthYearString_p):

    # convert string to dateTime object
    dateObject = parse(timestr=monthYearString_p)

    firstDay = dateObject.replace(day=1)

    nextMonth = firstDay.replace(month=firstDay.month + 1, day=1)
    lastDay = nextMonth - timedelta(days=1)

    return firstDay, lastDay

def Get_Extended_Month_Bounds(monthYearString_p, band_p = 1):

    # convert string to dateTime object
    dateObject = parse(timestr=monthYearString_p)

    firstDay = dateObject.replace(day=1) - timedelta(band_p)

    nextMonth = firstDay.replace(month=firstDay.month + 2, day=1)
    lastDay = nextMonth + timedelta(days=(band_p - 1))

    return firstDay, lastDay

