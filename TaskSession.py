class TaskSession(object):
    def __init__(self):
        pass

    def __init__(self, startTime, endTime, task):
        self.startTime = startTime
        self.endTime = endTime
        self.task = task

    def print(self):
        print(" task.id: " + str(self.task.id) + " startTime: " + str(self.startTime) + " endTime: " + str(self.endTime) + " task: " + str(self.task))

    # This method is used when the scheduler is checking if the session has already ended
    def checkSessionEndBeforeTaskArrival(self, session, task):
        if session.endTime <= task.readyTime:
            return True
        else:
            return False

    # This method is used when the scheduler is looking for an opening to start its task
    def isStartTimeAvailable(self, time):
        if time >= self.startTime and time < self.endTime:
            return False
        else:
            return True
