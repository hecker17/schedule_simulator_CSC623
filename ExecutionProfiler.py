import TaskSession
import PeriodicTask
import ServerPeriod
import SimulationSchedule
#matplotlibPresent = True
#try:
#    import matplotlib
#except ModuleNotFoundError:
#    matplotlibPresent = False

class ExecutionProfiler(object):
    def __init__(self, simulationSchedule, finalPeriodicTaskPool, periodicTaskPool, aperiodicTaskPool):
        self.simulationSchedule = simulationSchedule
        self.finalPeriodicTaskPool = finalPeriodicTaskPool
        self.periodicTaskPool = periodicTaskPool
        self.aperiodicTaskPool = aperiodicTaskPool

    def calculateActualStartAndEndTimes(self):
        for task in self.finalPeriodicTaskPool:    
            self.simulationSchedule.calculateActualStartAndEndTimes(task)
            task.printActualTimes()
        for task in self.aperiodicTaskPool:
            self.simulationSchedule.calculateActualStartAndEndTimes(task)
            task.printActualTimes()

    def calculateAmountOfDeadlinesMissed(self):
        numOfDeadlineMisses = 0
        for task in self.finalPeriodicTaskPool:
            if task.actualEndTime is None:
                # Task never finished...
                numOfDeadlineMisses += 1
                task.deadlineMissed = True
            elif task.actualEndTime > task.deadline:
                # Task deadline missed...
                numOfDeadlineMisses += 1
                task.deadlineMissed = True
            else:
                # Task finished before deadline...
                pass
        return numOfDeadlineMisses

    def calculateTotalSystemUtilization(self):
        systemUtilization = 0
        for task in self.periodicTaskPool:
            taskUtilization = task.executionTime / task.period
            systemUtilization += taskUtilization
        return systemUtilization

    def calculateTotalSystemDensity(self):
        systemDensity = 0
        for task in self.periodicTaskPool:
            taskDensity = task.executionTime / min(task.deadline, task.period)
            systemDensity += taskDensity
        return systemDensity

    def calculateAverageAperiodicTaskResponseTime(self):
        cumulativeResponseTime = 0
        numOfAperiodicTaskCompletions = 0
        averageResponseTime = None
        for task in self.aperiodicTaskPool:
            if task.actualStartTime is not None and task.actualEndTime is not None:
                aperiodicTaskResponseTime = task.actualEndTime - task.actualStartTime
                cumulativeResponseTime += aperiodicTaskResponseTime
                numOfAperiodicTaskCompletions += 1
            else:
                print(str(task.id) + " failed to finish...")
        if numOfAperiodicTaskCompletions > 0:
            averageResponseTime = cumulativeResponseTime / numOfAperiodicTaskCompletions
        return averageResponseTime

    def plotTaskSessions(self):
        matplotlibPresent = False
        if matplotlibPresent:
            pass
        else:
            print("Python3: matplotlib library is not installed...")