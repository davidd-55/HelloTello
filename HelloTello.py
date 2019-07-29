"""
This is HelloTello, an app that allows for RC or AI control of a Tello drone!
Huge thanks to Jabrils (YouTube @Jabrils) for inspiration, and Pomona HPC for employment.
This implementation only follows faces. Future update will support other HAAR cascades.
"""

from tello import Tello
import cascade_importer as ci
import time
import sys
import cv2
import numpy as np

def intro():
    """
    Prints program info to console and starts program when user is ready
    params: none
    return: True/False; True to continue program or False to quit
    """

    print("Welcome to the HelloTello app!\nIn manual mode, control Tello from a virtual RC remote.\n"
          "If manual mode is set to 'OFF', Tello will follow a face!\n")
    print("Before running this program, please ensure that you have python 3.6+, "
          "NumPy,\nand OpenCV-Python installed on your system. Check requirements.txt for more info.\n")
    print("Once you have looked over the controls, press any key + 'Enter' to continue or 'Q' to quit.\n")
    print("Here are the available controls:")
    print("\tESC - Emergency Motor Shutoff.\n\tT - Takeoff.\n\tQ - Exit.\n\tQ - Land.\n\tW - Forward.\n\tS - Backward"
          "\n\tA - Left.\n\tD - Right.\n\tI- Up.\n\tK - Down.\n\t"
          "J - Rotate Left.\n\tL - Rotate Right.\n\tM - Enable/Disable Manual Mode."
          "\n\t1 - Set Low Speed.\n\t2 - Set Normal Speed.\n\t3 - Set High Speed.")

    usr_in = input("")
    if usr_in == "q":
        return False
    else:
        return True

def initialize():
    """
    A simple function that initializes Tello by connecting, getting battery
    info, and starting video stream. Exits program if Tello could not connect.
    Params: none
    Returns: no return
    """

    # establish connection, exit if fails
    conn = t.connect()
    if not conn:
        print("Could not establish Tello connection. Reboot Tello, reconnect, and try again.")
        sys.exit()
    time.sleep(1)

    t.get_battery()
    time.sleep(1)

    # in case stream was already on
    t.streamoff(response=False)
    time.sleep(1)

    # get stream data, exit if fails
    strm = t.streamon(response=False)

def facedetect(img, cscde, mode):
    """
    Runs OpenCV image processing on an image (frame) and draws a box around detected
    object. Returns an np.array (x, y, z) of center coordinates and z = target box area + 1
    params:
        img - image of size 960x720
        cascade - HAAR cascad identifier in .xml format
        mode - boolean that determines text displayed on frame
    returns: face_coords - center coords of object detected by OpenCV
    """

    # initiate empty face coordinates x, y, area z in center; z = target dist+1 for face recognition line 248
    face_coords = np.array((480, 360, 9217))

    # grayscale and analyze frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cscde.detectMultiScale(gray, scaleFactor=2, minNeighbors=5) # 1.3, 5)

    # write flight mode on frame
    if mode:
        cv2.putText(img, "Manual Controls: ON", bottom_left_corner, font, 1, (0, 0, 255), 2)
    else:
        cv2.putText(img, "Manual Controls: OFF", bottom_left_corner, font, 1, (0, 0, 255), 2)

    # if face found, extract face coords and draw bounding box on frame
    for (x, y, w, h) in faces:
        x_center = int(x + (w/2))
        y_center = int(y + (h/2))
        face_coords = np.array((x_center, y_center, w*h))
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
        cv2.circle(img, (x_center, y_center), 10, (255, 0, 0), 1)
        cv2.line(img, (480, 360), (x_center, y_center), (255, 255, 255), 1)

    # show frame and return face coords
    cv2.imshow('stream', img)
    return face_coords

if __name__ == "__main__":
    
    # initial speed setting
    S = 30

    # enables controls and sets drone takeoff status
    MANUAL_MODE = True
    taken_off = False
    running = True

    # set intial velocities
    for_back_v = 0
    left_right_v = 0
    up_down_v = 0
    yaw_v = 0
    
    # for auto-adjust if face lost
    last_yaw_direction = 0

    # Keeps Tello from constantly fidgeting
    safety_x = 100
    safety_y = 100

    # following distances based on area of bounding box
    cam_center_coords = np.array((480, 360, 9216)) # z is target distance (bounding box area)

    # give user inputs
    if not intro():
        print("Exiting HelloTello...")
        sys.exit()

    # setup cascade and text for stream
    cas_lst = ci.cascade_finder()
    print("Now, choose what Tello will track.\nAvailable libraries:")
    for cascade in cas_lst:
        print(cascade)
    cascade_dir = "cascades/" + ci.usr_choice(cas_lst)
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner = (10, 710)
    cascade = cv2.CascadeClassifier(cascade_dir)

    # initialize Tello and video stream
    t = Tello()
    time.sleep(1)
    initialize()

    # loop controls once drone is connected
    while running:

        # detect face and find coordinates if exists
        frame_read = t.get_frame_read()
        frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
        frameRet = frame_read.frame
        face_center_coords = facedetect(frameRet, cascade, MANUAL_MODE)

        # velocity printout
        if S == 30:
            text = "Speed: Low"
        elif S == 65:
            text = "Speed: Normal"
        elif S == 100:
            text = "Speed: Fast"

        k = cv2.waitKey(30) & 0xFF
        
        # controls as given in intro() function
        if k == ord('t'):
            t.takeoff(response=False)
            taken_off = True

        if k == ord('m'):
            if MANUAL_MODE == True:
                MANUAL_MODE = False
            else:
                MANUAL_MODE = True

        if k == ord('q'):
            running = False
            if taken_off:
                t.land()
        
        if k == 27:
            print("Shutting down motors...")
            t.emergency()
            break

        if k == 49:          
            if S != 30:
                print("Setting speed to 'low'")
                S = 30
            else:
                print("Speed already set to low")

        if k == 50:
            if S != 65:
                print("Setting speed to 'normal'")
                S = 65
            else:
                print("Speed already set to normal")

        if k == 51:
            if S != 100:
                print("Setting speed to 'high'")
                S = 100
            else:
                print("Speed already set to high")
        
        # runs manual controls
        if MANUAL_MODE:

            if k == ord('a'):
                left_right_v = -S
            elif k == ord('d'):
                left_right_v = S
            else:
                left_right_v = 0
        
            if k == ord('w'):
                for_back_v = S
            elif k == ord('s'):
                for_back_v = -S
            else:
                for_back_v = 0

            if k == ord('i'):
                up_down_v = S
            elif k == ord('k'):
                up_down_v = -S
            else: 
                up_down_v = 0

            if k == ord('j'):
                yaw_v = -S
            elif k == ord('l'):
                yaw_v = S
            else: 
                yaw_v = 0

            if k == ord('q'):
                t.land()
                running = False

            t.send_rc_control(left_right_v, for_back_v, up_down_v, yaw_v, verbose=True)

        # runs AI controls
        else:
            move_vector = cam_center_coords - face_center_coords
            object_bool = (move_vector != np.array((0, 0, -1)))
            object_detected = object_bool.all()

            if k == ord('q'):
                t.land()
                running = False
            
            # AI movement if OpenCV detects object
            if object_detected:

                # print(move_vector)
                
                if move_vector[0] < -safety_x:
                    yaw_v = S
                    last_yaw_direction = 1
                elif move_vector[0] > safety_x:
                    yaw_v = -S
                    last_yaw_direction = -1
                else: 
                    yaw_v = 0

                if move_vector[1] < -safety_y:
                    up_down_v = -S
                elif move_vector[1] > safety_y:
                    up_down_v = S
                else:
                    up_down_v = 0

                if move_vector[2] < 0:
                    for_back_v = -S 
                elif move_vector[2] > 0:
                    for_back_v = S 
                else:
                    for_back_v = 0

                t.send_rc_control(left_right_v, for_back_v, up_down_v, yaw_v, verbose=True)

            else:   
                # if no face, rotate until finding one
                print("No face detected.")
                
                t.send_rc_control(0, 0, 0, int(last_yaw_direction * 20), verbose=False)

    # cleanup after loop terminates
    cv2.destroyAllWindows
    t.end()
