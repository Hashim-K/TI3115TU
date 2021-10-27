import time
import datetime
from math import floor

from project.BackEnd.Preset import Presets


class TimeObject:
    def __init__(self, dayzero, day:int, timeslot:int):
        presets = Presets()
        timeinterval = presets.time_interval
        timeremaining=(timeslot*timeinterval)%(60*24)
        h_remaining=floor(timeremaining/60)
        m_remaining=timeremaining%60
        if h_remaining<10:
            h="0"+str(h_remaining)
        else:
            h=str(h_remaining)
        if m_remaining<10:
            m="0"+str(m_remaining)
        else:
            m=str(m_remaining)
        d = datetime.timedelta(days=day, minutes=timeinterval*timeslot)
        dt = datetime.date.fromisoformat(dayzero) + d
        self.dateTime = dt.strftime("%Y-%m-%dT"+h+":"+m)
        self.timeZone = time.strftime("%z", time.gmtime())


def str_init(dateTime:str, timeZone:str):
    t = TimeObject(str(datetime.date.today()), 0, 0)
    t.dateTime = dateTime
    t.timeZone = timeZone
    return t
