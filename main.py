from math import gcd
import PeriodicTask
import AperiodicTask
import SimulationSchedule
import sys

# Set up several core objects
periodicTaskPool = []
aperiodicTaskPool = []
sortedPeriodicTaskPool = []
simSchedule = SimulationSchedule.SimulationSchedule()

# 1 is FCFS, 2 is RM, 3 is DM, 4 is EDF, and 5 is LST
periodicSchedulingAlgo = 5
# 1 is Polling Server, 2 is Deferrable Server
aperiodicSchedulingAlgo = 1
# The period length for the server scheduling algorithm
serverPeriod = 20
# The available execution time for the server scheduling algorithm
serverExecutionTime = 5

# Do some simple argument parsing
print("Number of args: " + str(len(sys.argv)))
if len(sys.argv) != 6:
    print("Incorrect number of arguments...")
    print("Usage:")
    print("    python3 main.py <periodicSchedulingAlgo> <aperiodicSchedulingAlgo> <serverPeriod> <serverExecutiontime> <taskFile>")
    print("        periodicSchedulingAlgo - 1 is FCFS, 2 is RM, 3 is DM, 4 is EDF, and 5 is LST.")
    print("        aperiodicSchedulingAlgo - 1 is Polling Server, 2 is Deferrable Server.")
    print("        serverPeriod - Period length for the Server.")
    print("        serverExecutiontime - Execution budget available to Server.")
    print("        taskFile - Path to task input file.")
    print("Using sample values...")
    periodicSchedulingAlgo = 5
    aperiodicSchedulingAlgo = 1
    serverPeriod = 20
    serverExecutionTime = 5

    # Set up sample periodic tasks
    periodicTask1 = PeriodicTask.PeriodicTask(1,35,0,33,10)
    periodicTask2 = PeriodicTask.PeriodicTask(2,35,4,28,3.5)
    periodicTask3 = PeriodicTask.PeriodicTask(3,35,5,29,10)
    periodicTaskPool.append(periodicTask1)
    periodicTaskPool.append(periodicTask2)
    periodicTaskPool.append(periodicTask3)
    
    # Set up sample aperiodic tasks
    aperiodicTask1 = AperiodicTask.AperiodicTask(4,25,6)
    aperiodicTask2 = AperiodicTask.AperiodicTask(5,45,3)
    aperiodicTask3 = AperiodicTask.AperiodicTask(6,62,2)
    aperiodicTask4 = AperiodicTask.AperiodicTask(7,64,2)
    aperiodicTask5 = AperiodicTask.AperiodicTask(8,66,2)
    aperiodicTaskPool.append(aperiodicTask1)
    aperiodicTaskPool.append(aperiodicTask2)
    aperiodicTaskPool.append(aperiodicTask3)
    aperiodicTaskPool.append(aperiodicTask4)
    aperiodicTaskPool.append(aperiodicTask5)
else:
    print("periodicSchedulingAlgo: " + str(sys.argv[1]))
    print("aperiodicSchedulingAlgo: " + str(sys.argv[2]))
    print("serverPeriod: " + str(sys.argv[3]))
    print("serverExecutionTime: " + str(sys.argv[4]))
    print("taskFile: " + str(sys.argv[5]))
    periodicSchedulingAlgo = int(sys.argv[1])
    aperiodicSchedulingAlgo = int(sys.argv[2])
    serverPeriod = int(sys.argv[3])
    serverExecutionTime = int(sys.argv[4])

    taskFile = open(str(sys.argv[5]), 'r')
    for line in taskFile.readlines():
        print(line.replace('\n',''))
        taskValues = line.replace('\n','').split(',')
        if taskValues[0] == 't':
            periodicTaskPool.append(PeriodicTask.PeriodicTask(str(taskValues[0]) + str(taskValues[1]),int(taskValues[2]),float(taskValues[3]),float(taskValues[4]),float(taskValues[5])))
        elif taskValues[0] == 'a':
            aperiodicTaskPool.append(AperiodicTask.AperiodicTask(str(taskValues[0]) + str(taskValues[1]),float(taskValues[2]),float(taskValues[3])))

    for task in periodicTaskPool:
        task.print()
    for task in aperiodicTaskPool:
        task.print()


# Set up sample tasks
#task1 = PeriodicTask.PeriodicTask(1,20,0,15,3)
#task2 = PeriodicTask.PeriodicTask(2,5,0,4,2)
#task3 = PeriodicTask.PeriodicTask(3,10,0,3,2)
task1 = PeriodicTask.PeriodicTask(1,35,0,33,10)
task2 = PeriodicTask.PeriodicTask(2,35,4,28,3.5)
task3 = PeriodicTask.PeriodicTask(3,35,5,29,10)


# Sorting Functions
def sortPeriod(task):
    return task.period

def sortReadyTime(task):
    return task.readyTime

def sortDeadline(task):
    return task.deadline
    
def sortReleaseTime(task):
    return task.releaseTime


# Calculate hyperperiod
def calculateHyperPeriod(taskPool):
    lcm = 1
    for task in taskPool:
        lcm = lcm * task.period // gcd(lcm, task.period)
    return lcm


# Sort periodic task pool based on scheduling algorithm
if periodicSchedulingAlgo == 1:
    # FCFS
    sortedPeriodicTaskPool = sorted(periodicTaskPool, key=sortReadyTime)
elif periodicSchedulingAlgo == 2:
    # RM
    sortedPeriodicTaskPool = sorted(periodicTaskPool, key=sortPeriod)
elif periodicSchedulingAlgo == 3:
    # DM
    sortedPeriodicTaskPool = sorted(periodicTaskPool, key=sortDeadline)
elif periodicSchedulingAlgo == 4:
    # EDF
    sortedPeriodicTaskPool = sorted(periodicTaskPool, key=sortReadyTime)
elif periodicSchedulingAlgo == 5:
    # LST
    sortedPeriodicTaskPool = sorted(periodicTaskPool, key=sortReadyTime)


# Sort aperiodic task pool based
sortedAperiodicTaskPool = sorted(aperiodicTaskPool, key=sortReleaseTime)


# Generate all the jobs for each task.  Order is important here for the static scheduling algorithm, because the task pool has been sorted by priority already
fullSimulationWindow = calculateHyperPeriod(periodicTaskPool) * 3
print("Time Window : " + str(fullSimulationWindow))
finalPeriodicTaskPool = []
for task in sortedPeriodicTaskPool:
    task.print()
    numberOfTasks = int(fullSimulationWindow / task.period)

    # In our final task pool, add every job of the task
    for i in range(numberOfTasks):
        offset = i * task.period
        finalPeriodicTaskPool.append(PeriodicTask.PeriodicTask(task.id + "_" + str(i), task.period, task.readyTime + offset, task.deadline + offset, task.executionTime))

print("Size of finalPeriodicTaskPool: " + str(len(finalPeriodicTaskPool)))
print("Size of sortedAperiodicTaskPool: " + str(len(sortedAperiodicTaskPool)))
# Insert static priority tasks or simulate the dynamic schedule
if periodicSchedulingAlgo == 1 or periodicSchedulingAlgo == 2 or periodicSchedulingAlgo == 3:
    for task in finalPeriodicTaskPool:
        simSchedule.insert(task)
    simSchedule.print()
elif periodicSchedulingAlgo == 4 or periodicSchedulingAlgo == 5:
    simSchedule.simulateDynamicSchedule(fullSimulationWindow, finalPeriodicTaskPool, periodicSchedulingAlgo)
    simSchedule.print()

# Aperiodic task insertion
simSchedule.setAperiodicServerParameters(aperiodicSchedulingAlgo, fullSimulationWindow, serverPeriod, serverExecutionTime)
for task in sortedAperiodicTaskPool:
    simSchedule.insertAperiodic(task)

# Trim all tasks outside fullSimulationWindow
simSchedule.trimAfter(fullSimulationWindow)

# Print final simulation schedule
simSchedule.print()
simSchedule.printById("t3_4")