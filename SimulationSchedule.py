from selectors import SelectorKey
import TaskSession
import PeriodicTask
import SortingFunctions

class SimulationSchedule(object):
    def __init__(self):
        self.scheduledTaskPool = []
    
    def sortStartTime(self, session):
        return session.startTime
    
    def sortReadyTime(self, session):
        return session.readyTime

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
                    break
                elif self.checkSessionEndBeforeTaskArrival(session, task):
                    pass
                elif not session.isStartTimeAvailable(taskReadyTime):
                    taskReadyTime = session.endTime
                else:
                    if session.startTime >= taskReadyTime + remainingExecutionTime:
                        taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReadyTime, taskReadyTime + remainingExecutionTime, task))
                        remainingExecutionTime = 0
                    else:
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

    def simulateDynamicSchedule(self, simulationTimeLength, taskPool, schedulingAlgo):
        # Sort the task pool by start time just in case
        taskPool = sorted(taskPool, key=self.sortReadyTime)
        availableTaskPool = []
        for task in taskPool:
            task.print()
            print(task)
        
        # Begin iterating over the list
        currentTime = 0
        nextTaskAvailableTime = 0
        while currentTime <= simulationTimeLength:
            # Get all the tasks at the current time and place them in the available task pool
            while nextTaskAvailableTime == currentTime:
                if len(taskPool) == 0:
                    print("No more unavailable tasks...")
                    break

                task = taskPool.pop(0)
                if task.readyTime == currentTime:
                    availableTaskPool.append(task)
                else:
                    taskPool.insert(0,task)
                
                # We always set the next available time to the task we just looked at's ready time.
                # That way if the task was ready we check the next task in the list.
                # But if the task was not ready we stop checking the next task in the list.
                nextTaskAvailableTime = task.readyTime

            # Calculate the priority of the available tasks
            currentlyExecutingTask = None
            if len(availableTaskPool) > 0:
                if schedulingAlgo == 4:
                    for task in availableTaskPool:
                        if currentlyExecutingTask is None:
                            currentlyExecutingTask = task
                        elif task.deadline < currentlyExecutingTask.deadline:
                            currentlyExecutingTask = task
                elif schedulingAlgo == 5:
                    pass
            else:
                print("No tasks to execute...")

            if len(taskPool) == 0 and len(availableTaskPool) == 1:
                self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + task.remainingExecutionTime, currentlyExecutingTask))
                currentTime = simulationTimeLength + 1
            elif nextTaskAvailableTime < currentTime + 1:
                currentlyExecutingTask.print()
                if currentlyExecutingTask is not None:
                    if nextTaskAvailableTime >= currentTime + currentlyExecutingTask.remainingExecutionTime:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, nextTaskAvailableTime, currentlyExecutingTask))
                        nextTaskAvailableTime = currentTime + currentlyExecutingTask.remainingExecutionTime
                        availableTaskPool.remove(currentlyExecutingTask)
                    else:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, nextTaskAvailableTime, currentlyExecutingTask))
                        currentlyExecutingTask.setRemainingExecutionTime(currentlyExecutingTask.executionTime - (nextTaskAvailableTime - currentTime))
                currentTime = nextTaskAvailableTime
            else:
                if currentlyExecutingTask is not None:
                    if currentlyExecutingTask.remainingExecutionTime <= 1:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + task.remainingExecutionTime, currentlyExecutingTask))
                        nextTaskAvailableTime = currentTime + currentlyExecutingTask.remainingExecutionTime
                        currentTime = nextTaskAvailableTime
                        availableTaskPool.remove(currentlyExecutingTask)
                    else:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + 1, currentlyExecutingTask))
                        currentlyExecutingTask.setRemainingExecutionTime(currentlyExecutingTask.remainingExecutionTime - 1)
                        currentTime += 1
                else:
                    currentTime += 1

        # After we finish our dynamic schedule we will be left with many task sessions that are a maximum of 1 time unit long...
        # We need to stitch adjacent task sessions of the same task back together

    def print(self):
        for task in self.scheduledTaskPool:
            task.print()
        