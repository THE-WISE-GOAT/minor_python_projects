import sys
import time
import argparse
import platform
import subprocess
import cv2
import mediapipe as mp

parser = argparse.ArgumentParser()
parser.add_argument("--camera", type=int, default=0)
parser.add_argument("--fist-frames", type=int, default=3) # Faster trigger
args = parser.parse_args()

def lock_screen():
    os_name = platform.system()
    if os_name == "Linux":
        for cmd in [
            ["loginctl", "lock-session"],
            ["xdg-screensaver", "lock"],
            ["gnome-screensaver-command", "--lock"],
        ]:
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except FileNotFoundError:
                continue
    elif os_name == "Darwin":
        subprocess.Popen(
            ["osascript", "-e", 'tell application "System Events" to key code 12 using {control down, command down}'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    elif os_name == "Windows":
        import ctypes
        ctypes.windll.user32.LockWorkStation()

def release_resources():
    try: cap.release()
    except: pass
    try: hands.close()
    except: pass

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, # 1 hand is faster for background processing
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

os_name = platform.system()
if os_name == "Linux":
    cap = cv2.VideoCapture(args.camera, cv2.CAP_V4L2)
elif os_name == "Windows":
    cap = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)
elif os_name == "Darwin":
    cap = cv2.VideoCapture(args.camera, cv2.CAP_AVFOUNDATION)
else:
    cap = cv2.VideoCapture(args.camera)

if not cap.isOpened():
    sys.exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) 

FINGER_TIPS = [8, 12, 16, 20]   
FINGER_PIPS = [6, 10, 14, 18]   
THUMB_TIP = 4
THUMB_IP = 3

def is_fist(landmarks, hand_label):
    lm = landmarks.landmark
    folded = 0
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        if lm[tip].y > lm[pip].y:   
            folded += 1
            
    if hand_label == "Right":
        thumb_curled = lm[THUMB_TIP].x > lm[THUMB_IP].x
    else:
        thumb_curled = lm[THUMB_TIP].x < lm[THUMB_IP].x
        
    return folded == 4 and thumb_curled

fist_frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.05)
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    fist_detected = False

    if results.multi_hand_landmarks:
        for hand_lm, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = hand_info.classification[0].label   
            if is_fist(hand_lm, label):
                fist_detected = True
                break 

    if fist_detected:
        fist_frame_count += 1
    else:
        fist_frame_count = max(0, fist_frame_count - 1)

    if fist_frame_count >= args.fist_frames:
        release_resources()
        lock_screen()
        sys.exit(0)
        
    time.sleep(0.01) # Keep CPU usage down