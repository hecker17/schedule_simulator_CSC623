class ServerPeriod(object):
    def __init__(self, periodStartTime, periodEndTime, serverExecutionTime):
        self.periodStartTime = periodStartTime
        self.periodEndTime = periodEndTime
        self.serverFullExecutionTime = serverExecutionTime
        self.serverRemainingExecutionTime = serverExecutionTime
        self.serverExecutionStartTime = None

    def print(self):
        print("periodStartTime: " + str(self.periodStartTime) + " periodEndTime: " + str(self.periodEndTime) + " serverFullExecutionTime: " + str(self.serverFullExecutionTime) + " serverRemainingExecutionTime: " + str(self.serverRemainingExecutionTime) + " serverExecutionStartTime: " + str(self.serverExecutionStartTime))
        