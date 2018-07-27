#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:28:41 2018

@author: gabriel
"""

import sys
import random
import schedulerModule as S
import testModule as T
from PyQt5.QtWidgets import  *
from PyQt5.QtGui import  *
from PyQt5.QtCore import  *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'RT Scheduler App GUI'
        self.left = 10
        self.top = 10
        self.algo = ""
        self.testing = False
        self.width = (screen.size().width())*0.7
        self.height = (screen.size().height())*0.3
        self.initUI()
        self.tasks = []
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        ###Test functionality
        self.testChk = QCheckBox("Test Mode",self)
        self.testChk.stateChanged.connect(self.toggleTests)
        #Test picker
        self.testCombo = QComboBox(self)
        self.testCombo.addItem("Select Test")
        self.testCombo.addItem("Testcase 1")
        self.testCombo.addItem("Testcase 2")
        self.testCombo.addItem("Testcase 3")
        self.testCombo.addItem("Testcase 4")
        self.testCombo.addItem("Testcase 5")
        self.testCombo.activated[str].connect(self.selected_test)
        self.testCombo.setEnabled(False)
        #### Add new task
        # Name textbox
        self.name = QLineEdit(self) 
        self.name.setPlaceholderText("Name")
        # Duration textbox
        self.duration = QLineEdit(self) 
        self.duration.setPlaceholderText("C")
        # period textbox
        self.period = QLineEdit(self) 
        self.period.setPlaceholderText("T")
        # Color picker
        self.colorBtn = QPushButton(self)
        self.taskColor = self.randomize_color()
        self.colorBtn.setStyleSheet("background-color:"+self.taskColor)
        self.colorBtn.clicked.connect(self.pick_color)
        # Add task button
        self.addBtn = QPushButton('Add Task', self)
        self.addBtn.clicked.connect(lambda: self.add_task(self.taskColor))
        # Task table
        self.createTable()
        # Algo combo box and scheduling info
        self.combo = QComboBox(self)
        self.combo.addItem("Select Algorithm")
        self.combo.addItem("RM")
        self.combo.addItem("EDF")
        self.combo.activated[str].connect(self.selected_algo)
        self.scheduleLbl = QLabel("Is is Schedulable?", self)
        self.schedulable = QLabel("---", self)
        self.schedulable.setStyleSheet("color: grey")
        # Go Button
        self.goBtn = QPushButton('Go!', self)
        self.goBtn.clicked.connect(self.run)
        self.canvas = PlotCanvas(self, width=5, height=4)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.layout.addWidget(self.taskTable, 0, 0, 1, 1) 
        
        self.layout.addWidget(self.combo, 3, 0)
        self.layout.addWidget(self.testChk, 3,1)
        self.layout.addWidget(self.testCombo, 3, 2)
        self.layout.addWidget(self.scheduleLbl,3,3)
        self.layout.addWidget(self.schedulable,3,4)
        self.layout.addWidget(self.goBtn, 3, 6)
        
        self.layout.addWidget(self.name, 5, 0)
        self.layout.addWidget(self.duration, 5, 1)
        self.layout.addWidget(self.period, 5, 2)
        self.layout.addWidget(self.colorBtn, 5, 4)
        self.layout.addWidget(self.addBtn, 5, 6)
        
        self.layout.addWidget(self.canvas, 0, 1, 1, 4)
        self.setLayout(self.layout) 
        self.show()
        self.run()
        
        
    def toggleTests(self, state):
        if (state == 2):
            self.testCombo.setEnabled(True)
        else:
            self.taskTable.setRowCount(0)
            self.tasks = []
            self.testCombo.setEnabled(False)
            
            
    def createTable(self):
        self.taskTable = QTableWidget()
        self.taskTable.setRowCount(0)
        self.taskTable.setColumnCount(4)
        self.taskTable.setHorizontalHeaderLabels(["Name", "Ci", "Ti", "Color"])
#        self.taskTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
#        self.taskTable.resizeColumnsToContents()

    def add_test_tasks(self, tasks):
        for task in tasks:
            self.tasks.append(task)

            rowPosition = self.taskTable.rowCount()
            self.taskTable.insertRow(rowPosition)
            self.taskTable.setItem(rowPosition, 0, QTableWidgetItem(task.name))
            self.taskTable.setItem(rowPosition, 1, QTableWidgetItem(str(task.duration)))
            self.taskTable.setItem(rowPosition, 2, QTableWidgetItem(str(task.period)))
            self.taskTable.setItem(rowPosition, 3, QTableWidgetItem(task.pltColor))
            self.taskTable.item(rowPosition, 3).setBackground(QColor(task.pltColor))
            self.taskTable.resizeColumnsToContents()
        
        
    def selected_test(self, testcase):
#        self.taskTable.clearContents()
        self.taskTable.setRowCount(0)
        self.tasks = []
        
        if(testcase == "Testcase 1"):
            self.add_test_tasks(T.testcase1.tasks)
        elif(testcase == "Testcase 2"):
            self.add_test_tasks(T.testcase2.tasks)
        elif(testcase == "Testcase 3"):
            self.add_test_tasks(T.testcase3.tasks)
        elif(testcase == "Testcase 4"):
            self.add_test_tasks(T.testcase4.tasks)
        elif(testcase == "Testcase 5"):
            self.add_test_tasks(T.testcase5.tasks)
        
        self.selected_algo(self.combo.currentText())  
        
    def selected_algo(self, algo):
        self.algo = algo
        schedulable = S.isSchedulable(self.tasks, algo)
        
        if(schedulable == True):
            self.schedulable.setText("Yes!")
            self.schedulable.setStyleSheet("color: green")
        elif(schedulable == False):
            self.schedulable.setText("No")
            self.schedulable.setStyleSheet("color: Red")
        else:
            self.schedulable.setText("---")
            self.schedulable.setStyleSheet("color: grey")
        
    @pyqtSlot()
    def run(self):
        if (self.algo == "RM"):
            scheduler = S.Scheduler(S.RateMonotonic(self.tasks))
            scheduler.run(0)
#            print(scheduler.result)
            self.canvas.plot(scheduler.result)
        
        elif (self.algo == "EDF"):
            scheduler = S.Scheduler(S.EDF(self.tasks))
            scheduler.run(0)
#            print(scheduler.result) 
            self.canvas.plot(scheduler.result)
        
    def add_task(self, color):
        duration = self.duration.text()
        period = self.period.text()
        name = self.name.text()
        rowPosition = self.taskTable.rowCount()
        self.taskTable.insertRow(rowPosition)
    
        self.taskTable.setItem(rowPosition, 0, QTableWidgetItem(name))
        self.taskTable.setItem(rowPosition, 1, QTableWidgetItem(duration))
        self.taskTable.setItem(rowPosition, 2, QTableWidgetItem(period))
        self.taskTable.setItem(rowPosition, 3, QTableWidgetItem(color))
        self.taskTable.item(rowPosition, 3).setBackground(QColor(color))
        self.taskTable.resizeColumnsToContents()
        
        self.duration.setText("")
        self.period.setText("")
        
        newTask = S.Task(name,int(duration), int(period))
        newTask.pltColor = self.taskColor
        
        
        self.taskColor = self.randomize_color() # start with random color
        self.colorBtn.setStyleSheet("background-color:"+self.taskColor)
        
        self.tasks.append(newTask)
        self.selected_algo(self.algo)

    def pick_color(self):
        color = QColorDialog.getColor()    
        if color.isValid():
            self.taskColor = color.name()
            self.colorBtn.setStyleSheet("background-color:"+self.taskColor)
        
        self.show()
        plt.gcf().clear()
    def randomize_color(self):
        r = lambda: random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(),r(),r())
        return color

class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=65):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xticks([0])
        self.axes.set_yticks([0,10, 30])
        self.axes.set_title("Scheduling")
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        
    def plot(self, scheduling):
        ax = self.figure.add_subplot(111)
        time_ticks = [x[1] for x in scheduling]
        ax.set_xticks(time_ticks)
        for entry in scheduling:    
            t = entry[1]
            event = entry[0]
            print(t, t+event.duration, event.name)
            ax.add_patch(Rectangle((t,0),event.duration,10,color=event.color))
#            ax.annotate(event.name, xy=(event.deadline, 10), xytext=(event.deadline, 25),arrowprops=dict(arrowstyle="->"))
        self.draw()
    
if __name__ == '__main__':
    app=QApplication.instance() # checks if QApplication already exists  
    if not app: # create QApplication if it doesnt exist 
        app = QApplication(sys.argv) 
    screen = app.primaryScreen()
    ex = App()
    sys.exit(app.exec_())
    