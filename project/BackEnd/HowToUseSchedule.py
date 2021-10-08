import Schedule

# Schedule.presets can be used to set the different presets.
# Use 'Schedule.presets.PrintPresets()' to see what presets there are.
# Schedule.presets.PrintPresets()

# To set the value for a preset use 'Schedule.presets.preset = value'.
Schedule.presets.import_google = False

# 'Schedule.schedule.SetUp()' is used to set up the schedule. This imports the events from the google calendar
# and creates the occurrences for the routine events based on the presets. These are then appended to the schedule.
Schedule.schedule.SetUp()

# Use 'Schedule.Display()' at any time after setting up the schedule to display it.
Schedule.Display()

# Use 'Schedule.event.PrintOccurrences' to get an overview of when the event occurs.
# Schedule.routines.dinner.PrintOccurrences()

if Schedule.presets.import_google:
    # To remove an event, set the duration to '0:00'.
    Schedule.routines.dinner.EditOccurrence(2, start_time='0:00', duration='0:00')
    # Use 'Schedule.event.ChangeOccurrence(index, start_time=0, duration=0, end_time=0, add_day=0)' to change
    # the occurrence of an event. Exactly two of the three boundary variables (start_time, duration, end_time) need
    # to be defined to change the occurrence.
    Schedule.events[3].EditOccurrence(4, end_time='17:45', duration='0:45')
    # The 'day_add=' variable is used for when the event starts or ends 1 or more days earlier or later.
    # This applies for example when
    Schedule.routines.sleep.EditOccurrence(5, start_time='1:15', end_time='8:30', add_day=1)

    # After changes are made 'Schedule.schedule.Update' is used to update the schedule.
    Schedule.schedule.Update()
    Schedule.Display()

    # Use 'Schedule.schedule.ReturnEmpty()' to get the list of empty spaces.
    Schedule.schedule.PrintEmpty()

    # print(Schedule.schedule.ReturnEmpty())
