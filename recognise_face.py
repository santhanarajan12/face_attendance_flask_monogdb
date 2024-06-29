import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import face_recognition
import cv2
import pickle

# Function to prepare image
def prepare_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# Function to compare test image with saved encoding
def compare_test_image(image, encoding):
    image = prepare_image(image)
    test_image_encoding = face_recognition.face_encodings(image)
    if len(test_image_encoding) == 1:
        result = face_recognition.compare_faces([test_image_encoding[0]], encoding, tolerance=0.6)
        return 1 if result[0] else 0
    elif len(test_image_encoding) == 0:
        return 2
    elif len(test_image_encoding) > 1:
        return 3

# Load training data
with open('train_data.pkl', 'rb') as f:
    train_data = pickle.load(f)

# Function to find and compare the number and face
def find_compare(number, image):
    for values in train_data:
        if values[1] == number:
            check_image = compare_test_image(image, values[4])
            if check_image == 0:
                return "Number and Face Don't Match, Please try again"
            elif check_image == 1:
                return "Your attendance marked " + str(values[0])
            elif check_image == 2:
                return "Cannot Find Face Properly, Please Try Again"
            elif check_image == 3:
                return "Multiple Faces Detected, Please try again"
    return "Registration number not found"

# Tkinter GUI
class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("800x600")

        # Label and entry for number input
        self.label = tk.Label(root, text="Enter your Number:")
        self.label.pack(pady=10)
        self.number_entry = tk.Entry(root)
        self.number_entry.pack(pady=10)

        # Button to start recognition
        self.start_button = tk.Button(root, text="Start Recognition", command=self.start_recognition)
        self.start_button.pack(pady=10)

        # Label to display results
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        # Camera feed display
        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)

        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)

        # Update the video feed
        self.update_video_feed()

    def update_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_video_feed)

    def start_recognition(self):
        number = self.number_entry.get()
        ret, frame = self.cap.read()
        if ret:
            result = find_compare(number, frame)
            self.result_label.config(text=result)
        else:
            messagebox.showerror("Error", "Failed to capture image from camera")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
