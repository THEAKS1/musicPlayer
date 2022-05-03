import os, pickle
from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

class Player(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        mixer.init()

        if os.path.exists("songs.pickle"):
            with open("songs.pickle", "rb") as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

    def create_frames(self):
        self.track = LabelFrame(self, text = "Song Track", font = ("times new roman", 15, "bold"), bg = "grey", fg = "white", bd = 5, relief = GROOVE)
        self.track.configure(width = 410, height = 300)
        self.track.grid(row = 0, column = 0, padx = 10)

        self.tracklist = LabelFrame(self, text = f"Playlist - {len(self.playlist)}", font = ("times new roman", 15, "bold"), bg = "grey", fg = "white", bd = 5, relief = GROOVE)
        self.tracklist.configure(width = 190, height = 400)
        self.tracklist.grid(row = 0, column = 1, rowspan = 3, pady = 5)

        self.controls = LabelFrame(self, font = ("times new roman", 15, "bold"), bg = "white", fg = "white", bd = 5, relief = GROOVE)
        self.controls.configure(width = 410, height = 80)
        self.controls.grid(row = 2, column = 0, pady = 5, padx = 10)

    def track_widgets(self):
        self.canvas = Label(self.track, image = img)
        self.canvas.configure(width = 400, height = 240)
        self.canvas.grid(row = 0, column = 0)

        self.songtrack = Label(self.track, font = ("times new roman", 15, "bold"), bg = "white", fg = "dark blue")
        self.songtrack["text"] = "PROTOTYPE_player"
        self.songtrack.configure(width = 30, height = 1)
        self.songtrack.grid(row = 1, column = 0)

    def control_widgets(self):
        self.loadSongs = Button(self.controls, bg = "green", fg = "white", font = 10, text = "Load Songs", command = self.retrive_songs)
        self.loadSongs.grid(row = 0, column = 0, padx = 10)

        self.prev = Button(self.controls, image = prev, command = self.prev_song)
        self.prev.grid(row = 0, column = 1)

        self.pause = Button(self.controls, image = pause, command = self.pause_song)
        self.pause.grid(row = 0, column = 2)

        self.next = Button(self.controls, image = next_, command = self.next_song)
        self.next.grid(row = 0, column = 3)

        self.volume = DoubleVar()
        self.slider = Scale(self.controls, from_ = 0, to = 10, orient = HORIZONTAL, variable = self.volume, command = self.change_volume)
        self.slider.grid(row = 0, column = 4, padx = 5)
        self.slider.set(8)
        mixer.music.set_volume(0.8)


    def tracklist_widgets(self):
        self.scrollbar = Scrollbar(self.tracklist, orient = VERTICAL)
        self.scrollbar.grid(row = 0, column = 1, rowspan = 5, sticky = "ns")

        self.list = Listbox(self.tracklist, selectmode = SINGLE, yscroll = self.scrollbar.set, selectbackground = "grey", selectforeground = "black")
        self.list.config(height = 22)

        self.enumerate_songs()

        self.list.bind("<Double-1>", self.play_songs)

        self.scrollbar.config(command = self.list.yview)
        self.list.grid(row = 0, column = 0, rowspan = 5)

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def retrive_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root_ + "/" + file).replace("\\", "/")
                    self.songlist.append(path)
        
        with open("songs.pickle", "wb") as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.tracklist["text"] = f"Playlist - {str(len(self.playlist))}"
        self.list.delete(0, END)
        self.enumerate_songs()

    def play_songs(self, event = None):
        if event is not None:
            self.current = self.list.curselection()[0]

        mixer.music.load(self.playlist[self.current])
        self.pause["image"] = play
        self.paused = False
        self.played = True
        self.songtrack["anchor"] = "w"
        self.songtrack["text"] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg = "sky blue")
        mixer.music.play()

    def prev_song(self):
        self.list.itemconfigure(self.current, bg = "white")
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.play_songs()

    def next_song(self):
        self.list.itemconfigure(self.current, bg = "white")
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.play_songs()

    def change_volume(self, event = None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause["image"] = pause
        else:
            if self.played == False:
                self.play_songs()
            self.paused = False
            mixer.music.unpause()
            self.pause["image"] = play

root = Tk()
root.geometry("700x450")
root.title("PROTOTYPE_Player")

img = PhotoImage(file = "music.gif")
next_ = PhotoImage(file = "icons/next.png")
prev = PhotoImage(file = "icons/back.png")
play = PhotoImage(file = "icons/play.png")
pause = PhotoImage(file = "icons/pause.png")

app = Player(master = root)
app.mainloop()