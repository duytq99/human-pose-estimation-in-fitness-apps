import os
import cv2
import sys
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from utils.cls import *
from utils.calc_angle import *
from utils.counter import *
import argparse
import imageio

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--path', type=str, help='Path to video', required=False)
# my_parser.add_argument('--draw', type=bool, help='Draw keypoint', action=store_true, required=False, default=0)
my_parser.add_argument('--draw', help='Draw keypoint', action='store_true')

args = my_parser.parse_args()

if args.path is None:
    input = 0
else:
    input = args.path
rpt_pull = RepetitionCounter(0.8, 0.3)
rpt_push = RepetitionCounter(0.7, 0.3)
rpt_squat = RepetitionCounter(0.7, 0.3)
rpt = dict(PULL = rpt_pull, PUSH = rpt_push, SQUAT = rpt_squat)
cap = cv2.VideoCapture(input)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
count=0
dict_count = dict(SQUAT = 0, PUSH = 0, PULL = 0)
list_act = ['PULL', 'PUSH', 'SQUAT', 'UNKNOWN']
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        image_height, image_width, _ = image.shape
        if count%3==0:
            act, prob, image = classification(image, pose=pose, draw=args.draw)
            if act in [0, 2]:
                if prob<0.5:
                    rpt[list_act[0]].fit(prob)
                    rpt[list_act[2]].fit(prob)
                    dict_count[list_act[0]] = rpt[list_act[0]].n_repeats
                    dict_count[list_act[2]] = rpt[list_act[2]].n_repeats
                elif prob>0.5:
                    rpt[list_act[act]].fit(prob)
                    dict_count[list_act[act]] = rpt[list_act[act]].n_repeats
            elif act==1:
                rpt[list_act[act]].fit(prob)
                dict_count[list_act[act]] = rpt[list_act[act]].n_repeats
        count = count+1
        show = cv2.resize(image, (image_width//2, image_height//2))
        show[:170, :180, :] = np.ones((170, 180, 3))*255
        for ind, (k,v) in enumerate(dict_count.items()):
            cv2.putText(show, k + ': ' + str(v), (0,50*(ind+1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(show, 'PUSHUP: ' + str(round(prob, 3)) , (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Demo', show)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()