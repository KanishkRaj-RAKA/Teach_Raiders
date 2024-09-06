import cv2 # type: ignore
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename

# Load pre-trained models face_detector = cv2.dnn.readNetFromTensorflow('models/opencv_face_detector_uint8.pb', 'models/opencv_face_detector.pbtxt')
face_detector = cv2.dnn.readNetFromTensorflow(r'C:\Users\Hp\Desktop\models\opencv_face_detector_uint8.pb', r'C:\Users\Hp\Desktop\models\opencv_face_detector.pbtxt')
age_net = cv2.dnn.readNetFromCaffe(r'C:\Users\Hp\Desktop\models\age_deploy.prototxt', r'C:\Users\Hp\Desktop\models\age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe(r'C:\Users\Hp\Desktop\models\gender_deploy.prototxt', r'C:\Users\Hp\Desktop\models\gender_net.caffemodel')

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# Create GUI
root = Tk()
root.title("Face Detection and Gender Recognition")

# Create label and button to upload image
label = Label(root, text="Select an image:")
label.pack()

def upload_image():
    filepath = askopenfilename()
    if filepath:
        process_image(filepath)

button = Button(root, text="Upload Image", command=upload_image)
button.pack()

# Create canvas to display output
canvas = Canvas(root, width=720, height=640)
canvas.pack()

def process_image(filepath):
    # Read image
    image = cv2.imread(filepath)

    # Resize image
    image = cv2.resize(image, (720, 640))

    # Face detection
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], True, False)
    face_detector.setInput(blob)
    detections = face_detector.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detections[0, 0, i, 3]*image.shape[1])
            y1 = int(detections[0, 0, i, 4]*image.shape[0])
            x2 = int(detections[0, 0, i, 5]*image.shape[1])
            y2 = int(detections[0, 0, i, 6]*image.shape[0])
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Loop for all the faces detected
    for faceBox in faceBoxes:
        face = image[max(0, faceBox[1]-15):min(faceBox[3]+15, image.shape[0]-1),
                     max(0, faceBox[0]-15):min(faceBox[2]+15, image.shape[1]-1)]

        # Extracting the main blob part
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        # Prediction of gender
        gender_net.setInput(blob)
        genderPreds = gender_net.forward()
        gender_classes = ['Male', 'Female', 'Non-Binary', 'Transgender', 'Other']  # Add more classes as needed
        gender = gender_classes[genderPreds[0].argmax()]
        
        # Prediction of age
        age_net.setInput(blob)
        agePreds = age_net.forward()
        age = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)'][agePreds[0].argmax()]

        # Putting text of age and gender
        cv2.putText(image, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4, cv2.LINE_AA)

    # Display output
    cv2.imshow("Output", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

root.mainloop()