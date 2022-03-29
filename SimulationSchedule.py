import TaskSession
import PeriodicTask
import SortingFunctions

class SimulationSchedule(object):
    def __init__(self):
        self.scheduledTaskPool = []
    
    def sortStartTime(self, session):
        return session.startTime

    def isExecutionFinished(task):
        if task.remainingExecutionTime == 0:
            return True
        else:
            return False

    def checkSessionEndBeforeTaskArrival(self, session, task):
        if session.endTime <= task.readyTime:
            return True
        else:
            return False

    def insert(self, task):
        if len(self.scheduledTaskPool) == 0:
            self.scheduledTaskPool.append(TaskSession.TaskSession(task.readyTime, task.readyTime + task.executionTime, task))
        else:
            taskReadyTime = task.readyTime
            remainingExecutionTime = task.executionTime
            taskSessionsToBeAdded = []
            for session in self.scheduledTaskPool:
                if remainingExecutionTime == 0:
                    #print("Execution complete...")
                    break
                elif self.checkSessionEndBeforeTaskArrival(session, task):
                    #print("Session ends before we arrive... Don't care")
                    pass
                elif not session.isStartTimeAvailable(taskReadyTime):
                    #print("Session was using our readytime... Using next closest")
                    taskReadyTime = session.endTime
                else:
                    #print("readyTime currently available...")
                    if session.startTime >= taskReadyTime + remainingExecutionTime:
                        #print("Yay!! There is enough time for us to finish running our task...")
                        taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReadyTime, taskReadyTime + remainingExecutionTime, task))
                        remainingExecutionTime = 0
                    else:
                        #print("There is not enough time to complete execution... Execute what we can and continue searching for place to execute remaining work...")
                        elapsedExecutionTime = session.startTime - taskReadyTime
                        remainingExecutionTime -= elapsedExecutionTime
                        taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReadyTime, taskReadyTime + elapsedExecutionTime, task))
                        taskReadyTime = session.endTime

            # If we iterated over all the current task sessions and we still have execution time remianing, add it
            if remainingExecutionTime > 0:
                taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReadyTime, taskReadyTime + remainingExecutionTime, task))
            
            # Add all the task sessions to the scheduled task pool and then sort it based on start times
            for task in taskSessionsToBeAdded:
                self.scheduledTaskPool.append(task)
            self.scheduledTaskPool = sorted(self.scheduledTaskPool, key=self.sortStartTime)

    def print(self):
        for task in self.scheduledTaskPool:
            task.print()
        