class PeriodicTask(object):
    def __init__(self, id, period, readyTime, deadline, executionTime):
        self.id = id
        self.period = period
        self.readyTime = readyTime
        self.deadline = deadline
        self.executionTime = executionTime
        self.remainingExecutionTime = executionTime

    def print(self):
        print("Periodic Task : id: " + str(self.id) + " period: " + str(self.period) + " readyTime: " + str(self.readyTime) + " deadline: " + str(self.deadline) + " executionTime: " + str(self.executionTime) + " remainingExecutionTime: " + str(self.remainingExecutionTime))
