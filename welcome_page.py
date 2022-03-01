'''
TITLE: Tome To Read
AUTHOR: James Thomason
DESCRIPTION: So far this is the welcome page. Probably will integrate most things from this file into the main file. \
            However, this is just the skeleton for the main page that displays the Logo as well as a welcome.
            The welcome screen itself will have the functionality of being able to click anywhere on screen to switch
            over to the main screen. 

'''
from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import customtkinter

class tome_to_read(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (start_page,welcome_page, page_two, settings_page):
            frame = F(self.container,self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame(start_page)
    
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class start_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        img = ImageTk.PhotoImage(Image.open("start_page_background.jpg").resize((900,800)), Image.ANTIALIAS)
        labl = tk.Label(self, image=img)
        labl.img = img
        labl.place(relx=0.5, rely=0.5, anchor= CENTER)

        # main logo creation, implementation, placing into frame
        logo = Image.open("TomeToRead_Logo.png")
        logo = logo.resize((350,380))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.55, rely=.4, anchor= CENTER)
        # end of main logo creation, implementation, placing into frame

        instructions = Button(self, text="Click here to begin!", font=("Raleway", 32), command=lambda: controller.show_frame(welcome_page), borderwidth=0)
        instructions.place(relx=.55,rely=.95, anchor= S)
        

class upload_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        

class welcome_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        label = Label(self, text = "Start Page")
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self,text = "Go to Page 2", command=lambda: controller.show_frame(page_two))

        button1.pack()

        button2 = tk.Button(self,text= "Go to settings page!", command=lambda: controller.show_frame(settings_page))
        button2.pack()


class settings_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # Top portion of the settings page
        settings_header = Frame(self, width= 900, height=100, bg="white")
        settings_header.grid(columnspan=3,rowspan=2,row=0)
        settings_label = Label(settings_header, text = "Settings", font = ("Raleway", 32), fg="black", bg="white")
        settings_label.place(relx=.5,rely=.5,anchor=CENTER)
        # Placing button into the top section of settings page
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        
        
        back_arrow = customtkinter.CTkButton(
        settings_header,
        width=50,
        height=30,
        border_width=0,
        corner_radius=2,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(welcome_page)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)


class page_two(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        label = Label(self, text = "Page Two")
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self,text = "Back to welcome page", command=lambda: controller.show_frame(welcome_page))

        button1.pack()

def main():
    # Main window that pops up
    app = tome_to_read()
    app.title("Tome to Read")
    app.geometry("900x800")
    app.mainloop()
    

if __name__ == "__main__":
    main()