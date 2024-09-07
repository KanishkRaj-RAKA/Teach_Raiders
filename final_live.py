import cv2
import time
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
import requests
import numpy as np

# Load pre-trained models
face_detector = cv2.dnn.readNetFromTensorflow(r'C:\Users\Hp\Desktop\models\opencv_face_detector_uint8.pb', 
                                               r'C:\Users\Hp\Desktop\models\opencv_face_detector.pbtxt')
age_net = cv2.dnn.readNetFromCaffe(r'C:\Users\Hp\Desktop\models\age_deploy.prototxt', 
                                   r'C:\Users\Hp\Desktop\models\age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe(r'C:\Users\Hp\Desktop\models\gender_deploy.prototxt', 
                                      r'C:\Users\Hp\Desktop\models\gender_net.caffemodel')

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# Create GUI
root = Tk()
root.title("Face Detection and Gender Recognition")

# Create label and button to start IP Webcam
label = Label(root, text="Start IP Webcam:")
label.pack()

def start_ip_webcam():
    process_ip_webcam()

button = Button(root, text="Start", command=start_ip_webcam)
button.pack()

# Create canvas to display output
canvas = Canvas(root, width=400, height=300)
canvas.pack()

def process_ip_webcam():
    # IP Webcam URL
    url = "http://192.168.29.209:8080/video"
    video_capture = cv2.VideoCapture(url)

    men_count = 0
    women_count = 0

    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            break

        # Resize frame
        frame = cv2.resize(frame, (720, 640))

        # Face detection
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)
        face_detector.setInput(blob)
        detections = face_detector.forward()
        faceBoxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                x1 = int(detections[0, 0, i, 3]*frame.shape[1])
                y1 = int(detections[0, 0, i, 4]*frame.shape[0])
                x2 = int(detections[0, 0, i, 5]*frame.shape[1])
                y2 = int(detections[0, 0, i, 6]*frame.shape[0])
                faceBoxes.append([x1, y1, x2, y2])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Loop for all the faces detected
        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1]-15):min(faceBox[3]+15, frame.shape[0]-1),
                         max(0, faceBox[0]-15):min(faceBox[2]+15, frame.shape[1]-1)]

            # Extracting the main blob part
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            # Prediction of gender
            gender_net.setInput(blob)
            genderPreds = gender_net.forward()
            gender_classes = ['Male', 'Female']  # Removed other classes as the model only supports two classes
            gender = gender_classes[genderPreds[0].argmax()]

            if gender == 'Male':
                men_count += 1
            elif gender == 'Female':
                women_count += 1

            # Putting text of age and gender
            cv2.putText(frame, f'{gender}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4, cv2.LINE_AA)

        # Display count of males and females
        cv2.putText(frame, f'Males: {men_count}, Females: {women_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4, cv2.LINE_AA)

        # Display output
        cv2.imshow("Output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

root.mainloop()