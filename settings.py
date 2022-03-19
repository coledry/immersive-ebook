'''
Author: Cole Dryer
Settings Page
'''
from tkinter import *

#creates tkinter window, title, icon and canvas:
window = Tk()
window.title("Tome to Read")
window.iconphoto(TRUE, PhotoImage(file = "tome.png"))
canvas = Canvas(bg="dark gray", width=595, height=770)
canvas.place(relx=.5, rely=.5, anchor=CENTER)

#Button Functions:
def back_fn(): #send the user back to their previous page (home/e-reader)
    print("back button pressed")
def switch_fn(): #switches from light to dark mode (switch_btn function)
    print("button pressed")
def slider1_fn(): #adjusts volume by percentage (slider1 function)
    print("button pressed")
def slider2_fn(): #adjusts volume by percentage (slider2 function)
    print("button pressed")
def ddstyle_fn(): #changes font style to user preference (dropdown btn1 function)
    print("button pressed")
def ddsize_fn(): #changes font size to user preference (IF DOABLE, dropdown btn2 function)
    print("button pressed")


#just using one 'settings' function for now:
def settings(): 
    #creates header section:
    settings_header = Frame(window, width= 585, height=70, bg="white")
    settings_header.grid(columnspan=3,rowspan=2,row=0)
    settings_header.place(x=768,y=97, anchor=N)
    settings_label = Label(settings_header, text = "Settings", font = ("Raleway", 32), fg="black", bg="white")
    settings_label.place(relx=.5, rely=.5,anchor=CENTER)
    #back button:
    back_btn = Button(window, text = "< Back", command=back_fn, bd=0, bg="dark gray")
    back_btn.place(x = 500, y = 118)
    
    #creates section 1 frame:
    sec1 = Frame(width= 585, height=225, bg="white")
    sec1.grid(columnspan=3,rowspan=2,row=0)
    sec1.place(x=768,y=172, anchor=N)
    #label(s):
    interface_lbl = Label(sec1, text="Interface Settings:", font = ("Raleway", 14), fg="black", bg="white")
    interface_lbl.place(relx=.5, rely=.1,anchor=CENTER)
    if_style_lbl = Label(sec1, text="Interface Style:", font = ("Raleway", 12), fg="black", bg="white")
    if_style_lbl.place(relx=.45, rely=.5,anchor=CENTER)
    #switch button(light mode/dark mode):

    #creates section 2 frame:
    sec2 = Frame(width= 585, height=225, bg="white")
    sec2.grid(columnspan=3,rowspan=2,row=0)
    sec2.place(x=768,y=402, anchor=N)
    #label(s):
    volume_lbl = Label(sec2, text="Volume Settings:", font = ("Raleway", 14), fg="black", bg="white")
    volume_lbl.place(relx=.5, rely=.1,anchor=CENTER)
    music_lbl = Label(sec2, text="Music:", font = ("Raleway", 12), fg="black", bg="white")
    music_lbl.place(relx=.23, rely=.4,anchor=CENTER)
    soundfx_lbl = Label(sec2, text="Sound FX:", font = ("Raleway", 12), fg="black", bg="white")
    soundfx_lbl.place(relx=.2, rely=.6,anchor=CENTER)
    #button sliders:

    #creates section 3 frame:
    sec3 = Frame(width= 585, height=225, bg="white")
    sec3.grid(columnspan=3,rowspan=2,row=0)
    sec3.place(x=768,y=632, anchor=N)
    #label(s):
    font_lbl = Label(sec3, text="Font Settings:", font = ("Raleway", 14), fg="black", bg="white")
    font_lbl.place(relx=.5, rely=.1,anchor=CENTER)
    fstyle_lbl = Label(sec3, text="Font Style:", font = ("Raleway", 12), fg="black", bg="white")
    fstyle_lbl.place(relx=.35, rely=.4,anchor=CENTER)
    fsize_lbl = Label(sec3, text="Font Size:", font = ("Raleway", 12), fg="black", bg="white")
    fsize_lbl.place(relx=.35, rely=.6,anchor=CENTER)
    #dropdown menus(font size/font style):
    
    window.mainloop()

settings()
