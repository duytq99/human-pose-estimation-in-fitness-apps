import cv2
import numpy as np
import mediapipe as mp
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

import pickle
from utils.calc_angle import *

load_pca_pull = pickle.load(open('model_ml/pca_pull.sav', 'rb'))
load_pca_push = pickle.load(open('model_ml/pca_push.sav', 'rb'))
load_pca_squat = pickle.load(open('model_ml/pca_squat.sav', 'rb'))
load_pca_all = pickle.load(open('model_ml/pca_all.sav', 'rb'))

load_svm_pull = pickle.load(open('model_ml/svm_pull.sav', 'rb'))
load_svm_push = pickle.load(open('model_ml/svm_push.sav', 'rb'))
load_svm_squat = pickle.load(open('model_ml/svm_squat.sav', 'rb'))

load_rf_all = pickle.load(open('model_ml/rf_all.sav', 'rb'))

model_dict = dict(
    pca_pull = load_pca_pull,
    pca_push = load_pca_push,
    pca_squat = load_pca_squat,
    pca_all = load_pca_all,
    svm_pull = load_svm_pull,
    svm_push = load_svm_push,
    svm_squat = load_svm_squat,
    rf_all = load_rf_all
)

kp_name = [
    'LEFT_SHOULDER', 
    'RIGHT_SHOULDER', 
    'LEFT_ELBOW', 
    'RIGHT_ELBOW', 
    'LEFT_HIP', 
    'RIGHT_HIP', 
    'LEFT_WRIST', 
    'RIGHT_WRIST', 
    'LEFT_KNEE', 
    'RIGHT_KNEE', 
    'LEFT_ANKLE', 
    'RIGHT_ANKLE'
]
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
count = 0

def classification(image, model_dict=model_dict, kp_name=kp_name, pose=None, draw=False):
    # PCA
    pca_squat = model_dict['pca_squat']
    pca_push = model_dict['pca_push']
    pca_pull = model_dict['pca_pull']
    pca_all = model_dict['pca_all']

    PCA = [pca_pull, pca_push, pca_squat]
    # SVM
    svm_squat = model_dict['svm_squat']
    svm_push = model_dict['svm_push']
    svm_pull = model_dict['svm_pull']

    SVM = [svm_squat, svm_push, svm_squat]
    # SVM
    rf_all = model_dict['rf_all']
    #Process image
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape
    results = pose.process(image)
    if results.pose_landmarks:
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if draw==True:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        kp = {}
        for pos in kp_name:
            kp[pos] = [results.pose_landmarks.landmark[getattr(mp_pose.PoseLandmark, pos)].x * image_width,
                      results.pose_landmarks.landmark[getattr(mp_pose.PoseLandmark, pos)].y * image_height]

        l = calc_l3(kp)
        s = np.min([slope(kp['LEFT_SHOULDER'], kp['LEFT_ANKLE']),
                    slope(kp['RIGHT_SHOULDER'], kp['RIGHT_ANKLE'])])
        angle = np.array([])
        for k in l.keys():
            angle = np.append(angle, calc_angles(l[k]))
        angle = np.append(angle, s)
        prob_act = rf_all.predict_proba([angle])[0]
        prob_choose = prob_act>np.array([0.8, 0.8, 0.42])
        act = prob_choose.argmax()
        prob = SVM[act].predict_proba(PCA[act].transform([angle]))[0][0]
        if act==0: prob = 1-prob
        if prob_choose[act]:
            # print('passs')
            return act, prob, image
        else:
            # print('not passs')
            return 3, 0., image
    else:
        return 3, 0., image