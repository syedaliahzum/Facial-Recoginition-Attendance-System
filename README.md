# Face Recognition Attendance System

A face recognition-based attendance system that logs attendance in a CSV file using webcam input. Built with **face_recognition**, **OpenCV**, and **Tkinter**.

## Features
- Real-time face recognition from webcam.
- Logs name and timestamp when a known face is detected.
- Simple GUI to display video feed with recognized faces.

## Requirements
- Python 3.x
- OpenCV
- face_recognition
- Tkinter
- Pillow
## Install dependencies:
pip install opencv-python face_recognition pillow

## How to Use:
Place images of known individuals in the known_faces/ folder (e.g., john_doe.jpg).
 ### Run the application:
- python face_recognition_attendance.py
- The system will log attendance with name and timestamp in attendance.csv.
  
## How it Works:
- Loads known face encodings from images in the known_faces/ folder.
- Captures webcam frames and detects faces.
- Logs name and timestamp in attendance.csv when a match is found.

