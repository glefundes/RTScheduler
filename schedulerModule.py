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
        self.duration = duration
        self.period = period
        self.use = self.duration/self.period
        self.remaining = duration
        self.returnsAt = period
        
        self.pltColor = 'blue'
    def printTask(self):
        print("(C:"+str(self.duration)+" T:"+str(self.period)+")")
            
class rateMonotonic:
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
    
class Scheduler:
    def __init__(self, algo):
        self.result = []
        self.done = []
        self.algo = algo
        self.scaleLimit = 2*(max(self.algo.tasks, key=attrgetter('period'))).period
        
        if(algo == "RM"):
            self.algo = rateMonotonic(self.tasks)
            
    def begin(self, t):
        if (t <= self.scaleLimit):
            tasks = self.algo.getTasks()
            nextTask = (min(tasks, key=attrgetter('priority')))# Get highest priority task
            finishingTime = t + nextTask.duration        
            self.result.append ((nextTask, t))
            
            
            # No tasks completed yet
            if(len(self.done) == 0):
                self.done.append(nextTask)
                tasks.remove(nextTask)
                self.algo.setTasks(tasks)
                self.begin(finishingTime)
            
            # check if next task can be completed without preemption
            else:
                # Check returning tasks for returning time, find the one that returns the earliest
                for task in self.done:
                    task.returnsAt = -((-t) // task.period) * task.period
                nextReturning = (min(self.done, key=attrgetter('returnsAt')))
                
                # Preemption: some task returns before the end of current task, and it has priority
                if (finishingTime >= nextReturning.returnsAt and nextReturning.priority < nextTask.priority):
                    nextTask.remaining -= (nextReturning.returnsAt - t)   
                    finishingTime = t + (nextReturning.returnsAt - t)
                    tasks.append(nextReturning)
                    self.algo.setTasks(tasks)
                    self.begin(finishingTime)
                
                # current task can finish before the next one returning
                else:
                    # check if task was split up
                    if(nextTask.period != nextTask.remaining):
                        finishingTime = t + nextTask.remaining
                        nextTask.remaining = nextTask.period
                        
                    self.done.append(nextTask)
                    tasks.remove(nextTask)
                    self.algo.setTasks(tasks)
                    self.begin(finishingTime)
             


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
    