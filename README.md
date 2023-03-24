# auto-score
Get piano score from Synthesia video

This script takes a Synthesia piano video and creates the table score in Latex ready format.

First working version is comprised of the following files:
- auto_score.py
- color_calibration.py
- key_printer.py
- parameters.py
- [song].py - bohemian.py serves as example

**Step 1: Get video and create array of keys**

Download video from Youtube, here is the example for bohemian.py (Queen - Bohemian Rhapsody by Sheet Music Boss https://www.youtube.com/watch?v=CNRkEFvg9OI), save it to root folder.
Rename the variable *video* to the file name.

Open one frame of the video where the keyboard can be seen in full and pick a Y-coordinate where it will be convenient to scan if a natural node (white key) is pressed (variable NY) and a where flat note (black key) is pressed (FY). 

Pick the first and last keys that are completely visible, on a complete 7-octave keyobard, the first key should be "A1" and last "C8". Depending on how the video is rendered, there keys are different, for the *bohemian.py* case the first is "A1" while the last is "D7". If a key is cut, don't take into account, it should the first fully visible key at each side.

Locate the X coordinate where the first key starts and the one where the last key ends, for our case it would 0 and 1280.

Save your *song.py* file, open *parameters.py* and rename the first import to load, now it states *import bohemian as pm*, you might change it to the corresponding new file name.

With those variables set, we're ready to execute *key_printer.py*. Run *"python3 key_printer"* and it will print on the console a nested array containing the X coordinate for each of the keys visible in the video. Copy this output and paste it as variable *keys* in your *song.py* file

**Step 2: Calibrate color**

Now, *color_calibration.py* can be executed. Run *"python3 color_calibration.py > out.txt"*, it will print the RGB color of all new keys being pressed for each frame. Look for frames were each type of note is being pressed: Left Hand Natural Node (white key on left hand, usually light blue, variable name LHNN), Left Hand Flat Note (black key on left hand, dark blue, LHFN), Right Hand Natural Note (light green, RHNN) and Right Hand Flat Note (RHFN). 

Save those values in your song.py file. There is an additional variable called *threshold* which represents the tolerance in which those values can change from key to key, default is 20 and usually works well, but there mught be cases where the colors are too similar and the threshold must be reduced, or the colors are changing across the video for a same key and it must be increased.

**Step 3: Execute auto_score**

There is one last variable to set, *merge*. There are videos in which full chords or sets of keys that should be pressed at the same time are separated by 1 or 2 frames, if *merge = 0* then those keys will be separated from the chord. For our case, there are a few chords where key presses are separated by a frame, so *merge = 1* and if that happens then the script joins them. Usually if the keys are correct but are separated in the table, then merge should be adjusted.

After all is ready, execute *"python3 auto_score.py > out.tex"*, this will create the LaTex ready file, you can open the *out.tex* directly in LaTex and compile it as PDF.


