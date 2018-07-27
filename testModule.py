#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:13:02 2018

@author: gabriel
"""
import schedulerModule as S

class TestCase:
    def __init__(self, test_id ,tasks):
        self.test_id = test_id
        self.tasks = tasks

        
### Testcase 1
t1 = S.Task("A",20,100)
t1.pltColor = 'red'
t2 = S.Task("B", 40,150)
t2.pltColor = 'green'
t3 = S.Task("C",100,350)
t3.pltColor = 'blue'
tasks = [t1, t2, t3]
testcase1 = TestCase(1,tasks)

### Testcase 2
t1 = S.Task("A",10,20)
t1.pltColor = 'red'
t2 = S.Task("B",25,50)
t2.pltColor = 'green'
tasks = [t1, t2]
testcase2 = TestCase(2,tasks)

### testcase 3
t1 = S.Task("A",1,2)
t1.pltColor = 'red'
t2 = S.Task("B",1,4)
t2.pltColor = 'green'
t3 = S.Task("C",1,8)
t3.pltColor = 'blue'
t4 = S.Task("D",1,16)
t4.pltColor = 'yellow'
tasks = [t1, t2, t3,t4]
testcase3 = TestCase(3,tasks)

### testcase 4
t1 = S.Task("A",2,10)
t1.pltColor = 'red'
t2 = S.Task("B",1,5)
t2.pltColor = 'green'
t3 = S.Task("C",5,30)
t3.pltColor = 'blue'
t4 = S.Task("D",2,15)
t4.pltColor = 'yellow'
tasks = [t1, t2, t3,t4]
testcase4 = TestCase(4, tasks)

### testcase 5
t1 = S.Task("A",1,8)
t1.pltColor = 'red'
t2 = S.Task("B",2,5)
t2.pltColor = 'green'
t3 = S.Task("C",4,10)
t3.pltColor = 'blue'
tasks = [t1, t2, t3]
testcase5 = TestCase(5, tasks)