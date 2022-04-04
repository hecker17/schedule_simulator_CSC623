from selectors import SelectorKey
from signal import pause
import TaskSession
import PeriodicTask
import SortingFunctions
import ServerPeriod
import math

class SimulationSchedule(object):
    def __init__(self):
        self.scheduledTaskPool = []

    def setAperiodicServerParameters(self, aperiodicSchedulingAlgo, fullSimulationWindow, serverPeriod, serverExecutionTime):
        self.aperiodicSchedulingAlgo = aperiodicSchedulingAlgo
        self.fullSimulationWindow = fullSimulationWindow
        self.serverPeriod = serverPeriod
        self.serverPeriodList = []

        # Create a list of all the server periods
        serverPeriodsInSimulation = math.ceil(fullSimulationWindow / serverPeriod)
        for period in range(serverPeriodsInSimulation):
            self.serverPeriodList.append(ServerPeriod.ServerPeriod(period * serverPeriod, (period + 1) * serverPeriod ,serverExecutionTime))
    
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

    def insertAperiodic(self, task):
        #print("Aperiodic Server Parameters: serverPeriod: " + str(self.serverPeriod))

        taskReleaseTime = task.releaseTime
        taskSessionsToBeAdded = []

        # Then check which server period we are in based on our releaseTime
        currentServerPeriod = None
        for period in self.serverPeriodList:
            if taskReleaseTime < period.periodEndTime:
                currentServerPeriod = period

            if currentServerPeriod == None:
                pass
                #print("We could not find a server period compatible with our release time...")
            else:
                #print("We have a valid currentServerPeriod! " + str(currentServerPeriod.periodStartTime) + " - " + str(currentServerPeriod.periodEndTime))
                if currentServerPeriod.periodStartTime > taskReleaseTime:
                    taskReleaseTime = currentServerPeriod.periodStartTime
            
                # Check if there is remaining execution time
                serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime
                #print("serverRemainingExecutionTime: " + str(serverRemainingExecutionTime))
                if serverRemainingExecutionTime > 0 and task.remainingExecutionTime > 0:
                    #print("There is some execution time still available...")

                    # Search for an opening in the scheduledTaskPool
                    #print("===================================================================" + str(len(self.scheduledTaskPool)))
                    for i in range(len(self.scheduledTaskPool)):
                        session = self.scheduledTaskPool[i]

                        # If there is no more execution required for the task...
                        if task.remainingExecutionTime <= 0 or currentServerPeriod.serverRemainingExecutionTime <= 0:
                            pass
                        # If session ends before the task is released we can ignore it
                        elif session.endTime < taskReleaseTime:
                            pass
                        # If session ends before current period or begins after current period we can ignore it
                        # If sessions are outside our current period
                        elif session.endTime <= currentServerPeriod.periodStartTime or session.startTime >= currentServerPeriod.periodEndTime:
                            pass
                        # If a session starts before we released and ends after we were released... Adjust our release time...
                        elif session.startTime <= taskReleaseTime and session.endTime >= taskReleaseTime:
                            #print("!!")
                            #session.print()
                            taskReleaseTime = session.endTime

                            # Check if there even is a next task
                            if i + 1 >= len(self.scheduledTaskPool):
                                #print("Last task...")
                                # If there is no next task just slap what we can on...
                                
                                # Check how much execution time is left
                                potentialTaskExecutionTime = task.remainingExecutionTime
                                if task.remainingExecutionTime > currentServerPeriod.serverRemainingExecutionTime:
                                    potentialTaskExecutionTime = currentServerPeriod.serverRemainingExecutionTime
                                # Find execution cutoff
                                executionCutoff = currentServerPeriod.periodEndTime
                                #print("taskReleaseTime : " + str(taskReleaseTime))
                                #print("potentialTaskExecutionTime : " + str(potentialTaskExecutionTime))
                                #print("executionCutoff : " + str(executionCutoff))

                                if taskReleaseTime + potentialTaskExecutionTime <= executionCutoff:
                                    #print("We can execute the maximum amount")
                                    task.remainingExecutionTime = task.remainingExecutionTime - potentialTaskExecutionTime
                                    currentServerPeriod.serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime - potentialTaskExecutionTime
                                    taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReleaseTime, taskReleaseTime + potentialTaskExecutionTime, task))
                                    #print("Successful Insertion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    #task.print()
                                else:
                                    elapsedExecutionTime = executionCutoff - taskReleaseTime
                                    #print("We can only execute a portion of the maximum : " + str(elapsedExecutionTime))
                                    task.remainingExecutionTime = task.remainingExecutionTime - elapsedExecutionTime
                                    currentServerPeriod.serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime - elapsedExecutionTime
                                    taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReleaseTime, executionCutoff, task))
                                    #print("Successful Insertion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    #task.print()
                            else:
                                # Set our current session to the next session...
                                session = self.scheduledTaskPool[i+1]
                                if session.startTime == taskReleaseTime:
                                    pass
                                    #print("There is no room!!!")
                                else:
                                    #print("There is some room!!!!")
                                    # Check how much execution time is left
                                    potentialTaskExecutionTime = task.remainingExecutionTime
                                    if task.remainingExecutionTime > currentServerPeriod.serverRemainingExecutionTime:
                                        potentialTaskExecutionTime = currentServerPeriod.serverRemainingExecutionTime
                                    # Find execution cutoff
                                    executionCutoff = session.startTime
                                    if session.startTime > currentServerPeriod.periodEndTime:
                                        executionCutoff = currentServerPeriod.periodEndTime
                                    #print("potentialTaskExecutionTime : " + str(potentialTaskExecutionTime))
                                    #print("executionCutoff : " + str(executionCutoff))

                                    if taskReleaseTime + potentialTaskExecutionTime <= executionCutoff:
                                        #print("We can execute the maximum amount")
                                        task.remainingExecutionTime = task.remainingExecutionTime - potentialTaskExecutionTime
                                        currentServerPeriod.serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime - potentialTaskExecutionTime
                                        taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReleaseTime, taskReleaseTime + potentialTaskExecutionTime, task))
                                        #print("Successful Insertion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                        #task.print()
                                    else:
                                        elapsedExecutionTime = executionCutoff - taskReleaseTime
                                        #print("We can only execute a portion of the maximum : " + str(elapsedExecutionTime))
                                        task.remainingExecutionTime = task.remainingExecutionTime - elapsedExecutionTime
                                        currentServerPeriod.serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime - elapsedExecutionTime
                                        taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReleaseTime, executionCutoff, task))
                                        #print("Successful Insertion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                        #task.print()
                        else:
                            # This occurs when we release before the current session begins... We can try and insert in here...

                            # Check if there even is a next task
                            if i + 1 >= len(self.scheduledTaskPool):
                                # I don't think we need to do this as our current session is the one in the "future"
                                pass
                            else:
                                # Check how much execution time is left
                                potentialTaskExecutionTime = task.remainingExecutionTime
                                if task.remainingExecutionTime > currentServerPeriod.serverRemainingExecutionTime:
                                    potentialTaskExecutionTime = currentServerPeriod.serverRemainingExecutionTime
                                # Find execution cutoff
                                executionCutoff = session.startTime
                                if session.startTime > currentServerPeriod.periodEndTime:
                                    executionCutoff = currentServerPeriod.periodEndTime

                                if taskReleaseTime + potentialTaskExecutionTime <= executionCutoff:
                                    #print("We can execute the maximum amount")
                                    task.remainingExecutionTime = task.remainingExecutionTime - potentialTaskExecutionTime
                                    currentServerPeriod.serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime - potentialTaskExecutionTime
                                    taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReleaseTime, taskReleaseTime + potentialTaskExecutionTime, task))
                                    #print("Successful Insertion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    #task.print()
                                else:
                                    elapsedExecutionTime = executionCutoff - taskReleaseTime
                                    #print("We can only execute a portion of the maximum")
                                    task.remainingExecutionTime = task.remainingExecutionTime - elapsedExecutionTime
                                    currentServerPeriod.serverRemainingExecutionTime = currentServerPeriod.serverRemainingExecutionTime - elapsedExecutionTime
                                    taskSessionsToBeAdded.append(TaskSession.TaskSession(taskReleaseTime, executionCutoff, task))
                                    #print("Successful Insertion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    #task.print()

        #print("################################################################")
        #for session in taskSessionsToBeAdded:
        #    session.print()
        #print("################################################################")
        # Add all the task sessions to the scheduled task pool and then sort it based on start times
        for task in taskSessionsToBeAdded:
            self.scheduledTaskPool.append(task)
        self.scheduledTaskPool = sorted(self.scheduledTaskPool, key=self.sortStartTime)



    def calculateTaskPriority(self, currentlyExecutingTask, availableTaskPool, schedulingAlgo):
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

    def simulateDynamicSchedule(self, simulationTimeLength, taskPool, schedulingAlgo):
        # Sort the task pool by start time just in case
        taskPool = sorted(taskPool, key=self.sortReadyTime)
        availableTaskPool = []
        
        # Begin iterating over the list
        currentTime = 0
        nextTaskAvailableTime = 0
        currentlyExecutingTask = None
        while currentTime <= simulationTimeLength:
            # Get all the tasks at the current time and place them in the available task pool
            #print("===============================================================================================================")
            #print("Current Time: " + str(currentTime))
            while nextTaskAvailableTime == currentTime:
                if len(taskPool) == 0:
                    #print("No more unavailable tasks...")
                    # Plus 1 is better?
                    nextTaskAvailableTime = simulationTimeLength + 1
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

            #print("Available tasks...")
            #for task in availableTaskPool:
            #    task.print()
            #print("Unavailalbe tasks...")
            #for task in taskPool:
            #    task.print()

            # Calculate the priority of the available tasks
            #print("======Priorities======")
            #currentlyExecutingTask = None
            if len(availableTaskPool) > 0:
                if schedulingAlgo == 4:
                    for task in availableTaskPool:
                        if currentlyExecutingTask is None:
                            currentlyExecutingTask = task
                        elif task.deadline < currentlyExecutingTask.deadline:
                            currentlyExecutingTask = task
                elif schedulingAlgo == 5:
                    for task in availableTaskPool:
                        #print("Task id: " + str(task.id) + " : priority: " +str(task.deadline - currentTime - task.remainingExecutionTime))
                        if currentlyExecutingTask is None:
                            currentlyExecutingTask = task
                        elif (task.deadline - currentTime - task.remainingExecutionTime) < (currentlyExecutingTask.deadline - currentTime - currentlyExecutingTask.remainingExecutionTime):
                            currentlyExecutingTask = task
            #if currentlyExecutingTask is not None:
            #    print("Currently Executing Task " + str(currentlyExecutingTask.id))
            #    currentlyExecutingTask.print()
            #else:
            #    print("No Currently Executing Task")

            if len(taskPool) == 0 and len(availableTaskPool) == 1:
                self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + task.remainingExecutionTime, currentlyExecutingTask))
                currentTime = simulationTimeLength + 1
            elif nextTaskAvailableTime < currentTime + 1:
                if currentlyExecutingTask is not None:
                    if currentTime + currentlyExecutingTask.remainingExecutionTime <= nextTaskAvailableTime:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + currentlyExecutingTask.remainingExecutionTime, currentlyExecutingTask))
                        currentTime = currentTime + currentlyExecutingTask.remainingExecutionTime
                        availableTaskPool.remove(currentlyExecutingTask)
                        currentlyExecutingTask = None
                    else:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, nextTaskAvailableTime, currentlyExecutingTask))
                        elapsedExecutionTime = nextTaskAvailableTime - currentTime
                        currentlyExecutingTask.remainingExecutionTime = currentlyExecutingTask.remainingExecutionTime - elapsedExecutionTime
                        currentTime = nextTaskAvailableTime
                else:
                    currentTime = nextTaskAvailableTime
            else:
                if currentlyExecutingTask is not None:
                    if currentlyExecutingTask.remainingExecutionTime <= 1:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + currentlyExecutingTask.remainingExecutionTime, currentlyExecutingTask))
                        currentTime = currentTime + currentlyExecutingTask.remainingExecutionTime
                        availableTaskPool.remove(currentlyExecutingTask)
                        currentlyExecutingTask = None
                    else:
                        self.scheduledTaskPool.append(TaskSession.TaskSession(currentTime, currentTime + 1, currentlyExecutingTask))
                        currentlyExecutingTask.remainingExecutionTime = currentlyExecutingTask.remainingExecutionTime - 1
                        currentTime += 1
                else:
                    currentTime += 1

        # # After we finish our dynamic schedule we will be left with many task sessions that are a maximum of 1 time unit long...
        # # We need to stitch adjacent task sessions of the same task back together
        baseTaskSession = None
        consolidatedTaskPool = []
        for taskSession in self.scheduledTaskPool:
            if baseTaskSession is None:
                baseTaskSession = taskSession
            else:
                if baseTaskSession.task == taskSession.task:
                    # Create new task session that is the combination of the base and current task sessions
                    baseTaskSession = TaskSession.TaskSession(baseTaskSession.startTime, taskSession.endTime, baseTaskSession.task)
                else:
                    consolidatedTaskPool.append(baseTaskSession)
                    baseTaskSession = taskSession
        # # Probably need to insert final task session
        consolidatedTaskPool.append(baseTaskSession)
        self.scheduledTaskPool = consolidatedTaskPool

    def trimAfter(self, fullSimulationWindow):
        print("Trim the task that starts before the end of the fullSimulationWindow and ends after it to end right at it.")
        print("Remove all tasks that start after the fullSimulationWindow.")
        for session in self.scheduledTaskPool:
            if session.startTime < fullSimulationWindow and session.endTime > fullSimulationWindow:
                session.endTime = fullSimulationWindow
            elif session.startTime >= fullSimulationWindow:
                self.scheduledTaskPool.remove(session)

    def print(self):
        print("Size of finalTaskPool: " + str(len(self.scheduledTaskPool)))
        for task in self.scheduledTaskPool:
            task.print()

    def printById(self, id):
        print("Size of finalTaskPool: " + str(len(self.scheduledTaskPool)))
        for session in self.scheduledTaskPool:
            if session.task.id == id:
                session.print()
        