from tkinter import *
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import pygame
import os
import time

root = Tk()
root.title("Mp3 Player")
root.geometry("500x350")
# root.resizable(False, False)

# Initialize Pygame Mixer
pygame.mixer.init()

songs_dirs = []


# Add  song function
def AddSong():
    songs = filedialog.askopenfilenames(initialdir="Audio/",
                                        title="Choose a song",
                                        filetypes=(("MP3 Files", "*.mp3"),))

    for song in songs:
        songs_dirs.append(os.path.split(song)[0])

        song = os.path.split(song)[1].replace(".mp3", "")
        songs_box.insert(END, song)


# Play the selected song
def PlaySong():
    song = songs_box.get(ACTIVE)
    song_path = f"{songs_dirs[0]}/{song}.mp3"

    print(song_path)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)

    # Call PlayTime func to get the song time and len
    PlayTime()

    # Update slider
    slider_pos = int(song_len)
    my_slider.config(to=slider_pos, value=0)


# Stop the song thats playing
def StopSong():
    pygame.mixer.music.stop()
    songs_box.selection_clear(ACTIVE)

    # clear time bar
    time_bar.config(text='')

# Create Global Pause var
global paused
paused = False


# Pause and Unpause the current song
def PauseSong(is_paused):
    global paused
    paused = is_paused

    if not paused:
        # pause the song
        pygame.mixer.music.pause()
        paused = False
    else:
        # unpause the song
        pygame.mixer.music.unpause()
        paused = True


# Play the next song
def NextSong():
    # current song - returns number
    next_s = songs_box.curselection()
    # add one to the current song
    next_s = next_s[0] + 1

    # Get the song
    song = songs_box.get(next_s)
    # get the actual dir
    song_path = f"{songs_dirs[0]}/{song}.mp3"

    # load and play the song
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)

    # clear the bar
    songs_box.selection_clear(0, END)

    # set the bar to the next song
    songs_box.activate(next_s)

    # set active bar
    songs_box.selection_set(next_s, last=None)


# Get the previous song
def PreviousSong():
    # current song - returns number
    n = songs_box.curselection()
    # subtracting one to the current song
    previous = n[0] - 1

    # Get the song
    song = songs_box.get(previous)
    # get the actual dir
    song_path = f"{songs_dirs[0]}/{song}.mp3"

    # load and play the song
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)

    # clear the bar
    songs_box.selection_clear(0, END)

    # set the bar to the next song
    songs_box.activate(previous)

    # set active bar
    songs_box.selection_set(previous, last=None)


# Delete a song
def DeleteSong():
    try:
        # current song - returns number
        n = songs_box.curselection()

        # getting the next song to delete
        num = n[0]
    except IndexError:
        messagebox.showinfo("Error", "Please select a song!")
        return

    print(n, num)

    # Delete the selected song
    songs_box.delete(ANCHOR)

    # set the bar to the next song
    songs_box.activate(num)

    # set active bar
    songs_box.selection_set(num, last=None)

    # stop if its playing
    pygame.mixer.music.stop()


# Delete all songs
def DeleteAllSongs():
    # delete all songs
    songs_box.delete(0, END)
    # stop if something is playing
    pygame.mixer.music.stop()


# Create slider function
def Slide(x):
    try:
        slider_label.config(text=f"{int(my_slider.get())} of {int(song_len)}")
    except NameError:
        messagebox.showinfo("No Song Selected", "Please choose a song!")


# Get song length and time info
def PlayTime():
    # Current time
    current_time = pygame.mixer.music.get_pos() / 1000

    # Convert to time format
    convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Get the song
    song = songs_box.get(ACTIVE)
    # get the actual dir
    song = f"{songs_dirs[0]}/{song}.mp3"
    # load song with mutagen
    song_mut = MP3(song)

    # get song len with mutagen
    global song_len
    song_len = song_mut.info.length

    # Convert to time format
    convert_song_len = time.strftime('%M:%S', time.gmtime(song_len))

    # Output time to status bar
    time_bar.config(text=f"Time Elapsed: {convert_current_time} of {convert_song_len}")
    slider_label.config(text=f"{int(my_slider.get())} of {int(song_len)}")

    # Update slider pos value to the curent songs value
    my_slider.config(value=int(current_time))

    # update time
    time_bar.after(1000, PlayTime)

# Create playlist box
songs_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
songs_box.pack(pady=20)

# Select images for the buttons
delete_button_image = PhotoImage(file="Images/trash_bin.png")
add_button_image = PhotoImage(file="Images/add.png")
back_button_image = PhotoImage(file="Images/rewind_back.png")
stop_button_image = PhotoImage(file="Images/stop.png")
play_button_image = PhotoImage(file="Images/play.png")
pause_button_image = PhotoImage(file="Images/pause.png")
forward_button_image = PhotoImage(file="Images/rewind_forward.png")

# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()

# Create Buttons
delete_button = Button(controls_frame, image=delete_button_image, command=DeleteSong, borderwidth=0)
add_button = Button(controls_frame, image=add_button_image, command=AddSong, borderwidth=0)
back_button = Button(controls_frame, image=back_button_image, command=PreviousSong, borderwidth=0)
stop_button = Button(controls_frame, image=stop_button_image, command=StopSong, borderwidth=0)
play_button = Button(controls_frame, image=play_button_image, command=PlaySong, borderwidth=0)
pause_button = Button(controls_frame, image=pause_button_image, command=lambda: PauseSong(paused), borderwidth=0)
forward_button = Button(controls_frame, image=forward_button_image, command=NextSong, borderwidth=0)

delete_button.grid(row=0, column=0, padx=5)
add_button.grid(row=0, column=1, padx=5)
back_button.grid(row=0, column=2, padx=5)
stop_button.grid(row=0, column=3, padx=5)
play_button.grid(row=0, column=4, padx=5)
pause_button.grid(row=0, column=5, padx=5)
forward_button.grid(row=0, column=6, padx=5)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove All Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Clear Every Song From The Playlist", command=DeleteAllSongs)

# Create time bar
time_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
time_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create a music pos slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=Slide, length=360)
my_slider.pack(pady=20)

# Create slider label
slider_label = Label(root, text="0")
slider_label.pack(pady=10)

root.mainloop()
