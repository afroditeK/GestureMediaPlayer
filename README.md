# Gesture Media Player

A Python application that allows you to control music playback using **hand gestures**.  
Built with **Tkinter**, **OpenCV**, **MediaPipe**, and **Pygame**.

## Features

- Play / Pause with left-hand gestures
- Volume control with right-hand thumb-index finger distance
- Load songs manually or choose from predefined music types (Pop, Jazz, Electronic)
- Next / Previous song navigation
- Simple GUI with instructions and music type selection

## Folder Structure
```
GestureMediaPlayer/
├── main.py
├── media/
│ ├── Pop/ # Put your Pop mp3 files here
│ ├── Jazz/ # Put your Jazz mp3 files here
│ └── Electronic/# Put your Electronic mp3 files here
└── .gitignore
```
**Note:** For the music type selection to work, you must organize your mp3 files in the appropriate subfolders under `media/` as shown above.


## How to Run

1. **Make sure you have Python 3.7 or higher.**  
   - If `python` does not point to Python 3, use `python3`.

2. Install the required libraries:
```bash
pip install opencv-python mediapipe pygame pillow numpy
```

3. Run the app
```bash
python gesture_media_player.py #or python3 
```
