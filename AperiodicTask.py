class AperiodicTask(object):
    def __init__(self, id, releaseTime, executionTime):
        self.id = id
        self.releaseTime = releaseTime
        self.executionTime = executionTime
        self.remainingExecutionTime = executionTime
        self.actualStartTime = None
        self.actualEndTime = None

    def print(self):
        print("Aperiodic Task : id: " + str(self.id) + " releaseTime: " + str(self.releaseTime) + " executionTime: " + str(self.executionTime) + " remainingExecutionTime: " + str(self.remainingExecutionTime))

    def printActualTimes(self):
        print("Aperiodic Task : id: " + str(self.id) + " actualStartTime: " + str(self.actualStartTime) + " actualEndTime: " + str(self.actualEndTime))