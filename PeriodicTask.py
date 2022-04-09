class PeriodicTask(object):
    def __init__(self, id, period, readyTime, deadline, executionTime):
        self.id = id
        self.period = period
        self.readyTime = readyTime
        self.deadline = deadline
        self.executionTime = executionTime
        self.remainingExecutionTime = executionTime
        self.actualStartTime = None
        self.actualEndTime = None
        self.deadlineMissed = False

    def print(self):
        print("Periodic Task : id: " + str(self.id) + " period: " + str(self.period) + " readyTime: " + str(self.readyTime) + " deadline: " + str(self.deadline) + " executionTime: " + str(self.executionTime) + " remainingExecutionTime: " + str(self.remainingExecutionTime) + " actualStartTime: " + str(self.actualStartTime) + " actualEndTime: " + str(self.actualEndTime) + " deadlineMissed: " + str(self.deadlineMissed))

    def printActualTimes(self):
        print("Periodic Task : id: " + str(self.id) + " actualStartTime: " + str(self.actualStartTime) + " actualEndTime: " + str(self.actualEndTime))