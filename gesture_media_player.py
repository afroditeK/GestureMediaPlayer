import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import pygame
import os
import math
import numpy as np

class GestureMediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Media Player")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        self.song_list = []
        self.current_song_index = 0
        self.is_playing = False
        self.volume = 0.5
        self.current_music_type = "None"

        pygame.mixer.init()

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        # self.mp_draw = mp.solutions.drawing_utils

        # Set media root folder
        self.media_root_folder = os.path.join(os.getcwd(), "media")

        # Main frames: Left control panel and Right webcam display
        self.left_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        self.left_frame.place(x=20, y=20, width=340, height=660)

        self.right_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        self.right_frame.place(x=380, y=20, width=500, height=660)

        # Left frame contents
        self.load_button = tk.Button(self.left_frame, text="Load Songs Manually", command=self.load_songs_manual,
                                     bg="#6c63ff", fg="black", font=("Segoe UI", 14, "bold"),
                                     bd=0, padx=10, pady=10, cursor="hand2", activebackground="#5848c2")
        self.load_button.pack(pady=(20, 10), fill="x", padx=20)

        self.song_label = tk.Label(self.left_frame, text="No song loaded", fg="#222",
                                   font=("Segoe UI", 12, "bold"), bg="#ffffff")
        self.song_label.pack(pady=(0, 15), padx=20, anchor="w")

        self.volume_label = tk.Label(self.left_frame, text="Volume: 50%", fg="#444",
                                     font=("Segoe UI", 12), bg="#ffffff")
        self.volume_label.pack(pady=(0, 15), padx=20, anchor="w")

        self.instructions_label = tk.Label(
            self.left_frame,
            text=(
                "Instructions:\n"
                "• Left hand open = Play\n"
                "• Left hand fist = Pause\n"
                "• Right hand thumb-index distance = Volume\n"
            ),
            font=("Segoe UI", 11), bg="#ffffff", fg="#555", justify="left"
        )
        self.instructions_label.pack(padx=20, pady=(0, 25), anchor="w")

        music_type_title = tk.Label(self.left_frame, text="Choose Music Type", font=("Segoe UI", 14, "bold"),
                                    bg="#ffffff", fg="#6c63ff")
        music_type_title.pack(pady=(0, 10), padx=20, anchor="w")

        self.music_types = ["Pop", "Jazz", "Electronic"]
        self.music_type_buttons = []

        btn_frame = tk.Frame(self.left_frame, bg="#ffffff")
        btn_frame.pack(padx=20, fill="x")

        for mt in self.music_types:
            btn = tk.Button(btn_frame, text=mt, bg="#d9d2e9", fg="#3b2e94",
                            font=("Segoe UI", 12, "bold"), bd=0, pady=8,
                            cursor="hand2", activebackground="#b4a7d6",
                            command=lambda mt=mt: self.load_songs_for_type(mt))
            btn.pack(fill="x", pady=5)
            self.music_type_buttons.append(btn)

        self.current_music_type_label = tk.Label(self.left_frame, text="Current Music Type: None",
                                                 font=("Segoe UI", 13), bg="#ffffff", fg="#333")
        self.current_music_type_label.pack(pady=(30, 0), padx=20, anchor="w")

        # Previous and Next buttons
        nav_btn_frame = tk.Frame(self.left_frame, bg="#ffffff")
        nav_btn_frame.pack(pady=20, padx=20, fill="x")

        self.prev_button = tk.Button(nav_btn_frame, text="⏮ Previous", command=self.prev_song,
                                     bg="#6c63ff", fg="black", font=("Segoe UI", 12, "bold"),
                                     bd=0, padx=10, pady=8, cursor="hand2", activebackground="#5848c2")
        self.prev_button.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.next_button = tk.Button(nav_btn_frame, text="Next ⏭", command=self.next_song,
                                     bg="#6c63ff", fg="black", font=("Segoe UI", 12, "bold"),
                                     bd=0, padx=10, pady=8, cursor="hand2", activebackground="#5848c2")
        self.next_button.pack(side="left", expand=True, fill="x", padx=(10, 0))

        # Right frame contents - Webcam feed
        self.canvas = tk.Label(self.right_frame, bg="black")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.cap = cv2.VideoCapture(0)
        self.root.after(10, self.update_frame)

    def load_songs_manual(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            songs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".mp3")]
            if songs:
                self.song_list = songs
                self.current_song_index = 0
                self.play_song(self.song_list[self.current_song_index])
                self.current_music_type = "Manual"
                self.current_music_type_label.config(text="Current Music Type: Manual")
            else:
                messagebox.showinfo("No songs found", "No .mp3 files found in the selected folder.")

    def load_songs_for_type(self, music_type):
        folder = os.path.join(self.media_root_folder, music_type)
        if not os.path.exists(folder):
            messagebox.showerror("Folder not found",
                                 f"The folder for {music_type} music does not exist:\n{folder}")
            return

        songs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".mp3")]
        if songs:
            self.song_list = songs
            self.current_song_index = 0
            self.play_song(self.song_list[self.current_song_index])
            self.current_music_type = music_type
            self.current_music_type_label.config(text=f"Current Music Type: {music_type}")
        else:
            messagebox.showinfo("No songs found", f"No .mp3 files found in the {music_type} folder.")

    def play_song(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.is_playing = True
        self.song_label.config(text=f"▶ Now Playing: {os.path.basename(path)}")

    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.song_label.config(text=f"⏸ Paused: {os.path.basename(self.song_list[self.current_song_index])}")

    # def unpause_song(self):
    #     if not self.is_playing:
    #         pygame.mixer.music.unpause()
    #         self.is_playing = True
    #         self.song_label.config(text=f"▶ Now Playing: {os.path.basename(self.song_list[self.current_song_index])}")

    def unpause_song(self):
        if not self.is_playing:
            if not self.song_list:
                messagebox.showwarning("No songs loaded", "No songs are loaded to play!")
                return
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.song_label.config(text=f"▶ Now Playing: {os.path.basename(self.song_list[self.current_song_index])}")

    def prev_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
            self.play_song(self.song_list[self.current_song_index])

    def next_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.play_song(self.song_list[self.current_song_index])

    def count_fingers(self, landmarks):
        tips_ids = [4, 8, 12, 16, 20]
        fingers = []

        #checks if the thumb is up
        fingers.append(1 if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x else 0)
        #checks if the other fingers are open or close
        for id in range(1, 5):
            fingers.append(1 if landmarks[tips_ids[id]].y < landmarks[tips_ids[id] - 2].y else 0)
        #counts how many 1's are in the list
        return fingers.count(1)

    def calc_thumb_index_distance(self, landmarks, w, h):
        # Calculate distance between thumb tip and index finger tip
        x1, y1 = int(landmarks[4].x * w), int(landmarks[4].y * h)
        x2, y2 = int(landmarks[8].x * w), int(landmarks[8].y * h)
        return math.hypot(x2 - x1, y2 - y1)

    def update_frame(self):
        #check if webcam is open
        if not self.cap.isOpened():
            self.root.after(10, self.update_frame)
            return

        #read a video frame
        ret, frame = self.cap.read()
        if not ret:
            self.root.after(10, self.update_frame)
            return

        #Flip the frame horizontally so movements appear natural like a mirror
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb) #info about detected hands and their landmarks

        h, w, _ = frame.shape
        left_hand = None
        right_hand = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                label = results.multi_handedness[i].classification[0].label
                if label == "Left":
                    left_hand = hand_landmarks
                elif label == "Right":
                    right_hand = hand_landmarks
                    
         # ----- Check if current song ended and move to next -----
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.next_song()

        # ----- Gesture detection -----
        # Left hand: open hand or fist for play/pause
        if left_hand:
            left_fingers = self.count_fingers(left_hand.landmark)
            # Open hand (4 or 5 fingers) = Play
            if left_fingers >= 4 and not self.is_playing:
                self.unpause_song()
            # Fist (0 or 1 finger) = Pause
            elif left_fingers <= 1 and self.is_playing:
                self.pause_song()

        # Right hand: volume control by thumb-index finger distance
        if right_hand:
            dist = self.calc_thumb_index_distance(right_hand.landmark, w, h)
            # Normalize dist to volume range (approx 20 to 150 pixels)
            vol = np.clip((dist - 20) / (150 - 20), 0, 1) #makes sure the volume vol never goes below 0 or above 1
            self.volume = vol
            pygame.mixer.music.set_volume(self.volume)
            self.volume_label.config(text=f"Volume: {int(self.volume * 100)}%")

        #converts OpenCV images into a format that Tkinter can display inside the app window (with PIL)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.config(image=imgtk)

        self.root.after(10, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureMediaPlayer(root)
    root.mainloop()
class GestureMediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Media Player")