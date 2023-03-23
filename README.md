# auto-score
Get piano score from Synthesia video

This script takes a Synthesia piano video and creates the table score in Latex ready format.

First working version is comprised of the following files:
- auto_score.py
- color_calibration.py
- key_printer.py
- parameters.py
- [song].py - bohemian.py serves as example

**Step 1: Get video and calibrate color**
Download video from Youtube, here is the example for bohemian.py (Queen - Bohemian Rhapsody by Sheet Music Boss), save it to root folder.
Rename the variable *video* to the file name.
Open one frame of the video where the keyboard can be seen in full and pick a Y-coordinate where it will be convenient to scan if a natural node is pressed (variable NY) and a where flat note is pressed (FY). 
Save your *song.py* file, open *parameters.py* and rename the first import to load, now it states *import bohemian as pm*, you might change it to the corresponding new file name.
Now, *color_calibration.py* can be executed. Run *python3 color_calibration.py > out.txt*, it will print the RGB color of all new keys being pressed for each frame. Use those values to (TBD...)
