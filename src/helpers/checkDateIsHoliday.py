from datetime import date, datetime
import holidays

def checkDateIsHoliday(date):
    br_holidays = holidays.country_holidays('BR')
    iso_date = datetime.strptime(date, "%d/%m/%Y")
    holiday = br_holidays.get(iso_date)
    if (holiday):
        return holiday
    else:
        return False