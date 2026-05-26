#!/usr/bin/env python3

import time
import argparse
import cv2
import mediapipe as mp
import numpy as np
import pyautogui

EAR_THRESHOLD = 0.21
CONSEC_FRAMES = 2
COOLDOWN_SEC = 0.9
KEY_TO_PRESS = "down"
SHOW_DEBUG_WINDOW = True
WEBCAM_INDEX = 0

parser = argparse.ArgumentParser(description="Blink to keypress controller")
parser.add_argument("--key", "-k", default=KEY_TO_PRESS)
parser.add_argument("--threshold", type=float, default=EAR_THRESHOLD)
parser.add_argument("--frames", type=int, default=CONSEC_FRAMES)
parser.add_argument("--cooldown", type=float, default=COOLDOWN_SEC)
parser.add_argument("--no-gui", dest="show", action="store_false")
args = parser.parse_args()

EAR_THRESHOLD = args.threshold
CONSEC_FRAMES = args.frames
COOLDOWN_SEC = args.cooldown
KEY_TO_PRESS = args.key
SHOW_DEBUG_WINDOW = args.show

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 387, 385, 263, 380, 373]

def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def compute_ear(landmarks, idxs, w, h):
    pts = [(landmarks[i].x * w, landmarks[i].y * h) for i in idxs]
    p1, p2, p3, p4, p5, p6 = pts
    vert1 = euclidean(p2, p6)
    vert2 = euclidean(p3, p5)
    horiz = euclidean(p1, p4)
    return 0.0 if horiz == 0 else (vert1 + vert2) / (2.0 * horiz)

def check_accessibility_permission_hint():
    try:
        pyautogui.size()
    except Exception:
        print("Warning: pyautogui could not query screen size. On macOS, give Accessibility permission.")
        time.sleep(1)

def main():
    print(f"Blink→Key: pressing '{KEY_TO_PRESS}' on double blink.")
    check_accessibility_permission_hint()

    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        print("Webcam not available.")
        return

    blink_counter = 0
    last_blink_time = 0            # timestamp of the most recent blink
    last_trigger_time = 0          # timestamp when we last sent a keypress (for cooldown)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame capture failed.")
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        ear = None
        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0].landmark
            left_ear = compute_ear(lm, LEFT_EYE_IDX, w, h)
            right_ear = compute_ear(lm, RIGHT_EYE_IDX, w, h)
            ear = (left_ear + right_ear) / 2.0

            if ear < EAR_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= CONSEC_FRAMES:
                    now = time.time()

                    # if we've already triggered recently, ignore until cooldown has passed
                    if now - last_trigger_time < COOLDOWN_SEC:
                        # still in cooldown; skip detection and reset
                        blink_counter = 0
                    else:
                        # check for double blink pattern
                        if now - last_blink_time < 0.35:
                            print(f"Double blink detected. Sending key: {KEY_TO_PRESS}")
                            try:
                                pyautogui.press(KEY_TO_PRESS)
                            except Exception as e:
                                print("Failed to send keypress.")
                                print("Exception:", e)

                            last_trigger_time = now
                            # reset last_blink_time so a third blink doesn't retrigger immediately
                            last_blink_time = 0
                        else:
                            # record the time of this blink as the first of a possible pair
                            last_blink_time = now

                    blink_counter = 0


        if SHOW_DEBUG_WINDOW:
            disp = frame.copy()
            if ear is not None:
                cv2.putText(disp, f"EAR: {ear:.3f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(disp, f"Key: {KEY_TO_PRESS}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.imshow("Blink→Key (press q to quit)", disp)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            try:
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    cap.release()
    if SHOW_DEBUG_WINDOW:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
