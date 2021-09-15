# Full Week Priority Algorithm
*by A. Eyong*
## 1.1 Introduction
For efficient handling of priorities and deadlines it may be better to import all the unallocated blocks of time for one whole week from the get-go. 

## 1.2 Proposed Algorithm
1. The algorithm first *imports* the unallocated blocks of time for the whole week.
2. It then *sorts* all **tasks** based on their deadlines and priority; during this process it groups the tasks with the same deadlines set together and sorts them based on which has the highest priority.
3. After it has done this *sorting* the *scheduling* starts. It starts at the **tasks** with the earliest deadline and the highest priority. It then runs the **subalgorithm** (1.2.1 Subalgorithm)
4. Repeat

### 1.2.1 Subalgorithm
When we are considering a task, each task, we do the following:
1. Using its deadline the days to consider are limited and therefore also the unallocated blocks we have to consider.
2. We then randomly assign **chunks** of the tasks to these unallocated blocks. To ensure a spread. [This random assignment does *should* not assign a chunk to the middle of an unused series of blocks, but should always start filling from the top.] 