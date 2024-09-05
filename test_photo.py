import cv2
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter window
window = tk.Tk()
window.title("Face Detection")

# Create a button to upload an image
def upload_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", ".jpg .jpeg .png .bmp")])
    if file_path:
        # Read the image
        img = cv2.imread(file_path)
        # Resize the image to half its original size
        img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Create a face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Display the image with detected faces
        cv2.imshow('Faces', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Create a button to upload an image
upload_button = tk.Button(window, text="Upload Image", command=upload_image)
upload_button.pack()

# Run the Tkinter event loop
window.mainloop()