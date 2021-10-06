import numpy as np


# Creates an array.
def CreateArray(number_of_columns, number_of_rows):
    return np.zeros(shape=(number_of_columns, number_of_rows)) - 1


# Converts a date to the format used by the schedule.
def DayAndSlot(datetime, day_zero, time_interval):
    day_zero = [int(day_zero.split('-')[2]),
                int(day_zero.split('-')[1]),
                int(day_zero.split('-')[0])]
    date = [int(datetime.split(',')[0].split('-')[0]),
            int(datetime.split(',')[0].split('-')[1]),
            int(datetime.split(',')[0].split('-')[2])]
    day = DaysSince2020(date) - DaysSince2020(day_zero)
    slot = round(
        (int(datetime.split(',')[1].split(':')[0]) * 60 + int(datetime.split(',')[1].split(':')[1])) / time_interval)
    return [day, slot]


# Converts a time to a slot.
def Slot(time, time_interval):
    return round((int(time.split(':')[0]) * 60 + int(time.split(':')[1])) / time_interval)


# Calculates the amount of days passed since 1-1-2000.
def DaysSince2020(date):
    year0 = 2020
    day, month, year1 = date[0], date[1], date[2]
    day_count = 0
    while year0 < year1:
        if year0 % 4 == 0 and (year0 % 100 != 0 or year0 % 400 == 0):
            day_count = day_count + 366
        else:
            day_count = day_count + 365
        year0 = year0 + 1

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year1 % 4 == 0 and (year1 % 100 != 0 or year1 % 400 == 0):
        days_in_month[1] = 29

    day_count = day_count + sum(days_in_month[0:month - 1])
    day_count = day_count + day - 1

    return day_count


# Checks on what day of the week a certain date is.
def CheckWhatDay(todate, mode):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mondate = [4, 1, 2021]
    if mode == 0:
        return (DaysSince2020(todate) - DaysSince2020(mondate)) % 7
    if mode == 1:
        return days[(DaysSince2020(todate) - DaysSince2020(mondate)) % 7]


# Calculates new date based on old date and days in between.
def XDaysLater(date, X):
    year, month, day = int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month[1] = 29
    day = day + X
    if day > days_in_month[month - 1]:
        day = day - days_in_month[month - 1]
        month = month + 1
        if month > 12:
            month = month - 12
            year = year + 1
    if day < 10:
        day = '0' + str(day)
    return str(year) + '-' + str(month) + '-' + str(day)


# Formats the date to be displayed in the form of 'January 1st'.
def DateFormat(date):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    month, day = int(date.split('-')[1]), int(date.split('-')[2])
    st, nd, rd = [1, 21, 31], [2, 22], [3, 23]
    if day in st:
        day = str(day) + 'st'
    elif day in nd:
        day = str(day) + 'nd'
    elif day in rd:
        day = str(day) + 'rd'
    else:
        day = str(day) + 'th'

    return months[month - 1] + ' ' + day


# Shuffles a list of colors for the google events to use.
def GetColors():
    color_list = ['#DAF0C2', '#B0DC7A', '#7FBD32', '#649528', '#477114', '#CBBA01', '#B6A702', '#A39600', '#8A7C00']
    return color_list


# Creates a list of ticks for x-axis of the schedule plot.
def CreateXTicks(day_zero, number_of_days):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    date = [int(day_zero.split('-')[2]), int(day_zero.split('-')[1]), int(day_zero.split('-')[0])]
    day = CheckWhatDay(date, 0)
    tick_list = []
    for i in range(number_of_days):
        if day + i > 6:
            day = day - 7
        tick_list.append(days[day + i])
    return tick_list


# Identifies blocks of empty slots in the schedule.
def EmptySlots(Schedule, number_of_slots):
    free_blocks = []
    free_block = []
    for day in range(len(Schedule)):
        for slot in range(len(Schedule[day])):
            if Schedule[day][slot] == -1:
                free_block.append([day, slot])
            else:
                if len(free_block) > 0 or (len(free_block) > 0 and slot == number_of_slots - 1):
                    free_block.append([day, slot])
                    free_blocks.append(free_block)
                    free_block = []
    for free_block in free_blocks:
        while len(free_block) > 2:
            free_block.pop(1)
    return free_blocks
