import sys

import cv2,os
from keras.models import load_model
import numpy as np
from tqdm import tqdm
from utils import preprocess_input
# parameters for loading data and images
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

emotion_model_path = 'trained_models/float_models/fer2013_mini_XCEPTION.33-0.65.hdf5'
emotion_labels = {0:'angry',1:'disgust',2:'fear',3:'happy',
                4:'sad',5:'surprise',6:'neutral'}
detection_model_path = 'trained_models/facemodel/haarcascade_frontalface_default.xml'

emotion_classifier = load_model(emotion_model_path, compile=False)
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_target_size = emotion_classifier.input_shape[1:3]

def general_predict(imggray,imgcolor):
    gray_image = np.expand_dims(imggray,axis=2)#224*224*1
    faces = face_detection.detectMultiScale(imggray, 1.3, 5)
    res = []
    if len(faces)==0:
        print('No face')
        return None
    else:
        for face_coordinates in faces:
            x1,y1,width,height = face_coordinates
            x1,y1,x2,y2 = x1,y1,x1+width,y1+height
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue
            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            #emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            res.append([emotion_label_arg,x1,y1,x2,y2])

    return res

def save_predict(imgurl,targeturl='images/predicted_test_image.png'):
    imggray = cv2.imread(imgurl,0)
    imgcolor = cv2.imread(imgurl,1)
    ress = general_predict(imggray,imgcolor)
    if ress==None:
        print('No face and no image saved')
    for res in ress:
        label = emotion_labels[res[0]]
        lx,ly,rx,ry = res[1],res[2],res[3],res[4]
        cv2.rectangle(imgcolor,(lx,ly),(rx,ry),(0,0,255),2)
        cv2.putText(imgcolor,label,(lx,ly),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)         
    # cv2.imwrite('images/res_1.png', imgcolor)
    cv2.imwrite('res.png', imgcolor)

save_predict('test/11.png')
