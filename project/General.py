import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random


# General Functions

def Time2Slot(time, time_interval):
    minute = time[1] * 60 + time[2]
    return [time[0], round(minute / time_interval)]


def DayAndSlot(datetime,day_zero,time_interval):
    day_zero = [int(day_zero.split('-')[2]),
                int(day_zero.split('-')[1]),
                int(day_zero.split('-')[0])]
    date = [int(datetime.split(',')[0].split('-')[0]),
            int(datetime.split(',')[0].split('-')[1]),
            int(datetime.split(',')[0].split('-')[2])]
    day = DaysSince2000(date)-DaysSince2000(day_zero)
    slot = round((int(datetime.split(',')[1].split(':')[0])*60+int(datetime.split(',')[1].split(':')[1]))/time_interval)

    return [day,slot]


def DaysSince2000(date):
    year0 = 2000
    day,month,year1 = date[0],date[1],date[2]
    day_count = 0
    while year0 < year1:
        if year0%4 == 0 and (year0%100 != 0 or year0%400 == 0):
            day_count = day_count + 366
        else:
            day_count = day_count + 365
        year0 = year0+1

    DaysInMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
    if year1%4 == 0 and (year1%100 != 0 or year1%400 == 0):
        DaysInMonth[1] = 29

    day_count = day_count + sum(DaysInMonth[0:month-1])
    day_count = day_count + day - 1

    return day_count


def CheckWhatDay(todate,mode):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mondate = [4,1,2021]
    if mode == 0:
        return (DaysSince2000(todate)-DaysSince2000(mondate))%7
    if mode == 1:
        return days[(DaysSince2000(todate)-DaysSince2000(mondate))%7]


def XDaysLater(date,X):
    year,month,day = int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2])
    days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    if year%4 == 0 and (year%100 != 0 or year%400 == 0):
        days_in_month[1] = 29
    day = day + X
    if day > days_in_month[month-1]:
        day = day - days_in_month[month-1]
        month = month + 1
        if month > 12:
            month = month - 12
            year = year + 1
    if day < 10:
        day = '0'+str(day)
    return str(year)+'-'+str(month)+'-'+str(day)


def DateReformat(date):
    months = ['Januari','Februari','March','April','May','June','July','August','September','October','November','December']
    month,day = int(date.split('-')[1]),int(date.split('-')[2])
    st,nd,rd = [1,21,31],[2,22],[3,23]
    if day in st:
        day = str(day)+'st'
    elif day in nd:
        day = str(day)+'nd'
    elif day in rd:
        day = str(day)+'rd'
    else:
        day = str(day)+'th'

    return months[month-1]+' '+day


def GetColors():
    hex = ['#0072B5','#F5DF4D','#9BB7D4','#E9897E','#A0DAA9','#00A170','#926AA6','#D2386C']
    random.shuffle(hex)
    return hex


# Functions for the Schedule

def CreateSchedule(TI,Ndays,number_of_slots):
    TI = 5  # Time interval in minutes [1,5,10,15,20,30,40,45,60]
    return np.zeros(shape=(Ndays, number_of_slots)) - 1


def CreateXTicks(day_zero,number_of_days):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    date = [int(day_zero.split('-')[2]),int(day_zero.split('-')[1]),int(day_zero.split('-')[0])]
    day = CheckWhatDay(date,0)
    tick_list = []
    for i in range(number_of_days):
        if day + i > 6:
            day = day - 7
        tick_list.append(days[day+i])
    return tick_list


def EmptySlots(Schedule,number_of_slots):
    FreeBlocks = []
    FreeBlock = []
    for day in range(len(Schedule)):
        for slot in range(len(Schedule[day])):
            if Schedule[day][slot] == -1:
                FreeBlock.append([day, slot])
            else:
                if len(FreeBlock) > 0 or (len(FreeBlock) > 0 and slot == number_of_slots - 1):
                    FreeBlock.append([day, slot])
                    FreeBlocks.append(FreeBlock)
                    FreeBlock = []
    for FreeBlock in FreeBlocks:
        while len(FreeBlock) > 2:
            FreeBlock.pop(1)
    return FreeBlocks



