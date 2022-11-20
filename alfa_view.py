from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QFileDialog, QMessageBox
from extractors.BaseExtractor import Detector
import cv2
from deartifacter import deartifacter
import keypoints as keypoints
from mp_extractor import discrete_data_from_mp_json
import matplotlib.pyplot as plt
import json
import angle_calculator as angle_calculator
from moviepy.editor import *
import traceback


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(325, 340, 175, 80))
        self.pushButton.setObjectName("pushButton")

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(250, 90, 310, 30))
        self.pushButton1.setObjectName("pushButton1")
        self.have1 = False

        self.timeCode1 = QtWidgets.QLineEdit(self.centralwidget)
        self.timeCode1.setGeometry(QtCore.QRect(250, 180, 100, 30))
        self.timeCode1.setObjectName("timeCode1")

        self.timeCode2 = QtWidgets.QLineEdit(self.centralwidget)
        self.timeCode2.setGeometry(QtCore.QRect(460, 180, 100, 30))
        self.timeCode2.setObjectName("timeCode2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.add_func()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RunnerAnalysis"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
        self.pushButton1.setText(_translate("MainWindow", "Video path"))

    def add_func(self):
        self.pushButton.clicked.connect(self.btn)
        self.pushButton1.clicked.connect(self.btn1)

    @QtCore.Slot()
    def path(self):
        fname = QFileDialog.getOpenFileName()[0]
        return fname

    def btn(self):

        if (self.have1):
            self.have1 = False
            path = self.file1[0:len(self.file1)-3:1] + "json"  # TODO

            with open(path, 'r', encoding='utf-8') as read_file:
                data = discrete_data_from_mp_json(
                    (json.loads(read_file.read())))

            pair_keys = [(keypoints.LEFT_FOOT_INDEX, keypoints.RIGHT_FOOT_INDEX),  # 0
                         (keypoints.LEFT_ANKLE, keypoints.RIGHT_ANKLE),            # 1
                         (keypoints.LEFT_KNEE, keypoints.RIGHT_KNEE),              # 2
                         (keypoints.LEFT_HIP, keypoints.RIGHT_HIP),                # 3
                         (keypoints.LEFT_SHOULDER, keypoints.RIGHT_SHOULDER)]      # 4

            q1 = 5  # Параметры для сглаживаний
            q2 = 5

            for k in range(len(pair_keys)):  # Уничтожение смены ног из data
                left_key, right_key = pair_keys[k]
                coord_l, coord_r = deartifacter(
                    data[left_key].yvalues, data[right_key].yvalues)

                data[left_key].yvalues = coord_l
                data[right_key].yvalues = coord_r

            bodyangles = angle_calculator.calculate_angles(data)

            if True:
                bodyangles.between_legs = angle_calculator.mov_ave_median(
                    bodyangles.between_legs, q1, q2)
                bodyangles.body_lean = angle_calculator.mov_ave_median(
                    bodyangles.body_lean, q1, q2)
                bodyangles.left_ankle = angle_calculator.mov_ave_median(
                    bodyangles.left_ankle, q1, q2)
                bodyangles.right_ankle = angle_calculator.mov_ave_median(
                    bodyangles.right_ankle, q1, q2)

                bodyangles.left_knee = angle_calculator.mov_ave_median(
                    bodyangles.left_knee, 5, 5)
                bodyangles.right_knee = angle_calculator.mov_ave_median(
                    bodyangles.right_knee, 5, 5)
                bodyangles.left_hip = angle_calculator.mov_ave_median(
                    bodyangles.left_hip, 5, 5)
                bodyangles.right_hip = angle_calculator.mov_ave_median(
                    bodyangles.right_hip, 5, 5)

                plt.figure()
                plt.plot(bodyangles.time, bodyangles.between_legs,
                         label='new between_legs')
                plt.plot(bodyangles.time, bodyangles.body_lean,
                         label='new body_lean')
                plt.plot(bodyangles.time, bodyangles.left_ankle,
                         label='new left_ankle')
                plt.plot(bodyangles.time, bodyangles.right_ankle,
                         label='new right_ankle')
                plt.legend(loc=3)

                plt.figure()
                plt.plot(bodyangles.time, bodyangles.left_knee,
                         label='new left_knee')
                plt.plot(bodyangles.time, bodyangles.right_knee,
                         label='new right_knee')
                plt.plot(bodyangles.time, bodyangles.left_hip,
                         label='new left_hip')
                plt.plot(bodyangles.time, bodyangles.right_hip,
                         label='new right_hip')
                plt.legend(loc=3)

            plt.show()

        else:
            print("Try other buttons")

    def btn1(self):
        self.file1 = self.path()
        try:
            self.clip = VideoFileClip(self.file1).subclip(
                int(self.timeCode1.text()), int(self.timeCode2.text()))
            self.clip.write_videofile(
                self.file1[0:len(self.file1)-4:1] + "_clip" + ".mp4")
            cap = cv2.VideoCapture(
                self.file1[0:len(self.file1)-4:1] + "_clip" + ".mp4")
            det = Detector(cap, self.file1[0:len(
                self.file1)-3:1] + "json", is_file=True)
            det.run()
            self.have1 = True
        except Exception:
            print(traceback.format_exc())
            self.showDialog('Try again')

    def showDialog(self, txt):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(txt)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
