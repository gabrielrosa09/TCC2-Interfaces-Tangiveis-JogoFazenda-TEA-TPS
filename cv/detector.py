import cv2
import mediapipe as mp
import time


class HandDetector:

    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.gesture_start_time = {}
        self.current_gesture = None

    def find_hands(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmarks(self, img, hand_no=0):

        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def recognize_gesture(self, lm_list):

        if not lm_list:
            return None

        tip_ids = [4, 8, 12, 16, 20]
        fingers = []

        # Lógica para o polegar (eixo X)
        if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Lógica para os outros 4 dedos (eixo Y)
        for id in range(1, 5):
            if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Gesto "ROCK" (🤟)
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            return "ROCK"

        # Gesto "PUNHO" (✊)
        if all(finger == 0 for finger in fingers):
            return "PUNHO"

        # Gesto "PAZ" (✌️)
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            return "PAZ"

        # Gesto "UM" (☝️)
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            return "UM"

        # Gesto "MAO_ABERTA" (🖐️)
        if all(finger == 1 for finger in fingers):
            return "MAO_ABERTA"

        return None

    def check_continuous_gesture(self, gesture, duration=2):

        if gesture != self.current_gesture:
            self.current_gesture = gesture
            self.gesture_start_time = time.time()
            return None

        if self.current_gesture is not None:
            elapsed_time = time.time() - self.gesture_start_time
            if elapsed_time >= duration:

                self.gesture_start_time = time.time()
                return self.current_gesture

        return None