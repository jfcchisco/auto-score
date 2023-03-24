#!/usr/bin/python3

import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
import re
import sys
import logging

#module with parameters
import parameters as pm

#%%
def keyPressed(image, key, LHNN, LHFN, RHNN, RHFN):

    
    x = key[1]

    #if((image[y,x]==image[y+1,x]).all and (image[y+1,x]==image[y+2,x]).all and (image[y+2,x]==image[y+3,x]).all and (image[y+3,x]==image[y+4,x]).all):
    
    #else:
    #    return False

    #if(re.search("b", key[0])):
    #    y = pm.FY
    #else:
    #    y = pm.NY
    y = pm.FY if (re.search("b", key[0])) else pm.NY

    color = image[y,x]

    #print('Key:', key[0], ', X: ', x, ', Y: ', y, color)

    th = pm.threshold

    if((abs(color[0]-LHNN[0])<th and abs(color[1]-LHNN[1])<th and abs(color[2]-LHNN[2])<th) and not re.search("b", key[0])):
        return [True,"LH"]
    elif((abs(color[0]-LHFN[0])<th and abs(color[1]-LHFN[1])<th and abs(color[2]-LHFN[2])<th) and re.search("b", key[0])):
        return [True,"LH"]
    elif((abs(color[0]-RHNN[0])<th and abs(color[1]-RHNN[1])<th and abs(color[2]-RHNN[2])<th) and not re.search("b", key[0])):
        return [True,"RH"]
    elif((abs(color[0]-RHFN[0])<th and abs(color[1]-RHFN[1])<th and abs(color[2]-RHFN[2])<th) and re.search("b", key[0])):
        return [True,"RH"]
    else:
        return False

#%%
def merger(merge, frames, leftKeys, rightKeys):


    if(len(frames) != len(leftKeys[0]) or len(frames) != len(rightKeys[0])):
        print("Oh damn here we go again")
        return

    i = 0
    while i < len(frames)-1:
        if(not frames[i+1]):
            return
        
        if((frames[i+1] - frames[i]) <= merge):
            frames.pop(i+1)
            for x in range(5):
                if(leftKeys[x][i+1] != ""):
                    y = 0
                    while y < 5:
                        if(leftKeys[y][i] == ""):
                            leftKeys[y][i] = leftKeys[x][i+1]
                            y = 5
                        y += 1
                leftKeys[x].pop(i+1)
                
                if(rightKeys[x][i+1] != ""):
                    y = 0
                    while y < 5:
                        if(rightKeys[y][i] == ""):
                            rightKeys[y][i] = rightKeys[x][i+1]
                            y = 5
                        y += 1
                rightKeys[x].pop(i+1)
                

        i += 1

  
    return

#%%
def sorter(uLeft, uRight):
    # Sorted lists to return
    # print(uRight)
    sLeft = [[],[],[],[],[]]
    sRight = [[],[],[],[],[]]

    # List of keys from parameters (already sorted)
    keys = pm.keys

    # Takes every unsorted key, then goes through the keys list
    # Then goes inside the 5 elements of the unsorted key and checks if the key from the sorted list is present
    for i in range(len(uRight[0])):
        newKeys = 0
        for key in keys:
            for j in range(5):
                if(uRight[j][i] == key[0]):
                    sRight[newKeys].append(key[0])
                    newKeys += 1
        for x in range(newKeys, 5):
            sRight[x].append('')

    for i in range(len(uLeft[0])):
        newKeys = 0
        for key in keys:
            for j in range(5):
                if(uLeft[j][i] == key[0]):
                    sLeft[newKeys].append(key[0])
                    newKeys += 1
        for x in range(newKeys, 5):
            sLeft[x].append('')

    return sLeft, sRight

#%%
def printLatexHeader():
	print("\\documentclass[oneside]{article}")
	print("\\usepackage[utf8]{inputenc}")
	print("\\usepackage{graphicx}")
	print("\\usepackage[hidelinks]{hyperref}")
	print("\\usepackage{array}")
	print("\\usepackage{lastpage}")
	print("\\usepackage{lipsum}")
	print("\\usepackage{amsmath}")
	print("\\usepackage{parskip}")
	print("\\usepackage{setspace}")
	print("\\usepackage{multicol}")
	print("\\usepackage{currfile}")
	print("\\usepackage[ddmmyyyy]{datetime}")
	print("\\usepackage{tabularx}")
	print("\\usepackage{makecell}")
	print("\\usepackage{float}")
	print("\\usepackage{fancyhdr}")
	print("\\usepackage[export]{adjustbox}")
	print("\\usepackage[a4paper,landscape,total={170mm,257mm},left=7.5mm,right=7.5mm,top=5mm,bottom=5mm]{geometry}")
	print("\\usepackage{xcolor,colortbl}")
	print("\\definecolor{rob}{rgb}{0.0549,0.5059,0.7725}")
	print("\\graphicspath{ {images/} }")
	print("\\setlength{\parindent}{1em}")
	print("\\setlength{\parskip}{1em}")
	print("\\setlength\parindent{0pt}")
	print("\\onehalfspacing")
	print("\\pagenumbering{arabic}")
	print("\\pagestyle{fancy}")
	print("\\fancyhf{}")
	print("\\renewcommand{\headrulewidth}{0pt}")
	print("\\newcolumntype{x}{>{\centering\\arraybackslash}p{15pt}}")

	print("\n\\begin{document}\n"); print("\\textbf{TITLE} \\hfill Page \\thepage\n")

#%% Functions
def main():

    keys = pm.keys

    cap = cv2.VideoCapture(pm.video)

    count = 0
    
    leftKeys = [[],[],[],[],[]]
    rightKeys = [[],[],[],[],[]]
    frames = []
    newKeys = []
    currKeys = []
    prevKeys = []

    while True:
        
        ret, frame = cap.read()

        if not ret:
            break
        
        count += 1

        frameStr = str(count) + ","

        # New method that scans the keyboard
        prevKeys = currKeys
        currKeys = []
        newKeys = []

        #print("Frame: ", count)
        for key in keys:
            keyPress = keyPressed(frame, key, pm.LHNN, pm.LHFN, pm.RHNN, pm.RHFN)
            if(keyPress):
                currKeys.append(key[0] + "-" + keyPress[1])
                frameStr += key[0] + "-" + keyPress[1] + ","

        #print(count, ', CURR: ', currKeys)

        for keyP in currKeys:
            if(keyP not in prevKeys and keyP not in newKeys):
                newKeys.append(keyP)

        if(newKeys):
            newLKeys = 0
            newRKeys = 0
            for newKey in newKeys:
                if(re.search('-LH', newKey)):
                    leftKeys[newLKeys].append(re.sub('-LH','',newKey))
                    newLKeys += 1
                if(re.search('-RH', newKey)):
                    rightKeys[newRKeys].append(re.sub('-RH','',newKey))
                    newRKeys += 1

            frames.append(count)

            for i in range(newLKeys, 5):
                leftKeys[i].append("")

            for i in range(newRKeys, 5):
                rightKeys[i].append("")

            #print("LEFT: ", len(leftKeys[0]), len(leftKeys[1]), len(leftKeys[2]), len(leftKeys[3]), len(leftKeys[4]))
            #print("RIGHT: ", len(rightKeys[0]), len(rightKeys[1]), len(rightKeys[2]), len(rightKeys[3]), len(rightKeys[4]))
            

    # Done with the search on the video, now it's time to write the Latex output tables
    # Tables of 29 columns
    

    if(len(leftKeys[0]) != len(rightKeys[0])):
        print("Something is wrong")
        return
    if(pm.merge > 0):
        merger(pm.merge, frames, leftKeys, rightKeys)
        leftKeys, rightKeys = sorter(leftKeys, rightKeys)

    printLatexHeader()

    lineCount = 0
    firstKey = 0
    lastKey = 0

    cols = 29

    while True:
        line = ""

        #Check if we're about to print the last line
        if(len(leftKeys[i]) < (lineCount) * cols):
            print("\n\\end{document}")   
            return
        else:
            firstKey = lineCount * cols

        if(len(leftKeys[i]) < (lineCount * cols) + cols):
            lastKey = len(leftKeys[0])
        else:
                lastKey = (lineCount * cols) + cols


        

        # Four lines of left keys
        print("\\begin{tabular}{" + "|x" * (lastKey - firstKey) +"|}\n\t\\hline")    

        for i in range(5):
            # 29 keys for each line
            line = "\t\t"

            for x in range(firstKey, lastKey):
                line += " " + leftKeys[i][x] + " " * (3 - len(leftKeys[i][x]))
                if(x == lastKey - 1):
                    line += " \\\\"
                else:
                    line += " &"

            if(re.search('[ABCDEFG]', line)):
                print(line)

       # Four lines of right keys
        print("\t\\hline")    

        for i in range(5):
            # 29 keys for each line
            line = "\t\t"

            for x in range(firstKey, lastKey):
                #print(i, x)
                line += " " + rightKeys[i][x] + " " * (3 - len(rightKeys[i][x]))
                #print(x)
                if(x == lastKey - 1):
                    line += " \\\\"
                else:
                    line += " &"

            if(re.search('[ABCDEFG]', line)):
                print(line)

        print("\t\\hline\n\\end{tabular}\n")

        lineCount +=1

             

        
if __name__ == "__main__":
    main()