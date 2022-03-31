from math import gcd
import sched
import PeriodicTask
import SimulationSchedule

# Set up sample tasks
task1 = PeriodicTask.PeriodicTask(1,20,0,15,3)
task2 = PeriodicTask.PeriodicTask(2,5,0,4,2)
task3 = PeriodicTask.PeriodicTask(3,10,0,3,2)
taskPool = []
taskPool.append(task1)
taskPool.append(task2)
taskPool.append(task3)

# 1 is FCFS, 2 is RM, 3 is DM, 4 is EDF, and 5 is LST
schedulingAlgo = 4

# Sorting Functions
def sortPeriod(task):
    return task.period

def sortReadyTime(task):
    return task.readyTime

def sortDeadline(task):
    return task.deadline


# Calculate hyperperiod
def calculateHyperPeriod(taskPool):
    lcm = 1
    for task in taskPool:
        lcm = lcm * task.period // gcd(lcm, task.period)
    return lcm


# Sort task pool based on scheduling algorithm
if schedulingAlgo == 1:
    # FCFS
    sortedTaskPool = sorted(taskPool, key=sortReadyTime)
elif schedulingAlgo == 2:
    # RM
    sortedTaskPool = sorted(taskPool, key=sortPeriod)
elif schedulingAlgo == 3:
    # DM
    sortedTaskPool = sorted(taskPool, key=sortDeadline)
elif schedulingAlgo == 4:
    # EDF
    sortedTaskPool = sorted(taskPool, key=sortReadyTime)
elif schedulingAlgo == 5:
    # LST
    sortedTaskPool = sorted(taskPool, key=sortReadyTime)


# Generate all the jobs for each task.  Order is important here for the static scheduling algorithm, because the task pool has been sorted by priority already
fullSimulationWindow = calculateHyperPeriod(taskPool) * 3
finalTaskPool = []
for task in sortedTaskPool:
    task.print()
    numberOfTasks = int(fullSimulationWindow / task.period)
    print("Number of Periods : " + str(numberOfTasks))

    # In our final task pool, add every instance of the task
    for i in range(numberOfTasks):
        offset = i * task.period
        finalTaskPool.append(PeriodicTask.PeriodicTask(task.id, task.period, task.readyTime + offset, task.deadline + offset, task.executionTime))


simSchedule = SimulationSchedule.SimulationSchedule()
if schedulingAlgo == 1 or schedulingAlgo == 2 or schedulingAlgo == 3:
    # Insert all the tasks into the schedule.
    for task in finalTaskPool:
        simSchedule.insert(task)
    simSchedule.print()
elif schedulingAlgo == 4 or schedulingAlgo == 5:
    simSchedule.simulateDynamicSchedule(fullSimulationWindow, finalTaskPool, schedulingAlgo)
    simSchedule.print()

