from tkinter import ttk
from tkinter import *
import time
from mutagen.mp3 import MP3
import os
import tkinter.messagebox
from tkinter import filedialog
import threading
from pygame import mixer
mixer.init() #initializing the mixer

root = Tk()

statusbar = ttk.Label(root, text="Welcome",relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root) #creating the menubar in the root window
root.config(menu=menubar,bg='grey')

submenu = Menu(menubar, tearoff=0) #submenu is inside Menubar

def browse_files():
        global filenames
        filenames = filedialog.askopenfilename()
        #print(filenames)
        addtolist(filenames)

Playlist = []

def addtolist(f):
        f = os.path.basename(f)
        index = 0
        playlistbox.insert(index,f)
        Playlist.insert(index,filenames)
        index+=1

menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open",command=browse_files)
submenu.add_command(label="Exit", command=root.destroy)

def aboutUs():
        tkinter.messagebox.showinfo("About Music Player","This Music Player has been developed as a project for the EE551 course in Fall 2019 by Neel Haria.")

submenu = Menu(menubar, tearoff=0) #submenu is inside Menubar
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About", command=aboutUs)


#root.geometry('300x400')
root.title("Music Player")
root.iconbitmap()

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=20)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length = --:--',relief=GROOVE)
lengthlabel.pack()

currentlabel = ttk.Label(topframe, text='Current Time = --:--',relief=GROOVE)
currentlabel.pack()

playlistbox = Listbox(leftframe)
playlistbox.pack()
addbtn = ttk.Button(leftframe, text="Add",command=browse_files)
addbtn.pack(side=LEFT)
def delSong():
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        playlistbox.delete(selected_song) #removing from the list box
        Playlist.remove(selected_song) #removing from array

delbtn =ttk.Button(leftframe, text="Remove",command=delSong)
delbtn.pack(side=LEFT)
#labelphoto= Label(root, image = photo)
#labelphoto.pack()

def showDetails(play_song):
        #filelabel['text'] = os.path.basename(filenames)
        data_file = os.path.splitext(play_song)
        #print(data_file)
        if data_file[1] == ".mp3":
                audio = MP3(play_song)
                totallength = audio.info.length
                print(totallength)
        else:
                a = mixer.Sound(play_song)
                totallength = a.get_length()

        mins, secs = divmod(totallength,60)
        mins = round(mins)
        secs = round(secs)
        format_time = '{:2d}:{:2d}.'.format(mins,secs)
        lengthlabel['text'] = "Total Length" + '-' + format_time

        t1 =threading.Thread(target=start_count, args=(totallength,))
        t1.start()
        #        print(format_time)
        #       start_count(length)

def start_count(t):
        while t and mixer.music.get_busy():
                if paused:
                        continue
                else:
                        mins, secs = divmod(t, 60)
                        mins = round(mins)
                        secs = round(secs)
                        format_time = '{:02d}:{:02d}'.format(mins, secs)
                        currentlabel['text'] = "Current Length" + '-' + format_time
                        time.sleep(1)
                        t -= 1


def playMusic():
        global paused
        if paused:
                mixer.music.unpause()
                statusbar['text'] = "Unpaused"
                paused = FALSE
        else:
                try:
                        stopMusic()
                        time.sleep(1)
                        selectedSong = playlistbox.curselection()
                        selectedSong = int(selectedSong[0])
                        playthissong = Playlist[selectedSong]
                        mixer.music.load(playthissong)
                        mixer.music.play()
                        statusbar['text'] = "Playing Now" + "-" + os.path.basename(playthissong)
                        showDetails(playthissong)
                except:
                        #pass
                        tkinter.messagebox.showerror("Warning!", "Please Select a song!")
                         #if initialized then it goes to Else conditions

def stopMusic():
        try:
                mixer.music.stop()
                statusbar['text'] = "Music Stopped"

                #try:
        except:
                tkinter.messagebox.showinfo("No File Selected.", "Select a New File!")
                       # browse_files()
                #except:
                       # print("Select a new song")

        #except:
         #       pass

paused = FALSE
def pauseMusic():
        global paused
        paused = True
        mixer.music.pause()
        statusbar['text'] = "Paused"

def rewindMusic():
        playMusic()
        statusbar['text'] = "Music Rewinded"

mute = FALSE
def muteMusic():
        global mute
        if mute:
                mixer.music.set_volume(0.11)
                volbtn.configure(image=volphoto)
                scale.set(11)
                mute = FALSE
        else:           #mute the music
                mixer.music.set_volume(0)
                volbtn.configure(image=mutephoto)
                scale.set(0)
                mute = TRUE

def setvol(val):
        volume = float(val)/100           #TypeCasting string into integer value
        mixer.music.set_volume(volume)  #set_volume takes Value from 0 to 1 only


middleframe = Frame(rightframe) #relief=RAISED, borderwidth=10)
middleframe.pack( padx=50,pady=50)

bottomframe = Frame(rightframe)
bottomframe.pack(padx=10)

scale = ttk.Scale(bottomframe,from_= 0,to_= 100,orient = HORIZONTAL, command=setvol )
scale.set(11)  #Setting the default value of the volume to a certain value, 25 here.
mixer.music.set_volume(0.11)
scale.grid(row=0,column=1,padx=10,pady=10)

rewindphoto = PhotoImage(file='back.png')
rewindbtn = ttk.Button(bottomframe, image=rewindphoto, command=rewindMusic)
rewindbtn.grid(row=0,column=0)

playphoto = PhotoImage(file='play.png')
playbtn = ttk.Button(middleframe, image=playphoto, command=playMusic)
playbtn.grid(row=0,column=1,padx=10)

stopphoto = PhotoImage(file='stop.png')
stopbtn =ttk.Button(middleframe, image=stopphoto, command=stopMusic)
stopbtn.grid(row=0,column=0,padx=10)

pausephoto = PhotoImage(file='icon.png')
pausebtn = ttk.Button(middleframe, image=pausephoto, command=pauseMusic)
pausebtn.grid(row=0,column=2,padx=10)

mutephoto = PhotoImage(file ='mute.png')
volphoto = PhotoImage(file='volume.png')
volbtn = ttk.Button(bottomframe, image=volphoto, command=muteMusic)
volbtn.grid(row=0,column=4)


def onClosing():
        stopMusic()
        root.destroy()

root.protocol("WM_DELETE_WINDOW",onClosing)
root.mainloop()
