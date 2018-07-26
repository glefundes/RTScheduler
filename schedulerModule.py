#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:15:36 2018

@author: gabriel
"""
from operator import attrgetter

rslt = []

class Task:
    """ simple class to represent task with duration and period """
    def __init__(self, duration, period):
#        self.name = name
        self.duration = duration
        self.period = period
        self.deadline = period
        self.returnsAt = 0
        self.remaining = duration
        self.use = self.duration/self.period

        self.available = True
        self.pltColor = 'blue'            
    
    def printTask(self):
        print("(C:"+str(self.duration)+" T:"+str(self.period)+")", self.pltColor, "deadline:", self.deadline, "priority", self.priority)
        
class TaskEvent:
    def __init__(self, duration, deadline, color):
        self.duration = duration
        self.color = color
        self.deadline = deadline
        
class RateMonotonic:
    """ fixed priority by smallest period
        period == period """
    def __init__(self, tasks):
        self.schedulable = isSchedulable(tasks, "RM")
        # Sort tasks by smallest period(period)
        tasks.sort(key=lambda t: t.period, reverse=False)
        # assign priority based on previous sort
        offset = 0
        for task in tasks:    
            task.priority = 1+offset
            offset += 1
        self.tasks = tasks
    def getTasks(self):
        # Priority is fixed, no recalculation needed
        return self.tasks
    def setTasks(self, tasks):
        self.tasks = tasks
        
class EDF:
    """ dynamic priority by earliest deadline """
    def __init__(self, tasks):
        self.schedulable = isSchedulable(tasks, "EDF")
        # Sort tasks by smallest period(period)
        tasks.sort(key=lambda t: t.period, reverse=False)
        # assign priority based on previous sort
        offset = 0
        for task in tasks:    
            task.priority = 1+offset
            offset += 1
        self.tasks = tasks
    def getTasks(self):
        #dinamically assign priority and return sorted array
        self.tasks.sort(key=lambda t: t.deadline, reverse=False)
        offset = 0
        for task in self.tasks:    
            task.priority = 1+offset
            offset += 1
        return self.tasks
    
    def setTasks(self, tasks):
        self.tasks = tasks
            
class Scheduler:
    #TODO finished_task method
    #TODO context class
    
    def __init__(self, algo):
        self.result = []
        self.algo = algo
        self.scaleLimit = 2*(max(self.algo.tasks, key=attrgetter('period'))).period
        
        if(algo == "RM"):
            self.algo = RateMonotonic(self.tasks)
        
    def next_returning_task(self, tasks, t):        
        tasks.sort(key=lambda t: t.deadline, reverse=False)
        tasksDone = [task for task in tasks if not task.available]
        
        nextReturning = (min(tasksDone, key=attrgetter('returnsAt')))
        return nextReturning
    
    def run(self, t):
        if (t <= self.scaleLimit):
            tasks = self.algo.getTasks()
            if(t == 12):
                for task in tasks:
                    task.printTask()
            ##
            tasksDone = [task for task in tasks if not task.available]
            tasksAvailable = [task for task in tasks if  task.available]
            # possible idle time
            if (len(tasksAvailable) == 0):
               nextReturning = self.next_returning_task(tasksDone, t)
               print(t, "idletime: ", nextReturning.pltColor, nextReturning.returnsAt)
               if(t > nextReturning.returnsAt): nextReturning.returnsAt = t
               # update item?
               tasks.remove(nextReturning)
               nextReturning.available = True
               tasks.append(nextReturning)
               self.algo.setTasks(tasks)
               
               self.run(nextReturning.returnsAt)
            else:
                # task arrival
                nextTask = (min(tasksAvailable, key=attrgetter('priority')))# Get highest priority task
                finishingTime = t + nextTask.remaining        
                # No tasks completed yet, start
                if(len(tasksDone) == 0):
                    print(t, "Start")
                    tasks.remove(nextTask)
                    nextTask.returnsAt += nextTask.period
                    nextTask.deadline = (nextTask.period*2)
                    
                    nextTask.available = False
                    tasks.append(nextTask)
                    self.algo.setTasks(tasks)
                    
                    self.result.append ((TaskEvent(nextTask.remaining, nextTask.deadline, nextTask.pltColor), t))
                    self.run(finishingTime)
                
                # check if next task can be completed without preemption
                else:
                    # Check returning tasks for returning time, find the one that returns the earliest
                    nextReturning = self.next_returning_task(tasksDone, t)

                    # Preemption: some task returns before the end of current task, and it has priority
                    if (finishingTime > nextReturning.returnsAt and nextReturning.priority < nextTask.priority):
                        
                        print(t, "Preempt: ", nextReturning.pltColor+"(",nextReturning.priority,")", "takes over for ", nextTask.pltColor+"(",nextTask.priority,")" )
                        tasks.remove(nextReturning)
                        
                        nextTask.remaining -=  (nextReturning.returnsAt - t) 
                        nextReturning.available = True

                        tasks.append(nextReturning)
                        self.algo.setTasks(tasks)
                        
                        self.result.append ((TaskEvent(nextTask.remaining, nextTask.deadline, nextTask.pltColor), t))
                        self.run(nextReturning.returnsAt)
                    
                    # current task can finish before the next one returning
                    else:
                        print(t, "current task can finish before the next one returning", nextTask.pltColor)
                        self.result.append ((TaskEvent(nextTask.remaining, nextTask.deadline, nextTask.pltColor), t))
                        finishingTime = t + nextTask.remaining
                        tasks.remove(nextTask)
                        nextTask.remaining = nextTask.duration
                        nextTask.returnsAt += nextTask.period
                        nextTask.deadline = (nextTask.period + t)

                        nextTask.available = False
                        tasks.append(nextTask)
                        self.algo.setTasks(tasks)

                        self.run(finishingTime)
                 


def isSchedulable(tasks, algo):
    totalUse = sum(task.use for task in tasks)
    n = len(tasks)
    if(n == 0 ): return
    if (algo == "RM"):
       #check scallability based off of total use and number os tasks
       if (totalUse <= n*(2**(1/n)-1)):
           return True
       else:
           return False
       
    elif (algo == "EDF"):
        if(totalUse <= 1):
            return True
        else:
            return False
