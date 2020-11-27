from tkinter import *
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import tkinter.font as font
import pygame
import os
import time

root = Tk()
root.title("Mp3 Player")
root.geometry("1400x500")
root.resizable(False, False)

bg_color = "#0e0e0e"
fg_color = "#f63222"

my_font = font.Font(family='Consolas', size=10, weight="bold")

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

        if CheckIfSongExists(song):
            result = messagebox.askyesno("Dublication", fr"'{song}' already exists, do you want it to be added to ur playlist?")

            if not result:
                pass
        else:
            songs_box.insert(END, song)


def CheckIfSongExists(song):
    for i in range(songs_box.size()):
        if song == songs_box.get(i, last=None):
            return True

    return False

s_length = IntVar()
s_length.set(0)

s_name = StringVar()


# Play the selected song
def PlaySong(active_song=None):
    global stopped
    stopped = False

    try:
        if active_song is None:
            active_song = songs_box.get(ACTIVE)

        s_name.set(active_song)

        song_path = f"{songs_dirs[0]}/{active_song}.mp3"

        print(song_path)
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)
    except IndexError:
        messagebox.showinfo("Error", "Nothing there, please select a song!")
        return

    # Call PlayTime func to get the song time and len
    PlayTime()

    slider_start_label.config(text="00:00")
    slider_end_label.config(text="00:00")

    # Update slider
    slider_pos = int(song_len)
    my_slider.config(to=slider_pos, value=0)

    s_length.set(song_len)


# Create global stop var
global stopped
stopped = False


# Stop the song thats playing
def StopSong():
    time_bar.config(text='')
    my_slider.config(value=0)

    slider_start_label.config(text="00:00")
    slider_end_label.config(text="00:00")

    pygame.mixer.music.stop()
    songs_box.selection_clear(ACTIVE)

    # clear time bar
    time_bar.config(text='')

    global stopped
    stopped = True


# Create Global Pause var
global paused
paused = False


# Pause and Unpause the current song
def PauseSong(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause the song
        pygame.mixer.music.unpause()
        pause_button.config(image=pause_button_image)
        paused = False
    else:
        # pause the song
        pygame.mixer.music.pause()
        pause_button.config(image=paused_on_button_image)
        paused = True


# Play the next song
def NextSong():
    slider_start_label.config(text="00:00")
    slider_end_label.config(text="00:00")

    time_bar.config(text='')
    my_slider.config(value=0)

    try:
        # current song - returns number
        next_s = songs_box.curselection()
        # add one to the current song
        next_s = next_s[0] + 1

        # Get the song
        song = songs_box.get(next_s)

        # clear the bar
        songs_box.selection_clear(0, END)

        # set the bar to the next song
        songs_box.activate(next_s)

        # set active bar
        songs_box.selection_set(next_s, last=None)

        # StopSong()
        PlaySong(song)

        # get the actual dir
        # song_path = f"{songs_dirs[0]}/{song}.mp3"

        # load and play the song
        # pygame.mixer.music.load(song_path)
        # pygame.mixer.music.play(loops=0)
    except pygame.error:
        StopSong()
        return


# Get the previous song
def PreviousSong():
    s_length.set(song_len)
    slider_start_label.config(text="00:00")
    slider_end_label.config(text="00:00")

    time_bar.config(text='')
    my_slider.config(value=0)

    try:
        # current song - returns number
        n = songs_box.curselection()
        # subtracting one to the current song
        previous = n[0] - 1

        # Get the song
        song = songs_box.get(previous)

        # clear the bar
        songs_box.selection_clear(0, END)

        # set the bar to the next song
        songs_box.activate(previous)

        # set active bar
        songs_box.selection_set(previous, last=None)

        PlaySong(song)

        # get the actual dir
        # song_path = f"{songs_dirs[0]}/{song}.mp3"

        # load and play the song
        # pygame.mixer.music.load(song_path)
        # pygame.mixer.music.play(loops=0)
    except IndexError:
        messagebox.showinfo("Error", "Nothing there, please select a song!")
        return


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
    StopSong()


# Delete all songs
def DeleteAllSongs():
    # delete all songs
    songs_box.delete(0, END)
    # stop if something is playing
    StopSong()


# Create slider function
def Slide(x):
    try:
        song = songs_box.get(ACTIVE)
        song = f"{songs_dirs[0]}/{song}.mp3"

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    except NameError:
        messagebox.showinfo("No Song Selected", "Please choose a song!")


# Create volume func
def VolumeSlider(x):
    pygame.mixer.music.set_volume(volume_slider.get())

    if volume_slider.get() > 0:
        volume_button.config(image=volume_image)


def Mute():
    volume_slider.config(value=0)
    pygame.mixer.music.set_volume(0)
    volume_button.config(image=muted_image)


global replayed
replayed = False


def ReplayCurrentSong(is_replayed):
    global replayed
    replayed = is_replayed

    if replayed:
        # print("Don't Replay")
        replay_button.config(image=replay_button_image)
        replayed = False
    else:
        # print("Replay")
        replay_button.config(image=replay_button_on_image)
        replayed = True


# Get song length and time info
def PlayTime():
    # making sure there isn't double timing
    if stopped:
        return

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

    current_playing_song = f"{s_name.get()}"
    video_title_label.config(text=f"{current_playing_song}")

    # get song len with mutagen
    global song_len
    song_len = song_mut.info.length

    # Convert to time format
    convert_song_len = time.strftime('%M:%S', time.gmtime(song_len))

    # icrease current time by 1 sec
    current_time += 1

    if int(my_slider.get()) >= int(song_len):
        # Convert to time format
        convert_current_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))

        if replayed:
            my_slider.config(value=0)
            PlaySong()
        else:
            NextSong()

        # time_bar.config(text=f"Time Elapsed: {convert_current_time} of {convert_song_len}")
    elif paused:
        # pause_play_button.config(image=play_button_image, command=lambda: PauseSong(paused))
        pass
    elif int(my_slider.get()) == int(current_time):
        # Update slider
        slider_pos = int(song_len)
        my_slider.config(to=slider_pos, value=int(current_time))
    else:
        # Update slider
        slider_pos = int(song_len)
        my_slider.config(to=slider_pos, value=int(my_slider.get()))

        # convert to time format
        convert_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # move the slider along bt a sec
        new_time = int(my_slider.get()) + 1
        my_slider.config(value=new_time)

    convert_s_length = time.strftime('%M:%S', time.gmtime(s_length.get()))

    slider_start_label.config(text=f"{convert_current_time}")
    slider_end_label.config(text=f"{convert_s_length}")

    # update time
    time_bar.after(1000, PlayTime)


master_frame = Frame(root)
master_frame.pack()

# Create playlist box
songs_box = Listbox(master_frame, bg=bg_color, fg=fg_color, font=my_font, justify=CENTER, width=198, height=20,
                    selectbackground="gray",
                    selectforeground=bg_color)
songs_box.grid(row=0, column=0, columnspan=10, pady=10)

# Select images for the buttons
delete_button_image = PhotoImage(file="Images/trash_bin.png")
add_button_image = PhotoImage(file="Images/add.png")
back_button_image = PhotoImage(file="Images/rewind_back.png")
stop_button_image = PhotoImage(file="Images/stop.png")
play_button_image = PhotoImage(file="Images/play.png")

pause_button_image = PhotoImage(file="Images/pause.png")
paused_on_button_image = PhotoImage(file="Images/paused_on.png")

forward_button_image = PhotoImage(file="Images/rewind_forward.png")

replay_button_image = PhotoImage(file="Images/replay.png")
replay_button_on_image = PhotoImage(file="Images/replay_on.png")

volume_image = PhotoImage(file="Images/volume.png")
muted_image = PhotoImage(file="Images/muted.png")

music_image = PhotoImage(file="Images/note.png")

# Create Player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=5)

# Create start slider label
slider_start_label = Label(master_frame, text="00:00", font=my_font)
slider_start_label.grid(row=2, column=4, pady=10, sticky=E)

# Create end slider label
slider_end_label = Label(master_frame, text="00:00", font=my_font)
slider_end_label.grid(row=2, column=6, pady=10, sticky=W)

# Create Buttons
add_button = Button(controls_frame, image=add_button_image, command=AddSong, borderwidth=0)
back_button = Button(controls_frame, image=back_button_image, command=PreviousSong, borderwidth=0)

play_button = Button(controls_frame, image=play_button_image, command=PlaySong, borderwidth=0)
pause_button = Button(controls_frame, image=pause_button_image, command=lambda: PauseSong(paused), borderwidth=0)
stop_button = Button(controls_frame, image=stop_button_image, command=StopSong, borderwidth=0)

forward_button = Button(controls_frame, image=forward_button_image, command=NextSong, borderwidth=0)
delete_button = Button(controls_frame, image=delete_button_image, command=DeleteSong, borderwidth=0)
replay_button = Button(controls_frame, image=replay_button_image, command=lambda: ReplayCurrentSong(replayed),
                       borderwidth=0)

volume_button = Button(master_frame, image=volume_image, command=Mute, borderwidth=0)

# Set buttons positions
add_button.grid(row=0, column=0, padx=5)
back_button.grid(row=0, column=1, padx=5)

play_button.grid(row=0, column=2, padx=5)
pause_button.grid(row=0, column=3, padx=5)
stop_button.grid(row=0, column=4, padx=5)

forward_button.grid(row=0, column=5, ipadx=5)
delete_button.grid(row=0, column=6, padx=5)
replay_button.grid(row=0, column=7, padx=5)

volume_button.grid(row=1, column=8, rowspan=2, padx=20, sticky=E)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove All Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Clear Every Song From The Playlist", command=DeleteAllSongs)

# Create time bar
time_bar = Label(root, text='', bd=0, relief=GROOVE, anchor=E)
time_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create a music pos slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=Slide, length=360)
my_slider.grid(row=2, column=5, pady=10)

# Create volume slider
volume_slider = ttk.Scale(master_frame, from_=0, to=1, orient=HORIZONTAL, value=.2, command=VolumeSlider, length=130)
volume_slider.grid(row=1, column=9, rowspan=2, padx=10, pady=10, sticky=W)

# Create video title label
video_title_label = Label(master_frame, text="Title", font=my_font)
video_title_label.grid(row=3, column=5, rowspan=2)

# Load an image for the album cover of the song if such exists
note_image_label = Label(master_frame, image=music_image)
note_image_label.grid(row=1, column=0, rowspan=2)

root.mainloop()
