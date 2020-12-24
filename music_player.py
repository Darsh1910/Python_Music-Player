import os                       # to select the music mp3 files 
import pickle                   # Pickle is used to save values of List, Dictionary. 
import tkinter as tk            # to create the GUI/Graphical User Interface
from tkinter import filedialog  # to get access and open the file
from tkinter import PhotoImage  # to display the photo image 
from pygame import mixer        # to play/pause/volume up,down of the music

class Player(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		mixer.init()

		if os.path.exists('songs.pickle'):            ## songs are loaded in pickle list. If the song does not 
			                                          ## exists then it display empty list           
			with open('songs.pickle', 'rb') as f:                      
				self.playlist = pickle.load(f)                            
		else:
			self.playlist=[]

		self.current = 0           ### store the value of currently playing music 
		self.paused = True         ### no music is played when u open your application
		self.played = False        ### no music is played when u open your application

		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.tracklist_widgets()

	####################################################  There are 3 frames,main window, Track list, Play,pause,Volume buttuons 
	
	def create_frames(self):  
		self.track = tk.LabelFrame(self, text='Song Track', 
					font=("times new roman",15,"bold"),
					bg="grey",fg="white",bd=5,relief=tk.GROOVE)
		self.track.config(width=410,height=300)
		self.track.grid(row=0, column=0, padx=10)  ## Pad is the distance between frames 

		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
							font=("times new roman",15,"bold"),
							bg="grey",fg="white",bd=5,relief=tk.GROOVE)
		self.tracklist.config(width=190,height=400)
		self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

		self.controls = tk.LabelFrame(self,
							font=("times new roman",15,"bold"),
							bg="white",fg="white",bd=2,relief=tk.GROOVE)
		self.controls.config(width=410,height=80)
		self.controls.grid(row=2, column=0, pady=5, padx=10)

	def track_widgets(self):
		self.canvas = tk.Label(self.track, image=img)
		self.canvas.configure(width=400, height=240)
		self.canvas.grid(row=0,column=0)

		self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"),
						bg="white",fg="dark blue")
		self.songtrack['text'] = 'Music Player developed by Darsh Gupta'
		self.songtrack.config(width=30, height=1)
		self.songtrack.grid(row=1,column=0,padx=10)

	def control_widgets(self):
		self.loadSongs = tk.Button(self.controls, bg='green', fg='white', font=10)
		self.loadSongs['text'] = 'Load Songs'
		self.loadSongs['command'] = self.retrieve_songs ## binding func
		self.loadSongs.grid(row=0, column=0, padx=10)

		self.prev = tk.Button(self.controls, image=prev)
		self.prev['command'] = self.prev_song          ## binding func
		self.prev.grid(row=0, column=1)

		self.pause = tk.Button(self.controls, image=pause)
		self.pause['command'] = self.pause_song        ## binding func
		self.pause.grid(row=0, column=2)

		self.next = tk.Button(self.controls, image=next_)
		self.next['command'] = self.next_song          ## binding func
		self.next.grid(row=0, column=3)

		self.volume = tk.DoubleVar(self)                #creating a variable using tkinter
		self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL) ## slider from range1,10
		self.slider['variable'] = self.volume          
		self.slider.set(8)                               # initially setting the volume as 80 percent.
		mixer.music.set_volume(0.8)
		self.slider['command'] = self.change_volume
		self.slider.grid(row=0, column=4, padx=5)
    
	#################################################################### 5 function, tracklist,enumerate, retrieve, pause, prev, next, change volume
	
	
	def tracklist_widgets(self):                        ## Here there are 2 widgets in this frame
		                                                ## First is the list of songs and scroll bar. 	  
		self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL) # parent frame is Tracklist, orient = vertical. 
		self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')  # from stick with North, South and Vice versa. 

		##### LIST BOX
		
		self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
					 yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
		self.enumerate_songs()
		self.list.config(height=22)
		self.list.bind('<Double-1>', self.play_song) 

		self.scrollbar.config(command=self.list.yview)
		self.list.grid(row=0, column=0, rowspan=5)

	def retrieve_songs(self):
		self.songlist = []                          ### currently empty
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):  ## os.walk will give access to all files inside a directory 
				
				for file in files:                     ## to check the file is MP3. 
					if os.path.splitext(file)[1] == '.mp3': 
						path = (root_ + '/' + file).replace('\\','/')  ## Apeending the path of the mp3 file to songlist 
						self.songlist.append(path)

		with open('songs.pickle', 'wb') as f:   # wb = write binary    ## after running the program again it will load the previous songs, PICKLE
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'  ## displays at the top. number of songs in the playlist. 
		self.list.delete(0, tk.END)
		self.enumerate_songs()

	def enumerate_songs(self):                           #### it will show name of all the songs of the selected files.
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))


	def play_song(self, event=None):
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")

		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])
		self.songtrack['anchor'] = 'w' 
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])

		self.pause['image'] = play
		self.paused = False
		self.played = True
		self.list.activate(self.current) 
		self.list.itemconfigure(self.current, bg='sky blue')

		mixer.music.play()

	def pause_song(self):
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pause['image'] = pause
		else:
			if self.played == False:
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause['image'] = play

	def prev_song(self):
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current + 1, bg='white')
		self.play_song()

	def next_song(self):
		if self.current < len(self.playlist) - 1:
			self.current += 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current - 1, bg='white')
		self.play_song()

	def change_volume(self, event=None):
		self.v = self.volume.get()                   
		mixer.music.set_volume(self.v / 10)

# ---------------------------------------------------- MAIN -------------------------------------------------------------------

root = tk.Tk()  # this is to create a window for our music player
root.geometry('600x400') # configure the size of the window....(width x height)
root.wm_title('Music Player') # title of the window

img = PhotoImage(file='images/music.gif')              ##### Stored the images in variables 
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')

app = Player(master=root)
app.mainloop()