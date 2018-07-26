#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:28:41 2018

@author: gabriel
"""

import sys
import random
import schedulerModule as S
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
        self.width = (screen.size().width())*0.7
        self.height = (screen.size().height())*0.3
        self.initUI()
        self.tasks = []
        self.done = []
        self.algo = ""
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #### Add new task
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
        self.layout.addWidget(self.scheduleLbl,3,2)
        self.layout.addWidget(self.schedulable,3,4)
        self.layout.addWidget(self.goBtn, 3, 6)
        
        self.layout.addWidget(self.duration, 5, 0)
        self.layout.addWidget(self.period, 5, 2)
        self.layout.addWidget(self.colorBtn, 5, 4)
        self.layout.addWidget(self.addBtn, 5, 6)
        
        self.layout.addWidget(self.canvas, 0, 1, 1, 6)
        self.setLayout(self.layout) 
        self.show()
        self.run()
        
    def createTable(self):
        self.taskTable = QTableWidget()
        self.taskTable.setRowCount(0)
        self.taskTable.setColumnCount(3)
        self.taskTable.setHorizontalHeaderLabels(["Ci", "Ti", "Color"])
#        self.taskTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
#        self.taskTable.resizeColumnsToContents()

    
        
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

#        if (self.algo == "RM"):
#            scheduler = S.Scheduler(S.RateMonotonic(self.tasks))
#
        scheduler.run(0)
#        print(scheduler.result)
        self.canvas.plot(scheduler.result)
        
    def add_task(self, color):
        duration = self.duration.text()
        period = self.period.text()

        rowPosition = self.taskTable.rowCount()
        self.taskTable.insertRow(rowPosition)
    
        self.taskTable.setItem(rowPosition, 0, QTableWidgetItem(duration))
        self.taskTable.setItem(rowPosition, 1, QTableWidgetItem(period))
        self.taskTable.setItem(rowPosition, 2, QTableWidgetItem(color))
        self.taskTable.item(rowPosition, 2).setBackground(QColor(color))
        self.taskTable.resizeColumnsToContents()
        
        self.duration.setText("")
        self.period.setText("")
        
        newTask = S.Task(int(duration), int(period))
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
            print(t, t+event.duration, event.color)
            ax.add_patch(Rectangle((t,0),event.duration,10,color=event.color))
#            ax.annotate(event.color, xy=(event.deadline, 0), xytext=(event.deadline, 15),arrowprops=dict(arrowstyle="->"))
        self.draw()
    
if __name__ == '__main__':
    app=QApplication.instance() # checks if QApplication already exists  
    if not app: # create QApplication if it doesnt exist 
        app = QApplication(sys.argv) 
    screen = app.primaryScreen()
    ex = App()
    sys.exit(app.exec_())
    