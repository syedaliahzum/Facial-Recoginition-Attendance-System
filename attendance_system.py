import face_recognition
import cv2
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


known_face_encodings = []
known_face_names = []


known_faces_dir = 'known_faces'
for filename in os.listdir(known_faces_dir):
    if filename.endswith('.jpg'):
        try:
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:  
                name = os.path.splitext(filename)[0]  
                for encoding in face_encodings:
                    known_face_encodings.append(encoding)  
                    known_face_names.append(name)  
        except Exception as e:
            print(f"Error loading {filename}: {e}")


attendance_list = []


root = tk.Tk()
root.title("Face Recognition Attendance System")


label_video = tk.Label(root)
label_video.pack()


log_text = tk.Text(root, height=10, width=50)
log_text.pack()


scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log_text.yview)


video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    messagebox.showerror("Error", "Could not open webcam.")
    root.quit()


def update_frame():
    ret, frame = video_capture.read()
    if not ret:
        messagebox.showerror("Error", "Failed to capture image.")
        return

    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(frame_rgb)

    
    if face_locations:
        face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):
            top, right, bottom, left = face_location
            name = "Unknown"
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                if name not in attendance_list:
                    attendance_list.append(name)
                    now = datetime.now()
                    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                    with open('attendance.csv', 'a') as f:
                        f.write(f"{name},{timestamp}\n")

                    
                    log_text.insert(tk.END, f"{name} - {timestamp}\n")
                    log_text.yview(tk.END)  

            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
    else:
        for face_location in face_locations:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    frame_image = Image.fromarray(frame_rgb)
    frame_image = ImageTk.PhotoImage(frame_image)

  
    label_video.config(image=frame_image)
    label_video.image = frame_image  

    
    label_video.after(10, update_frame)


update_frame()

root.mainloop()


video_capture.release()
cv2.destroyAllWindows()
