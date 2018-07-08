#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:13:02 2018

@author: gabriel
"""
import schedulerModule as S


t1 = S.Task(20,100)
t2 = S.Task(40,150)
t3 = S.Task(100,350)
tasks = [t1, t2, t3]

RM = S.rateMonotonic(tasks)

scheduler = S.Scheduler(RM)

scheduler.begin(0)
print(scheduler.result)