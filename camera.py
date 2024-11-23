# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import cv2, os
from keras.models import load_model
import numpy as np
from utils import preprocess_input
# parameters for loading data and images
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

from moviepy.editor import *


class Ui_MainWindow2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 663)
        MainWindow.setStyleSheet("background-color: rgb(67, 152, 255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 501, 101))
        self.label.setStyleSheet("font: 44pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(660, 80, 71, 51))
        self.label_5.setStyleSheet("font: 44pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(660, 20, 121, 31))
        self.label_7.setStyleSheet("font: 20pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(740, 110, 51, 21))
        self.label_8.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(10, 180, 591, 411))
        self.label_25.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 36pt \"微软雅黑\";\n"
"image: url(1/显示背景.png);\n"
"")
        self.label_25.setText("")
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(80, 220, 451, 331))
        self.label_13.setStyleSheet("background-color: transparent;\n"
"background-color: teansparent;")
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.file = QtWidgets.QPushButton(self.centralwidget)
        self.file.setGeometry(QtCore.QRect(0, 610, 61, 51))
        self.file.setStyleSheet("image: url(1/首页.png);\n"
"background-color: transparent;")
        self.file.setText("")
        self.file.setObjectName("file")
        self.small_pic = QtWidgets.QLabel(self.centralwidget)
        self.small_pic.setGeometry(QtCore.QRect(620, 280, 161, 141))
        self.small_pic.setStyleSheet("background-color: transparent;")
        self.small_pic.setText("")
        self.small_pic.setObjectName("small_pic")
        self.shutdown = QtWidgets.QPushButton(self.centralwidget)
        self.shutdown.setGeometry(QtCore.QRect(970, 610, 61, 51))
        self.shutdown.setStyleSheet("image: url(图片/识别.png);\n"
"background-color: transparent;")
        self.shutdown.setText("")
        self.shutdown.setObjectName("shutdown")
        self.camera = QtWidgets.QPushButton(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(890, 610, 61, 51))
        self.camera.setStyleSheet("image: url(图片/相机 (2).png);\n"
"background-color: transparent;")
        self.camera.setText("")
        self.camera.setObjectName("camera")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 260, 151, 71))
        self.pushButton.setStyleSheet("font: 16pt \"Arial\";\n"
"background-color: rgb(188, 188, 188);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 420, 151, 71))
        self.pushButton_2.setStyleSheet("font: 16pt \"Arial\";\n"
"background-color: rgb(188, 188, 188);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label.raise_()
        self.label_5.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_25.raise_()
        self.label_13.raise_()
        self.file.raise_()
        self.small_pic.raise_()
        self.camera.raise_()
        self.shutdown.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        config = ConfigProto()
        config.gpu_options.allow_growth = True
        session = InteractiveSession(config=config)

        emotion_model_path = 'trained_models/float_models/fer2013_mini_XCEPTION.33-0.65.hdf5'
        self.emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
                          4: 'sad', 5: 'surprise', 6: 'neutral'}
        detection_model_path = 'trained_models/facemodel/haarcascade_frontalface_default.xml'

        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        self.emotion_target_size = self.emotion_classifier.input_shape[1:3]

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.img_num=0
        self.cap = cv2.VideoCapture()  # 视频流
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率 循环倒计时
        self.timer_camera.timeout.connect(self.show_camera)  # 若定时器结束，则调用show_camera()

        #两个按钮定义功能
        self.pushButton.clicked.connect(self.button_open_camera_clicked)   #相机打开按钮  连接button_open_camera_clicked函数
        self.pushButton_2.clicked.connect(self.button_close_camera_clicked)#相机关闭按钮  连接button_close_camera_clicked函数
    def button_open_camera_clicked(self):
        self.label_13.setStyleSheet("background: transparent;")
        if self.timer_camera.isActive() == False:  # 若定时器未启动
                flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
                if flag == False:  # flag表示open()成不成功
                # https://www.icode9.com/content-4-96818.html
                    msg = QtWidgets.QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确",
                                                                    buttons=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示

        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label_13.clear()  # 清空视频显示区域
    def button_close_camera_clicked(self):
        self.timer_camera.stop()  # 关闭定时器
        self.cap.release()  # 释放视频流
        self.label_13.clear()  # 清空视频显示区域
        self.label_13.setStyleSheet("background: transparent;")
    def show_camera(self):

        flag, self.image = self.cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        cv2.imwrite('./jietu.jpg', show)
        input_img = self.save_predict('./jietu.jpg')

        cv2.imwrite('res2.png', input_img)
        self.label_13.setStyleSheet("image: url(./res2.png)")  #将检测出的图片放到界面框中
        self.img_num+=1

    def general_predict(self,imggray, imgcolor):
        gray_image = np.expand_dims(imggray, axis=2)  # 224*224*1
        faces = self.face_detection.detectMultiScale(imggray, 1.3, 5)
        res = []
        if len(faces) == 0:
            print('No face')
            return None
        else:
            for face_coordinates in faces:
                x1, y1, width, height = face_coordinates
                x1, y1, x2, y2 = x1, y1, x1 + width, y1 + height
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (self.emotion_target_size))
                except:
                    continue
                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = self.emotion_classifier.predict(gray_face)
                # emotion_probability = np.max(emotion_prediction)
                emotion_label_arg = np.argmax(emotion_prediction)
                res.append([emotion_label_arg, x1, y1, x2, y2])

        return res

    def save_predict(self,imgurl):
        imggray = cv2.imread(imgurl, 0)
        imgcolor = cv2.imread(imgurl, 1)
        ress = self.general_predict(imggray, imgcolor)
        if ress == None:
            print('No face and no image saved')
        try:
            for res in ress:
                label = self.emotion_labels[res[0]]
                lx, ly, rx, ry = res[1], res[2], res[3], res[4]
                cv2.rectangle(imgcolor, (lx, ly), (rx, ry), (0, 0, 255), 2)
                cv2.putText(imgcolor, label, (lx, ly), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        except:
            print('no')
            # cv2.imwrite('images/res_1.png', imgcolor)
        return imgcolor
        # cv2.resize(imgcolor, (741, 421))
        # cv2.imwrite('res.png', imgcolor)
        # self.label_13.setStyleSheet("image: url(res.png)")
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "人脸表情预测"))
        self.pushButton.setText(_translate("MainWindow", "开始预测"))
        self.pushButton_2.setText(_translate("MainWindow", "结束预测"))

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow2()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


