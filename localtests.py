#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:13:02 2018

@author: gabriel
"""

# Testcase 1
t1 = S.Task(20,100)
t1.pltColor = 'red'
t2 = S.Task(40,150)
t2.pltColor = 'green'
t3 = S.Task(100,350)
t3.pltColor = 'blue'
tasks = [t1, t2, t3]
RM = S.RateMonotonic(tasks)
scheduler = S.Scheduler(RM)
# testcase 2

t1 = S.Task(10,20)
t1.pltColor = 'red'
t2 = S.Task(25,50)
t2.pltColor = 'green'
tasks = [t1, t2]
RM = S.RateMonotonic(tasks)
scheduler = S.Scheduler(RM)

# testcase 3

t1 = S.Task(1,2)
t1.pltColor = 'red'
t2 = S.Task(1,4)
t2.pltColor = 'green'
t3 = S.Task(1,8)
t3.pltColor = 'blue'
t4 = S.Task(1,16)
t4.pltColor = 'yellow'
tasks = [t1, t2, t3,t4]
RM = S.RateMonotonic(tasks)
scheduler = S.Scheduler(RM)

# testcase 4

t1 = S.Task(2,10)
t1.pltColor = 'red'
t2 = S.Task(1,5)
t2.pltColor = 'green'
t3 = S.Task(5,30)
t3.pltColor = 'blue'
t4 = S.Task(2,15)
t4.pltColor = 'yellow'
tasks = [t1, t2, t3,t4]
RM = S.RateMonotonic(tasks)
scheduler = S.Scheduler(RM)

# testcase 5

t1 = S.Task(1,8)
t1.pltColor = 'red'
t2 = S.Task(2,5)
t2.pltColor = 'green'
t3 = S.Task(4,10)
t3.pltColor = 'blue'
tasks = [t1, t2, t3]
EDF = S.EDF(tasks)
scheduler = S.Scheduler(EDF)