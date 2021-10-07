import random
import numpy as np

# Day and slot from date and time.
'''This function is used when importing events from the google calendar. (See ImportGoogleEvents() in Schedule)
The start and end times for an activity imported from the google calendar are in the form of '2021-10-06,17:21:00', 
while they need to be in the form of [day, slot] for the program to make an Event class object for them. 
This function uses the following inputs: 
datetime (the date and time in the form '2021-10-06,17:21:00'), day_zero (the first day of the week) 
and time_interval (the length of a time slot). 
It's output is the index of the day and slot in the schedule ([day, slot]).'''


def DayAndSlot(datetime, day_zero, time_interval):
    # This bit creates a list of the date of the first day of the week (day_zero). day_zero_lst = [day, month, year]
    day_zero_lst = [int(day_zero.split('-')[2]),
                    int(day_zero.split('-')[1]),
                    int(day_zero.split('-')[0])]
    # This bit creates a list of the date in the 'datetime' variable. date_lst = [day, month, year]
    date_lst = [int(datetime.split(',')[0].split('-')[0]),
                int(datetime.split(',')[0].split('-')[1]),
                int(datetime.split(',')[0].split('-')[2])]
    # This bit creates a list of the time in the 'datetime' variable. time_lst = [hour, minute]
    time_lst = [int(datetime.split(',')[1].split(':')[0]),
                int(datetime.split(',')[1].split(':')[1])]
    # This bit uses the function DaysSince2020 to see how many days are in between the first day of the week (day_zero)
    # and the date from the input to determine the index of the day in the schedule.
    day = DaysSince2020(date_lst) - DaysSince2020(day_zero_lst)
    # This bit converts the time to index of the slot in the schedule.
    slot = round((time_lst[0] * 60 + time_lst[1]) / time_interval)
    return [day, slot]


# Slot from time.
'''This function is used to convert a time in the form '17:43:00' to the index of the slot in the schedule. It is
used in the function RoutineEvents() in Schedule, where in converts the user's time preferences for the routine 
activities (sleep, morning routine, lunch and dinner) to the corresponding index of the slot in the schedule
so it can be used to create a list of occurrences for those activities for every day in the schedule.'''


def Slot(time, time_interval):
    return round((int(time.split(':')[0]) * 60 + int(time.split(':')[1])) / time_interval)


# Time from slot.
'''This function is used to get the time in the form 'hour:minute:second' to the index of the slot in the schedule.'''


def Slot2Time(slot, time_interval):
    return f'{int(slot * time_interval / 60)}:{int(slot * time_interval % 60)}:00'


# Check if year is leap year
'''This function is used to check if a year is a leap year. It is used by the functions DaysSince2020() and
XDaysLater(). Its input is a year and its output is True or False depending on whether the year is a leap year 
or not.'''


def LeapYear(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False


# Days since 01-01-2020.
'''This function calculates the amount of days since 1-1-2020. It is used by the functions DayAndSlot() and
CheckWhatDay() in order to determine the exact amount of days between 2 dates while taking leap years into account.
As input it takes a date as list ([day, month, year]) and as output it it gives the amount of days between 1-1-2020 and
the input date.'''


def DaysSince2020(date):
    year0 = 2020
    day, month, year1 = date[0], date[1], date[2]
    # The function uses the variable day_count to count up the days between the input date and 1-1-2020 through
    # several steps.
    day_count = 0
    # This bit accounts for the difference in years between the year of the date and 2020. For each year it goes
    # through, it adds 365 or 366 days to the day_count variable depending on whether a year is a leap year.
    while year0 < year1:
        # This if statement checks if the year is a leap year.
        if LeapYear(year0):
            day_count = day_count + 366
        else:
            day_count = day_count + 365
        year0 = year0 + 1
    # This bit gives a list of days per month. If the year is a leap year, the amount of days in february is set to 29.
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year1 % 4 == 0 and (year1 % 100 != 0 or year1 % 400 == 0):
        days_in_month[1] = 29
    # This bit accounts for the difference in months between the month of the date and January.
    day_count = day_count + sum(days_in_month[0:month - 1])
    # This bit accounts for the difference in days between the day of the date and the 1st.
    day_count = day_count + day - 1
    return day_count


# Checks what day of the week a date is.
'''This function checks what day of the week a certain date is and is used by the function CreateXTicks(). 
It does this by calculating the difference in days between the date (date) and a date know to be monday (mondate). 
It then calculates the remainder of this difference divided by 7. It follows that this remainder represents the day of 
the week (starting at 0 being Monday, 1 being Tuesday and so forth). The output is this number.'''


def CheckWhatDay(date):
    mondate = [4, 1, 2021]
    return (DaysSince2020(date) - DaysSince2020(mondate)) % 7


# Calculates new date based on old date and days in between.
'''This function determines the date of a day X days after another date. It is used by the functions Display() and 
ResolveOverlap() in Schedule. The inputs are date (the initial date in the form of a list ([day, month, year]) 
and X (the number of days between the initial date and the day for which the date is to be known.) The output is a
string of the date in the form 'day-month-year'.

Side note, I guess this function can be easily tested using the DaysSince2020() function, if that function has already 
been tested at least.'''


def XDaysLater(date, X):
    # This bit sets the variables year, month and day from the data in date.
    year, month, day = int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])
    # This bit gives a list of days per month. If the year is a leap year, the amount of days in february is set to 29.
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if LeapYear(year):
        days_in_month[1] = 29
    # This bit adds X amount of days to the day of the month.
    day = day + X
    # If day of the month now exceeds the amount of days in the month, it adjusts for that and adds 1 to the month.
    while day > days_in_month[month - 1]:
        day = day - days_in_month[month - 1]
        month = month + 1
        # If the month now exceeds the amount of months in a year, it adjusts for that and adds 1 to the year.
        if month > 12:
            month = month - 12
            year = year + 1
    return str(year) + '-' + str(month) + '-' + str(day)


# Formats the date to be displayed in the form of 'January 1st'.
'''This function converts a date to a clear readable format. (For example '10-23-2021' to 'September 23rd'. It is 
used by functions Display() and ResolveOverlap().'''


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


# Creates a list of ticks for x-axis of the schedule plot.
'''This function creates the ticks for the x-axis (the days representing the columns) for the displaying the schedule. 
It is used in the Display() function in Schedule. Its inputs are day_zero (the first day in the schedule in the form
'year-month-day') and number_of_days (the number of days in the schedule). Its output is a list of ticks for each of 
the columns in the displayed schedule.'''


def CreateXTicks(day_zero, number_of_days):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # This bit creates a list from the day_zero in the form of [day-month-year].
    date = [int(day_zero.split('-')[2]), int(day_zero.split('-')[1]), int(day_zero.split('-')[0])]
    # This bit checks on what day of the week day_zero is.
    day = CheckWhatDay(date)
    # This bit creates a list of the ticks and appends the names of all the days present in the schedule to it.
    tick_list = []
    for i in range(number_of_days):
        if day + i > 6:
            day = day - 7
        tick_list.append(days[day + i])
    return tick_list


# Identifies blocks of empty slots in the schedule.
'''This function checks which slots in the schedule are empty. It is used by the algorithm to determine in what time
 slot it can place task events. Its input is schedule array and its output is a list of the blocks of free spaces in
 the form [[[begin_day][begin_slot],[end_day][end_slot]], ... ]'''


def EmptySlots(schedule_array):
    number_of_slots = len(schedule_array[0])
    free_blocks = []
    free_block = []
    # This bit cycles through every slot in the schedule.
    for day in range(len(schedule_array)):
        for slot in range(len(schedule_array[day])):
            # This bit checks if a slot is empty.
            if schedule_array[day][slot] == -1:
                free_block.append([day, slot])
            else:
                # This bit checks if there are any slots appended to free_block or if there are any slots appended to
                # free_block and if the slot is the last slot of the day. If True, the slot is appended to free_block,
                # free_block is appended to free_blocks and free_block is set to an empty list.
                if len(free_block) > 0 or (len(free_block) > 0 and slot == number_of_slots - 1):
                    free_block.append([day, slot])
                    free_blocks.append(free_block)
                    free_block = []
    # This bit removes the slots in between the first and the last slot for each block of free slots so only the start
    # slot and the end slot remain.
    for free_block in free_blocks:
        while len(free_block) > 2:
            free_block.pop(1)
    return free_blocks
