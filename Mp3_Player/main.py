from tkinter import *
import pygame

root = Tk()
root.title("Mp3 Player")
root.geometry("600x350")

# Initialize Pygame Mixer
pygame.mixer.init()

def AddSong():
    pass



# Create playlist box
songs_box = Listbox(root, bg="black", fg="green", width=60)
songs_box.pack(pady=20)

# Select images for the buttons
back_button_image = PhotoImage(file="Images/rewind_back.png")
forward_button_image = PhotoImage(file="Images/rewind_forward.png")
play_button_image = PhotoImage(file="Images/play.png")
pause_button_image = PhotoImage(file="Images/pause.png")
stop_button_image = PhotoImage(file="Images/stop.png")

# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()

# Create Buttons
back_button = Button(controls_frame, image=back_button_image, borderwidth=0)
forward_button = Button(controls_frame, image=forward_button_image, borderwidth=0)
play_button = Button(controls_frame, image=play_button_image, borderwidth=0)
pause_button = Button(controls_frame, image=pause_button_image, borderwidth=0)
stop_button = Button(controls_frame, image=stop_button_image, borderwidth=0)

back_button.grid(row=0, column=0)
forward_button.grid(row=0, column=1)
play_button.grid(row=0, column=2)
pause_button.grid(row=0, column=3)
stop_button.grid(row=0, column=4)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add A Song To The Playlist", command=AddSong)

root.mainloop()