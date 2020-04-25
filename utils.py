from builtins import range
from datetime import date, timedelta
from enum import Enum

def count_days(date_start, date_end):
    return (date_end - date_start).days + 1

def is_weekend(day):
    SATURDAY = 5
    SUNDAY = 6
    return (day.weekday() == SATURDAY or day.weekday() == SUNDAY)  

def build_days_range(date_start, date_end):
    count = count_days(date_start, date_end)
    days = []
    for i in range(count):
        if not is_weekend(date_start):
            days.append(date_start)
        date_start = date_start + timedelta(1)
    return days

if __name__ == "__main__":
    pass