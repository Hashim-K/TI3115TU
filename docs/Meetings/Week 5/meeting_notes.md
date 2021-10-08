# Meeting Notes | 2021-10-4 | Week 5
*By R.E.M. Liu*
## Sprint planning
**Report**
- The deadline for the draft version of the report is Friday of this week, so writing the report will be the priority for the first half of the week.
- We need to work on the documentation of the code, so that it can be used in the report.
	- We listed which parts needed documentation: the GUI, the schedule set up, tasks, the scheduling algorithm
	- Each person will write the documentation for the code that they wrote, while one person writes the chapter on the requirements.

**Back end**
- Another goal for this week is to do more testing, but it has been decided to leave that mostly for the latter half of the week.
- Further coding has been put on hold.

# Meeting Notes | 2021-10-6 | week 5
*By R.E.M. Liu*
## TA meeting
- We gave a summary of what we were doing, which was mostly working on the report.
- The TA recommended that we can make use of **merge requests** more and leave comments.
- According to the planning for the project, this week we should have a "minimal working project", which factually we do not have yet, but the TA assessed that we were not behind, as we do already have many functions which will be needed for the core functionality, running the algorithm.
- Regarding testing, for the GUI, we can do manual tests. We can document it in the report as a table: write what we did, what we expected, and what the result was.
- The TA noted that our unit tests should be in a test folder, which we discovered had accidentally been deleted from our project. But that is not a problem and we made a new test folder.
- We mentioned that there was one pipeline error which we haven't been able to solve yet, relating to the import of PyQT5. The TA said she would ask the head TA about it.
## Group meeting
- We determined that since the Task code has already been tested, Teus' code could be tested next.
- There is a problem with the Google authorization: the socket does not close on exit and this causes the user to be unable to log in again.
	- We do not have an exact plan on how to fix this yet. Someone will have to do more research on the Google API to handle it. The problem only occurs sometimes. We might try to work on it later.
## Next group meeting plan
 - Everyone has expects to have written something for the report before the deadline on Friday, so we will also continue to work on software development.
 - Achere and Robin will start on building the GUI for the Google login and setting unavailable times after which the the schedule can be generated.
 - Teus has been writing a lot of documentation and is also polishing his code.
 - Nina will do testing on 'General.py'
 - Hashim is still working on the algorithm
# Meeting notes | 2021-10-08 | Week 5
*By R.E.M. Liu*

**Overview schedule set up**
- Teus demonstrated how his code worked, so that it is clear to everyone and the front-end can integrate it into the UI.
- There was discussion about the implementation, because the code did provide all the needed functionalities, but it was written in a somewhat "static" way. We had mentioned before that global variable were a concern, and he did make those part of classes to eliminate those. But some of the methods could be abstracted so that general 'events' can be created. In the end we proposed that no drastic changes were necessary, but Hashim will go over the code with Teus so that the the code may be made more "dynamic" and to facilitate integration with the UI.

**GUI demonstration**
- Achere and Robin demonstrated the new part of the GUI, where users will be able to connect their google account and set the unavailable times.
- Hashim mentioned that if one wants to rescale images, it is better to do it before importing it in python.

**Algorithm**
- Hashim gave a quick update on the algorithm and let the group know that the expected inputs are 1. the free time slots in the schedule and 2. all of the tasks from the JSON file.

**Other decisions**
 - We planned to hand in the draft report. At the moment it is lacking some content, such as the chapter on the software development process, but we thought to write it later and receive feedback on what we have so far. Hashim will still add his part and then submit it.
## To do list
 - We will merge the currently open front-end and back-end branches before the next sprint planning.
 - We will then continue working on the GUI and integrate the Google login and setting of unavailable times in the schedule.
 - We expect the algorithm to be done next week
 - We will continue testing
