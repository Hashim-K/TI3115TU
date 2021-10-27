class TimeList:
    def __init__(self):
        self.timelist=[]

    def add_time(self, start_day, start_time, end_day, end_time):
        self.timelist.append([[start_day, start_time], [end_day, end_time]])

    def delete_time(self, start_day, start_time, end_day, end_time):
        for time in self.timelist:
            if time == [[start_day,start_time],[end_day, end_time]]:
                self.timelist.remove(time)

    def __str__(self):
        text_description = ""
        for time in self.timelist:
            text_description += ( str(time) + "\n")
        return text_description

    def times(self):
        return self.timelist