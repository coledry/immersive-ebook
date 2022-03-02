'''
Author: Sarah Valine
Main Page: This opens up the main page and contains the buttons
that will lead to the various pages of the app. It also has the logo
and will play music in the background.

Has:
Buttons to go  to settings, library, and upload pages.
Logo
royalty free music lightly playing in background
'''

from tkinter import *
from tkinter import ttk
import pygame


sound = "bensound-theelevatorbossanova.mp3"
LARGEFONT =("Verdana", 35)

pygame.mixer.init() # initialise the pygame
pygame.mixer.music.load(sound) # loads the mp3 file
pygame.mixer.music.play(loops=3000) # continues playing it

def menu():
    '''
    This function opens up the main page and contains the buttons
    that will lead to the various pages of the app. It also has the logo
    and will play music in the background.

    has:
    Buttons to go  to settings, library, and upload pages.
    Logo
    royalty free music lightly playing in background
    '''

    
    top = Tk() # opens GUI window

    canvas = Canvas(bg="dark gray", width=595, height=770)
    canvas.place(relx=.5, rely=.5, anchor=CENTER)

    # creates the buttons and places them on the canvas
    au_button = Button(top, text = 'About Us') # button for About Us page
    au_button.place(x = 570, y = 578)

    lib_button = Button(top, text = 'Library')# button for Library page
    lib_button.place(x = 684, y = 578)

    upl_button = Button(top, text = 'Upload') # button for Upload page
    upl_button.place(x = 801, y = 578)

    set_button = Button(top, text = 'Settings') # buttons for Settings page
    set_button.place(x = 915, y = 578)

    logo = PhotoImage(file = 'tome.png') # inserts the logo
    logo_label = Label(image = logo) # names the logo
    logo_label.place(x = 625, y = 200) # places the logo on the canvas


    # keeps the GUI window open
    top.mainloop()

menu()
