from math import floor
from project.BackEnd.Preset import Presets


class TimeList:
    def __init__(self):
        self.timelist=[]

    def add_time(self, start_day, start_time, end_day, end_time):
        self.timelist.append([[start_day, start_time], [end_day, end_time]])


    def add_duration(self, start_day, start_time, duration):
        presets = Presets()
        end_time = int(start_time+(duration-1) % (1440/presets.time_interval))
        end_day = start_day+floor((duration-1)/(1440/presets.time_interval))
        if end_time > 1440/presets.time_interval - 1:
            end_time -= 1440/presets.time_interval
            end_day += 1
        self.timelist.append([[start_day, start_time], [end_day, int(end_time)]])

    def delete_time(self, start_day, start_time, end_day, end_time):
        for time in self.timelist:
            if time == [[start_day, start_time], [end_day, end_time]]:
                self.timelist.remove(time)

    def delete_duration(self, start_day, start_time, duration):
        presets = Presets()
        end_time = int(start_time + (duration - 1) % (1440 / presets.time_interval))
        end_day = start_day + floor((duration - 1) / (1440 / presets.time_interval))
        if end_time > 1440 / presets.time_interval - 1:
            end_time -= 1440/presets.time_interval
            end_day += 1
        for time in self.timelist:
            if time == [[start_day, start_time], [end_day, end_time]]:
                self.timelist.remove(time)

    def __str__(self):
        text_description = ""
        for time in self.timelist:
            text_description += ( str(time) + "\n")
        return text_description

    def times(self):
        return self.timelist