from math import gcd
import sched
from signal import pause
import PeriodicTask
import AperiodicTask
import SimulationSchedule

# Set up sample tasks
#task1 = PeriodicTask.PeriodicTask(1,20,0,15,3)
#task2 = PeriodicTask.PeriodicTask(2,5,0,4,2)
#task3 = PeriodicTask.PeriodicTask(3,10,0,3,2)
task1 = PeriodicTask.PeriodicTask(1,35,0,33,10)
task2 = PeriodicTask.PeriodicTask(2,35,4,28,3)
task3 = PeriodicTask.PeriodicTask(3,35,5,29,10)
taskPool = []
taskPool.append(task1)
taskPool.append(task2)
taskPool.append(task3)

# 1 is FCFS, 2 is RM, 3 is DM, 4 is EDF, and 5 is LST
periodicSchedulingAlgo = 5
# 1 is Polling Server, 2 is Deferrable Server
aperiodicSchedulingAlgo = 1

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
if periodicSchedulingAlgo == 1:
    # FCFS
    sortedTaskPool = sorted(taskPool, key=sortReadyTime)
elif periodicSchedulingAlgo == 2:
    # RM
    sortedTaskPool = sorted(taskPool, key=sortPeriod)
elif periodicSchedulingAlgo == 3:
    # DM
    sortedTaskPool = sorted(taskPool, key=sortDeadline)
elif periodicSchedulingAlgo == 4:
    # EDF
    sortedTaskPool = sorted(taskPool, key=sortReadyTime)
elif periodicSchedulingAlgo == 5:
    # LST
    sortedTaskPool = sorted(taskPool, key=sortReadyTime)


# Generate all the jobs for each task.  Order is important here for the static scheduling algorithm, because the task pool has been sorted by priority already
fullSimulationWindow = calculateHyperPeriod(taskPool) * 3
print("Time Window : " + str(fullSimulationWindow))
finalTaskPool = []
for task in sortedTaskPool:
    numberOfTasks = int(fullSimulationWindow / task.period)

    # In our final task pool, add every job of the task
    for i in range(numberOfTasks):
        offset = i * task.period
        finalTaskPool.append(PeriodicTask.PeriodicTask(task.id, task.period, task.readyTime + offset, task.deadline + offset, task.executionTime))

print("Size of finalTaskPool: " + str(len(finalTaskPool)))
simSchedule = SimulationSchedule.SimulationSchedule()
if periodicSchedulingAlgo == 1 or periodicSchedulingAlgo == 2 or periodicSchedulingAlgo == 3:
    # Insert all the tasks into the schedule.
    for task in finalTaskPool:
        simSchedule.insert(task)
    simSchedule.print()
elif periodicSchedulingAlgo == 4 or periodicSchedulingAlgo == 5:
    simSchedule.simulateDynamicSchedule(fullSimulationWindow, finalTaskPool, periodicSchedulingAlgo)
    simSchedule.print()

# Test Aperiodic Insertion
simSchedule.setAperiodicServerParameters(aperiodicSchedulingAlgo, fullSimulationWindow, 20, 5)
simSchedule.insertAperiodic(AperiodicTask.AperiodicTask(4,25,6))
simSchedule.insertAperiodic(AperiodicTask.AperiodicTask(5,45,3))
simSchedule.insertAperiodic(AperiodicTask.AperiodicTask(6,62,2))
simSchedule.insertAperiodic(AperiodicTask.AperiodicTask(7,64,2))
simSchedule.insertAperiodic(AperiodicTask.AperiodicTask(8,66,2))


simSchedule.print()