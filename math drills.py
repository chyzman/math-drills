import json
import math
import sys
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

var1 = 0
var2 = 0
var3 = 0
problemtype = 0
remaining = 0
thesave = []
starttime = 0
endtime = 0

config = open("config.json")
thevalues = json.load(config)

def saveconfig():
    thevalues["count"] = problemcount.value()
    thevalues["max"] = maxvalue.value()
    thevalues["min"] = minvalue.value()
    with open("config.json", "w") as file:
        json.dump(thevalues, file)

def updatemin():
    if minvalue.value() > maxvalue.value():
        maxvalue.setValue(minvalue.value())
    saveconfig()

def updatemax():
    if maxvalue.value() < minvalue.value():
        minvalue.setValue(maxvalue.value())
    saveconfig()

def updateremaining():
    remaininglabel.setText(f"{(problemcount.value()+1)-remaining}/{problemcount.value()}")
    progress.setValue((problemcount.value())-remaining)

def checkanswer():
    global remaining
    givenanswer = int(answer.text())
    correctanswer = (var3 if problemtype == 0 else var1)
    answer.setText("")
    if int(givenanswer) == correctanswer:
        if remaining > 1:
            remaining -= 1
            newproblem()
        else:
            finishthegame()
    else:
        thesave[-1]["fails"] += 1
    updateremaining()

def startthegame():
    global starttime
    global remaining
    starttime = time.time()
    remaining = problemcount.value()
    progress.setMaximum(problemcount.value())
    updateremaining()
    menu.hide()
    mainframe.show()
    newproblem()

def newproblem():
    global var1
    global var2
    global var3
    global problemtype
    var1 = random.randint(minvalue.value(), maxvalue.value())
    var2 = random.randint(minvalue.value(), maxvalue.value())
    var3 = var1 * var2
    problemtype = random.randint(0,1)
    thesave.append({"var1":var1,"var2":var2,"var3":var3,"type":problemtype,"fails":0})
    if problemtype == 0:
        problemlabel.setText(f"{var1} x {var2} =")
    else:
        problemlabel.setText(f"{var3} / {var2} =")

def finishthegame():
    global endtime
    endtime = time.time()
    totaltime = endtime - starttime
    progress.setValue(problemcount.value())

    finalscore = 0
    finalfails = 0
    for i in thesave:
        if i["fails"] == 0:
            finalscore += 1
        else:
            finalfails += i["fails"]

    scorebox = QMessageBox()

    scorebox.setText("You did it i guess")
    scorebox.setInformativeText(f"you got:\n{finalscore} correct\n{finalfails} wrong\nand took:\n{time.strftime('%H:%M:%S', time.gmtime(totaltime)) + str(float(totaltime) - float(math.floor(totaltime)))[1:]}")
    scorebox.setDetailedText(str([i for i in thesave]))
    scorebox.setStandardButtons(QMessageBox.Ok)
            
    scorebox.exec_()
    returntomenu()

def returntomenu():
    global thesave
    thesave = []
    mainframe.hide()
    menu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(300,300)
    window.setWindowTitle("math drills")

    menu = QWidget(window)
    menu.resize(300,300)

    menulayout = QGridLayout(menu)

    title = QLabel(menu, text="Math Drills\nBut It's\nActually Good", font=QFont('Arial', 25))
    menulayout.addWidget(title, 0, 0, 1, 3)

    playbutton = QPushButton(menu, text="Play")
    menulayout.addWidget(playbutton, 1, 0, 1, 3)
    playbutton.clicked.connect(startthegame)

    problemcountlabel = QLabel(menu, text="Problem Count:")
    menulayout.addWidget(problemcountlabel, 2, 0)

    problemcount = QSpinBox(menu, value=thevalues["count"], minimum=1)
    menulayout.addWidget(problemcount, 2, 1, 1, 2)
    problemcount.valueChanged.connect(saveconfig)
    
    rangelabel = QLabel(menu, text="Range:")
    menulayout.addWidget(rangelabel, 3, 0)

    minvalue = QSpinBox(menu, value=thevalues["min"], minimum=-((2**31)-1), maximum=((2**31)-1))
    menulayout.addWidget(minvalue, 3, 1)
    minvalue.valueChanged.connect(updatemin)

    maxvalue = QSpinBox(menu, value=thevalues["max"], minimum=-((2**31)-1), maximum=((2**31)-1))
    menulayout.addWidget(maxvalue, 3, 2)
    maxvalue.valueChanged.connect(updatemax)

    mainframe = QWidget(window)
    mainframe.resize(300,300)
    mainframe.hide()

    mainframelayout = QGridLayout(mainframe)

    remaininglabel = QLabel(mainframe, text="if you see this then it broke")
    mainframelayout.addWidget(remaininglabel, 0, 0)

    progress = QProgressBar(mainframe, minimum=0)
    mainframelayout.addWidget(progress, 0, 1)

    problemlabel = QLabel(mainframe, text="if you see this then it broke")
    mainframelayout.addWidget(problemlabel, 1, 0)
    
    answer = QLineEdit(mainframe)
    mainframelayout.addWidget(answer, 1, 1)
    answer.setValidator(QIntValidator())
    answer.returnPressed.connect(checkanswer)

    giveupbutton = QPushButton(mainframe, text="give up")
    mainframelayout.addWidget(giveupbutton, 2, 0, 1, 2)
    giveupbutton.clicked.connect(returntomenu)

    window.show()
    sys.exit(app.exec_())