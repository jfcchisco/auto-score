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
def getTotalKeys(keys, firstKey, lastKey):
    totalKeys = 0
    firstKeyFound = 0
    for key in keys:
        #print(key, totalKeys)
        if(not re.search("b", key)):
            if(re.search(key, lastKey)):
                totalKeys += 1
                print(totalKeys)
                break
            elif(re.search(key, firstKey)):
                firstKeyFound = 1
                totalKeys += 1
            elif(firstKeyFound):
                totalKeys += 1
            
            
    print(totalKeys)
    return totalKeys
        
        

#%%
def main():
    startPixel = pm.startPixel
    finalPixel = pm.finalPixel

    firstKey = pm.firstKey
    lastKey = pm.lastKey

    increments = [["Ab", 0.5], ["Bb", 0.65], ["Db", 0.45], ["Eb", 0.55], ["Gb", 0.35]]

    keys = [    "A1", "Bb1", "B1", "C1", "Db1", "D1", "Eb1", "E1", "F1", "Gb1", "G1", "Ab2", 
                "A2", "Bb2", "B2", "C2", "Db2", "D2", "Eb2", "E2", "F2", "Gb2", "G2", "Ab3", 
                "A3", "Bb3", "B3", "C3", "Db3", "D3", "Eb3", "E3", "F3", "Gb3", "G3", "Ab4", 
                "A4", "Bb4", "B4", "C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab5", 
                "A5", "Bb5", "B5", "C5", "Db5", "D5", "Eb5", "E5", "F5", "Gb5", "G5", "Ab6", 
                "A6", "Bb6", "B6", "C6", "Db6", "D6", "Eb6", "E6", "F6", "Gb6", "G6", "Ab7", 
                "A7", "Bb7", "B7", "C7", "Db7", "D7", "Eb7", "E7", "F7", "Gb7", "G7", "Ab8", 
                "A8", "Bb8", "B8", "C8"
            ]

    totalKeys = getTotalKeys(keys, firstKey, lastKey)

    keySize = float((finalPixel - startPixel) / totalKeys)


    #print(startPixel, finalPixel, totalKeys, keySize)


    keyString = "keys = [ "

    naturalKeys = 0
    firstKeyFound = 0

    center = startPixel + keySize/2

    #print(center)

    for key in keys:
        
        if(key == firstKey):
            firstKeyFound = 1
        
        if(firstKeyFound):
            if(re.search("b", key)):
                for inc in increments:
                    if(re.search(inc[0], key)):
                        coord = center + keySize * inc[1]
                        keyString += "[\"" + key + "\", " + str(int(coord)) + "], "
            else:
                coord = naturalKeys * keySize + keySize / 2 + startPixel
                keyString += "[\"" + key + "\", " + str(int(coord)) + "], "
                center = coord
                naturalKeys += 1
        #print(key, coord)
        if(key == lastKey):
            break

    keyString += "]"

    print(keyString)

if __name__ == "__main__":
    main()