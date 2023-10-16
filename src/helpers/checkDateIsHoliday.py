from datetime import date, datetime
import holidays
from holidays import countries

def checkDateIsHoliday(date):
    br_holidays = holidays.BR()
    iso_date = datetime.strptime(date, "%d/%m/%Y")
    holiday = br_holidays.get(iso_date)
    if (holiday):
        return holiday
    else:
        return False