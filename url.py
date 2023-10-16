from datetime import date, datetime, timedelta
import holidays
from holidays import countries

br_holidays = holidays.BR()
iso_date = datetime.strptime("25/12/2023", "%d/%m/%Y")
isWorkDay = False

while (isWorkDay == False):
    isHoliday = br_holidays.get(iso_date)
    isSaturday = iso_date.weekday() == 5
    isSunday = iso_date.weekday() == 6

    if (isHoliday or isSaturday or isSunday):
        iso_date = iso_date + timedelta(days=1)
    else:
        isWorkDay = True

print(iso_date)