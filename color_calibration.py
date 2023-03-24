#!/usr/bin/python3

import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
import re
import sys
import logging

import parameters as pm

#%%
def main():

    keys = pm.keys

    cap = cv2.VideoCapture(pm.video)

    count = 0
    
    while True:
        
        ret, frame = cap.read()

        if not ret:
            break
        
        count += 1

        #color = frame[y,x]

        # Open image for calibration
        #img = cv2.imread('sample2.png')

        for key in keys:
            if(re.search("b", key[0])):
                color = frame[pm.FY, key[1]]
                if(max(color)<40 or min(color)>190):
                    continue
                else:
                    print(count, key[0], color)
            else:
                color = frame[pm.NY, key[1]]
                if(max(color)<40 or min(color)>190):
                    continue
                else:
                    print(count, key[0], color)




if __name__ == "__main__":
    main()