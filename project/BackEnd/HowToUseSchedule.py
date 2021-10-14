from project.BackEnd import Schedule

blocks = [('Sleep', 0, '0:00', '7:30')]
for day in range(Schedule.presets.number_of_days):
    blocks.append(('Sleep', day, '23:30', '8:00'))
    blocks.append(('Lunch', day, '12:30', '0:45'))
    blocks.append(('Dinner', day, '18:30', '1:15'))

# Schedule.ImportGoogleEvents()

run = True
if run:
    Schedule.GetEvents()

run = False
if run:
    Schedule.SetSleep()
    Schedule.SetLunch()
    Schedule.SetDinner()
    for block in blocks:
        Schedule.AddOccurrence(Schedule.id_dict[block[0]], block[1], block[2], block[3])
    Schedule.SetMorningRoutine()

Schedule.StoreEvents()

# Schedule.ClearEvents()

Schedule.schedule.Update()

Schedule.SaveImage()

