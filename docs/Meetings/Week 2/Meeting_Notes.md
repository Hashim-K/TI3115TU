# Meeting Notes | 2021-09-13
*by A. Eyong*

### Calendar
- Discussed the method to be used for calendar importing; the Google Calendar API was picked as the best option as it has great documentation and is widely used.

### Scheduling Algorithm
- Proposed using a list containing time slot objects holding a taskID and a start and end time as attributes. These slots are ~ 10 minutes long. When they get occupied by an event, the taskID attribute will change to the taskID corresponding to the event. There will be certain taskIDs that are reserved for time that is not to be planned.

- The scheduling algorithm itself will schedule on *priority*, *deadline* of and other critera (time of day, etc.). The events to be scheduled are kept in a list that is therefore sorted by these criteria. [Not defined: How we will select from this list after we have 'filtered' for the criteria when considering a block of unallocated time Will it just go top-down ?]

### Organisational
Sprint weeks are defined to begin on Monday and end on Friday. Weekends are not considered within our sprints.

### GUI [Extra]
- PyQT5
- Dash Python
- PySimpleGUI

---
## This sprint (week 2)
- Data structure of tasks
- Framework for the GUI
- Initial implementation of the Google Calendar
- Familiarize everyone with Git


---
# Meeting Notes | 2021-09-15
*by A. Eyong*

## [TA Meeting Notes]
### Addition on the Requirements
Things that we require:
- Nonfunctional requirements
    - Measureable
    - Python version
    - Test Line Coverage

### Sprint
- Add sprint retrospective for last week
- [On data structures] Maybe use MySQL and Delft's own thing

---
