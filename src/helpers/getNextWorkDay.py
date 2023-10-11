from datetime import date, datetime, timedelta
import holidays
from helpers import dateToBrFormat as dtbf

def getNextWorkDay(date, separator):
    br_holidays = holidays.country_holidays('BR')
    iso_date = datetime.strptime(date, "%d/%m/%Y")
    isWorkDay = False

    while (isWorkDay == False):
        isHoliday = br_holidays.get(iso_date)
        isSaturday = iso_date.weekday() == 5
        isSunday = iso_date.weekday() == 6

        if (isHoliday or isSaturday or isSunday):
            iso_date = iso_date + timedelta(days=1)
        else:
            isWorkDay = True

    return dtbf.dateToBrFormat(iso_date.date(), separator)