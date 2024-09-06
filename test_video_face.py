import cv2
import tkinter as tk
from tkinter import filedialog
 
# Create a Tkinter window
window = tk.Tk()
window.title("Face Detection")

# Create a button to upload a video
def upload_video():
    # Open a file dialog to select a video
    file_path = filedialog.askopenfilename(title="Select a video", filetypes=[("Video files", ".mp4 .avi .mov")])
    if file_path:
        # Create a video capture object
        cap = cv2.VideoCapture(file_path)
        
        # Create a face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create a new window to display the faces
        cv2.namedWindow('Faces', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Faces', 400, 400)
        
        while True:
            # Read a frame from the video
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            
            # Iterate through the detected faces and display each face
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                cv2.imshow('Faces', face)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        # Release the video capture object
        cap.release()
        cv2.destroyAllWindows()

# Create a button to upload a video
upload_button = tk.Button(window, text="Upload Video", command=upload_video)
upload_button.pack()

# Run the Tkinter event loop
window.mainloop()