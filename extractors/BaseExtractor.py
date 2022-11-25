import json

import cv2
import mediapipe as mp


class Detector(object):
    """
    Detector class with mediapipe
    """

    def __init__(self, cap, output_fname, is_file=False, show_res=False):
        """
        Initialization
        @param cap: cv2.VideoCapture object
        @param output_fname: name of output json file
        @param is_file: True if capture object belongs to video file, else False
        @param show_res: if True, result window will be displayed
        """
        self.show_res = show_res
        self.is_file = is_file
        self.cap = cap
        self.out_name = output_fname
        self.points = []
        self.counter = 0
        success, image = self.cap.read()
        self.vid_writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'MP4V'), 15,
                                          (image.shape[1], image.shape[0]))

    def construct_state(self, landmarks):
        """
        Extracts points from landmarks structure
        @param landmarks: mediapipe landmarks structure
        @return:
        """
        state_dict = []
        for i, landmark in enumerate(landmarks):
            state_dict.append({'id': i,
                               'x': landmark.x,
                               'y': landmark.y,
                               'z': landmark.z,
                               'visibility': landmark.visibility})
        self.points.append({'frame': self.counter,
                            'points': state_dict})

    def run(self):
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=2) as pose:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    if self.is_file:
                        break
                    else:
                        continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                if results.pose_landmarks:
                    self.construct_state(results.pose_landmarks.landmark)
                if self.show_res:
                    image.flags.writeable = True
                    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    cv2.imshow('Result', cv2.flip(image, 1))
                    self.vid_writer.write(image)
                    if cv2.waitKey(5) & 0xFF == 27 and not self.is_file:
                        break
                self.counter += 1
        self.cap.release()
        self.vid_writer.release()
        with open(self.out_name, 'w') as f:
            json.dump(self.points, f)


if __name__ == '__main__':
    cap = cv2.VideoCapture('D:/RunnerAnalysis/data/2.MOV')
    det = Detector(cap, 'D:/RunnerAnalysis/data/2.json', is_file=True)
    det.run()
