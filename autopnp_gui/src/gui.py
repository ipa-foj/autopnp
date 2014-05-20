import rospy
from std_msgs.msg import String
import threading 

import sys
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QApplication, QMainWindow
from Ui_MainWindow import Ui_MainWindow

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

# ROS - Worker Thread
class RosThread(QThread):
    def __init__(self, ui, parent = None):
        QThread.__init__(self, parent)
        self.ui = ui
        self.sub1 = rospy.Subscriber("/chromosom/addComponent", String, self.add_callback)
        self.sub2 = rospy.Subscriber("/chromosom/remComponent", String, self.rem_callback)
        self.pub_add = rospy.Publisher('/chromosom/addComponent', String)
        self.pub_rem = rospy.Publisher('/chromosom/remComponent', String)
        self.gripper = rospy.Publisher('/TODO', String)

        ui.btnOpen.clicked.connect(self.open_gripper)
        ui.btnClose.clicked.connect(self.close_gripper)

        ui.rLin.clicked.connect(self.lin)
        ui.rDWA.clicked.connect(self.DWA)
 
    def run(self):        
        rospy.spin()
 
    def add_callback(self, data):
        if data.data=="gripper":
           self.ui.gripper.show()
 
    def rem_callback(self, data):
        if data.data=="gripper":
           self.ui.gripper.hide()

    def open_gripper(self):
        self.gripper.publish(String("hello"))
    def close_gripper(self):
        self.gripper.publish(String("hello"))

    def lin(self):
        #todo: move to...
        self.pub_add.publish(String("Linear Navigation"))
        self.pub_rem.publish(String("Dynamic Window Approach"))

    def DWA(self):
        #todo: move to...
        self.pub_rem.publish(String("Linear Navigation"))
        self.pub_add.publish(String("Dynamic Window Approach"))

ui.gripper.hide()

rospy.init_node('chromsome_gut')
th = RosThread(ui)
th.start()

window.show()
sys.exit(app.exec_())

th.join()
