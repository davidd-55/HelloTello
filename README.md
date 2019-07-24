# **HelloTello**

Hello all, welcome to **HelloTello!** 

This program displays a Tello drone video stream and allows a user to control a the drone either through keyboard controls (noted below) or in an 'auto' mode where the drone will follow a face that it recognizes using OpenCV. 

## **Functionality:**
- Interact with Tello using keyboard
- See Tello video stream on desktop and any faces it recognizes
- Automatically pilot Tello towards any faces in video frame (_don't worry, it won't fly into you!_)
    
## **Controls:**
- W,A,S,D: Forward, Backward, Left, Right
- Up,Down,Left,Right Arrows: Up, Down, Rotate Left/Right
- T: Takeoff
- L: Land and Exit
- ESC: Emergency Motor Shutoff
- M: Enable/Disable Manual Mode
- 1,2,3: Set Speed Low, Normal, High
    
## **Requirements (see requirements.txt):**
1. Python 3.6+ (let me know if it works on lower versions!)
2. NumPy 1.16.4
3. OpenCV-Python 4.1.0.25
    
## **Install and Run:**
- Install dependencies:
    $ pip install -r requirements.txt
    
- Run: Open a Terminal in /path/to/HelloTello and type:
    $ python TelloRC.py
    
- Note: You may have to add a '3' after pip and python commands if you have multiple python versions installed on your system.