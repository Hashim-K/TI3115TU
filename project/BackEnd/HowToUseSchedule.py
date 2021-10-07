import Schedule

# Schedule.presets can be used to set the different presets.
# Use 'Schedule.presets.PrintPresets()' to see what presets there are.
Schedule.presets.PrintPresets()

# To set the value for a preset use 'Schedule.presets.preset = value'.
Schedule.presets.dinner_time = '18:15'

# 'Schedule.schedule.SetUp()' is used to set up the schedule. This imports the events from the google calendar
# and creates the occurrences for the routine events based on the presets. These are then appended to the schedule.
Schedule.schedule.SetUp()

# Use 'Schedule.Display()' at any time after setting up the schedule to display it.
Schedule.Display()

# Use 'Schedule.event.PrintOccurrences' to get an overview of when the event occurs.
Schedule.routines.lunch.PrintOccurrences()

# Use 'Schedule.event.ChangeOccurrence(index, start_time=0, duration=0, end_time=0, day_add=0)' to change
# the occurrence of an event. Exactly two of the three boundary variables (start_time, duration, end_time) need
# to be defined to change the occurrence.
Schedule.routines.lunch.ChangeOccurrence(1, start_time='12:15', duration='0:30')
# The 'day_add=' variable is used for when the event starts or ends 1 or more days earlier or later.
# This applies for example when
Schedule.routines.sleep.ChangeOccurrence(3, start_time='0:45', end_time='12:00', day_add=1)

# Use 'Schedule.event.Occurrences.pop(index)' to remove an occurrence.
Schedule.routines.lunch.Occurrences.pop(5)

# After changes are made 'Schedule.schedule.Update' is used to update the schedule.
Schedule.schedule.Update()
Schedule.Display()
