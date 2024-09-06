import cv2 # type: ignore
import numpy as np # type: ignore

# Load the pre-trained model
net = cv2.dnn.readNetFromCaffe('gender_deploy.prototxt', 'gender_net.caffemodel')

# Load the image
image = cv2.imread('image.jpg')

# Preprocess the image
image = cv2.resize(image, (224, 224))
blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

# Pass the blob through the network
net.setInput(blob)
outputs = net.forward()

# Get the confidence scores for each class
scores = outputs[0]

# Get the class with the highest confidence score
class_id = np.argmax(scores)

# Get the confidence score for the class with the highest confidence score
confidence = scores[class_id]

# Print the class with the highest confidence score and its confidence score
print(f'Class: {class_id}, Confidence: {confidence:.2f}%')