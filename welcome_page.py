'''
TITLE: Tome To Read
AUTHORS: James Thomason, Colby Chambers, Sarah Valine, and Cole Dryer
DESCRIPTION: So far this is the welcome page. Probably will integrate most things from this file into the main file. \
            However, this is just the skeleton for the main page that displays the Logo as well as a welcome.
            The welcome screen itself will have the functionality of being able to click anywhere on screen to switch
            over to the main screen. 
'''


from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfile
from turtle import left
from PIL import Image, ImageTk
import customtkinter
import pandas as pd
import requests
import pygame
import os
import os.path

pygame.mixer.init()

url='https://raw.githubusercontent.com/colbychambers25/immersive-ebook/main/Domain_Free_eBook.csv'
book_library = pd.read_csv(url) #print to see what the panda looks like
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/Sound_audio_map.csv'
audio_map = pd.read_csv(url)
prev_song = ['none']
library_map = {}


class story_file:
    '''
    This will have be a more unique class compared to sounds_file and music_file due to the fact that we're planning to 
    let the user assign songs to the book. I'm assuming we'll need to mess around with the dataframes (book_library, audio_map) somehow
    to fully configure it
    '''
    def __init__(self):
        self.story = []
        # path = "./ereadpngs"
        '''os.chdir(path)
        for file in os.listdir():
            self.story.append(file)'''
        
    def save_files(self):
        file = open('story.txt','w')
        for stories in self.story:
            if stories not in file:
                file.write(stories +'\n')
        file.close()

    def add_story(self,filename):
        self.story.append(filename)

class sounds_file:
    def __init__(self):
        self.sounds = []

        if os.path.exists("tometoread_sounds.csv"):
            df = pd.read_csv("tometoread_sounds.csv")
            self.sounds = df['0'].tolist()

        else:
            path = "./ereadSounds"
            curdir = os.getcwd()
            os.chdir(path)
            for file in os.listdir():
                self.sounds.append(file)
            os.chdir(curdir)

    def save_songs(self):
        self.sound_df = pd.DataFrame(self.sounds)

        os.chdir("...")

        if not os.path.exists("tometoread_sounds.csv"):
            self.sound_df.to_csv("tometoread_sounds.csv", header='column_names', index=False)
        else:
            df_check = pd.read_csv('tometoread_music.csv')['0'].tolist()

            self.new_sounds = []
            for sound in self.sounds:
                if sound not in df_check:
                    self.new_sounds.append(sound)
            self.new_sounds_df = pd.DataFrame(self.new_sounds)
            self.new_sounds_df.to_csv("tometoread_sounds.csv", mode='a', header=False, index=False)
        print("Sounds have been saved")

    def add_sound(self, filename):
        self.sounds.append(filename)
        print("Sound has been saved!")
    
class music_file:
    def __init__(self):
        
        self.files = []
        # checking to see if the tometoread.txt file exists
        # if it exists, reads the file, and appends the name of each song or path to self.files
        if os.path.exists("tometoread_music.csv"):
            df = pd.read_csv('tometoread_music.csv')            
            self.files = df['0'].tolist()
            
        else:
            # If tometoread_music.txt does not exist, reads the ereadmp3 folder
            # and grabs all the names and appends them into self.files
            path = "./ereadmp3"
            curdir = os.getcwd()
            os.chdir(path)
            for file in os.listdir():
                self.files.append(file)
            os.chdir(curdir)
        
        
    def save_files(self):
        # creates a dataframe from the self.files list
        self.song_dataframe = pd.DataFrame(self.files)

        # changes the directory back into the main folder
        os.chdir("...")

        # check to see if tometoread.csv exists
        if not os.path.exists("tometoread_music.csv"):
            self.song_dataframe.to_csv("tometoread_music.csv", header='column_names', index=False)
        else:
        # If tometoread.csv exists, simply appends the NEWEST contents of self.song_dataframe

            # Making a Dataframe from tometoread_music for checking purposes
            df_check = pd.read_csv('tometoread_music.csv')['0'].tolist()

            # Loop over each song in self.files
            #   if song not in df_check
            #       add the NEW song into a separate structure
            # Add separate structure into the csv file
            self.new_songs = []
            for song in self.files:
                if song not in df_check:
                    self.new_songs.append(song)
            self.new_songs_df = pd.DataFrame(self.new_songs)
            self.new_songs_df.to_csv('tometoread_music.csv',mode = 'a', header=False, index= False)
        print("Songs have been saved.")

    def add_file(self,filename):
        self.files.append(filename)
        print("Song has been added!")



class tome_to_read(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (start_page,main_menu, settings_page, upload_page,library_page): # and ereader page, about us page, library page
            frame = F(self.container,self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame(start_page)

        
        # pygame.mixer.music.load(self.music.files[3])
        # pygame.mixer.music.play(loops=0)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_music(self):
        return self.mp3s
        
    def upload_file(self,type_of_upload):
        if type_of_upload in ["Music","Sound"]:
            file_type = [("Mp3 Files","*.mp3")]
        if type_of_upload == "Story":
            file_type = [("Pdf file","*.pdf"), ("text files","*.txt")]
        file = askopenfile(parent=self,mode="rb", title=f'Choose {type_of_upload} to upload!', filetype=file_type)

        # Handles adding Music files
        if type_of_upload == "Music" and file:
            # do something with the music file 
            music.add_file(file.name)
            pygame.mixer.music.load(file.name)
            pygame.mixer.music.play(loops=0)
            music.save_files()
        
        # Handles adding Story files
        if type_of_upload == "Story" and file:
            self.story.add_story(file)
            self.story.save_files()

        # Handles adding Sound files 
        if type_of_upload == "Sound" and file:
            pass

class start_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        img = ImageTk.PhotoImage(Image.open("extra_background.jpg").resize((1200,800)), Image.ANTIALIAS)
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

        instructions = Button(self, text="Click here to begin!", font=("Raleway", 32), command=lambda: controller.show_frame(main_menu), borderwidth=0)
        instructions.place(relx=.55,rely=.95, anchor= S)
        

# Music is supposed to play when this screen is shown, 
class main_menu(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)        
        # button layout
        # library button, upload button
        # about us button, settings button

        # button for about us page | Page not implemented 
        about_us_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="About Us",
            text_font = ("Raleway", 15)
            # implement command once about us page is done

        )
        about_us_btn.pack(side="left")
        about_us_btn.place(relx=.45, rely=.775, anchor=CENTER)
        
        # button for library page | Page not implemented
        library_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="Library",
            text_font = ("Raleway", 15),
            command = lambda: controller.show_frame(library_page)
        )
        library_btn.pack(anchor=CENTER)
        library_btn.place(relx=.45,rely=.7,anchor=CENTER)

        # button for upload page
        
        upload_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="Upload",
            text_font=("Raleway", 15),
            command = lambda: controller.show_frame(upload_page)
        )
        upload_btn.pack(anchor=CENTER)
        upload_btn.place(relx=.55,rely=.7,anchor=CENTER)

        # button for settings page
        settings_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=2,
            text="Settings",
            text_font= ("Raleway", 15),
            command = lambda: controller.show_frame(settings_page)
        )
        settings_btn.pack(anchor=CENTER)
        settings_btn.place(relx=.55, rely=.775, anchor=CENTER)

        # logo in main menu
        logo = Image.open("TomeToRead_Logo.png")
        logo = logo.resize((350,380))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.5, rely=.3, anchor= CENTER)

class upload_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # top portion of the user upload page
        upload_header = Frame(self, width = 10000, height = 100, bg = "white")
        upload_header.grid(columnspan=3,rowspan=2,row=0)
        upload_label = Label(self, text = "Add in your own story, music, or sound!", font = ("Raleway", 32), fg="black", bg="white")
        upload_label.place(relx=.5,y=50,anchor=CENTER)
        # Placing button into the top section of settings page
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)

        back_arrow = customtkinter.CTkButton(
        upload_header,
        width=50,
        height=30,
        border_width=0,
        corner_radius=2,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        # placeholder upload button
        upload_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Library",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Story")
        )
        
        upload_btn.place(relx=.3, rely=.5, anchor= CENTER)
    
        # Upload Music button, only allows upload of mp3 files
        music_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Music",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Music")
        )
        music_upload.place(relx=.7,rely=.5,anchor = CENTER)

        # Upload Sound button, only allows upload of mp3 files
        sound_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=2,
            text="Add to Sounds",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Sound")
        ).place(relx=.5,rely=.5,anchor=CENTER)

        # frame that showcases all the songs that are stored
        all_songs = Label(self,font=("Raleway",16), text = "All songs", anchor=CENTER)
        all_songs.place(relx=.66,rely=.15)
        songlistbox = Listbox(self,width=25,height=10,background="grey", selectmode=BROWSE)
        songlistbox.place(relx=.7,rely=.3,anchor=CENTER)
        for i, song in enumerate(music.files):
            songlistbox.insert(i,song)

class settings_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # Top portion of the settings page
        settings_header = Frame(self, width= 10000, height=100, bg="white")
        settings_header.grid(columnspan=3,rowspan=2,row=0)
        settings_label = Label(self, text = "Settings", font = ("Raleway", 32), fg="black", bg="white")
        settings_label.place(relx=.5,y=50,anchor=CENTER)
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
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        # sec1 frame
        sec1 = Frame(self,width=585,height=70,bg='white')
        sec1.place(relx=.5,rely=.2,anchor=N)

        # labels
        interface_lbl = Label(sec1, text="Interface Settings",font=("Raleway", 14), fg="black",bg="white")
        interface_lbl.place(relx=.5,rely=.2,anchor=CENTER)
        light_dark_lbl = Label(sec1, text="Interface Style:", font=("Raleway",12), fg="black",bg="white")
        light_dark_lbl.place(relx=.2,rely=.7,anchor=CENTER)

        # sec2 frame
        sec2 = Frame(self,width=585,height=225,bg="white")
        sec2.place(relx=.5,rely=.4,anchor=N)

        volume_lbl = Label(sec2, text="Volume Settings", font = ("Raleway", 14), fg="black", bg="white")
        volume_lbl.place(relx=.5, rely=.1,anchor=CENTER)
        music_lbl = Label(sec2, text="Music:", font = ("Raleway", 12), fg="black", bg="white")
        music_lbl.place(relx=.23, rely=.4,anchor=CENTER)
        soundfx_lbl = Label(sec2, text="Sound FX:", font = ("Raleway", 12), fg="black", bg="white")
        soundfx_lbl.place(relx=.2, rely=.6,anchor=CENTER)

        # sec3 frame
        sec3= Frame(self,width= 585, height=225, bg="white")
        sec3.place(relx=.5,rely=.75, anchor=N)


        font_lbl = Label(sec3, text="Font Settings:", font = ("Raleway", 14), fg="black", bg="white")
        font_lbl.place(relx=.5, rely=.1,anchor=CENTER)
        fstyle_lbl = Label(sec3, text="Font Style:", font = ("Raleway", 12), fg="black", bg="white")
        fstyle_lbl.place(relx=.2, rely=.4,anchor=CENTER)
        fsize_lbl = Label(sec3, text="Font Size:", font = ("Raleway", 12), fg="black", bg="white")
        fsize_lbl.place(relx=.2, rely=.6,anchor=CENTER)

class library_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        # Top portion of the settings page
        settings_header = Frame(self, bg="white", width=1200,height=100)
        settings_label = Label(settings_header, text = "Library", font = ("Raleway", 32), fg="black", bg="white")
        settings_label.pack(anchor=CENTER,fill="none",expand=False)
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
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side=LEFT,expand=False,pady=25,padx=25)
        settings_header.pack(fill=BOTH)
        
        # Creating the canvas
        scrollable_canvas = Canvas(self)
        scrollable_canvas.pack(side=LEFT,fill=BOTH,expand=1)

        # Creating a scrollbar
        library_scrollbar = Scrollbar(self, orient = VERTICAL, command = scrollable_canvas.yview)
        library_scrollbar.pack(side = RIGHT, fill = Y)

        # Configuring Canvas with scrollbar
        scrollable_canvas.configure(yscrollcommand=library_scrollbar.set)

        # Binding configure
        scrollable_canvas.bind('<Configure>', lambda e: scrollable_canvas.configure(scrollregion = scrollable_canvas.bbox("all")))

        # Creating another frame inside canvas
        canvas_frame = Frame(scrollable_canvas)

        # adding new frame to window in canvas
        scrollable_canvas.create_window((0,125), window=canvas_frame, anchor="nw")
        
        
        def action(item):
            return customtkinter.CTkButton(canvas_frame, width=200,height=300,border_width=2, 
            corner_radius=8,text = item,text_color='black', command = lambda: func(item)
            )

        def func(item):
            create_book(item,'on','',scrollable_canvas)

        rows = 0
        columns = 0
        col_adv = 0
        for i, item  in enumerate(book_library['Title']):
            b = action(item)
            #create_book(item,'on','',tk.Frame)
            #btn2.pack(side="right")
            # if line % 5 == 0:
            
            # First 3 buttons should be placed in (0,0),(0,1),(0,2)
            b.grid(row = rows, column = columns + i, padx = 5, pady = 10)

            # Then condition hits and then the next set of buttons should be placed in 
            # (1,0),(1,1),(1,2), and so forth for every 3 or 4 buttons
            if rows % 5 != 0:
                rows = rows + 1
                columns += 1
                
        '''else:
                b.grid(row = i, column = line, padx = 5, pady = 10)
            line += 1'''
        
        '''
        scrollable_canvas = Canvas(self)
        scrollable_canvas.pack(side=LEFT,fill=BOTH,expand=1)
        
        

        scrollbar = Scrollbar(scrollable_canvas, orient='vertical')
        scrollbar.place(anchor=E,bordermode=OUTSIDE, height=1200, width=25)
        
        
        
        back_arrow = customtkinter.CTkButton(
        settings_header,
        width=50,
        height=30,
        border_width=0,
        corner_radius=2,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)


        ''''''
        i=0
        x1 = -230
        y1 = -100
        line = 1
        my_str = tk.StringVar(self)


        def action(item):
            return customtkinter.CTkButton(scrollable_canvas, width=200,height=300,border_width=2, 
            corner_radius=8,text = item,text_color='black', command = lambda: func(item)
            )

        def func(item):
            create_book(item,'on','',self)
        lib = []
        for item in book_library['Title']:
            b = action(item)
            #create_book(item,'on','',tk.Frame)
            #btn2.pack(side="right")
            if line % 3 == 0:
                b.place(relx=.5, rely=.5,x=x1,y=y1, anchor=CENTER)
                y1+=320
                x1= -230
            else:
                b.place(relx=.5, rely=.5,x=x1,y=y1, anchor=CENTER)
                x1+=230
            line+=1
            i+=1
            #lib.append[b]
        print(lib)
           # x1+=230'''


class Book:
    def __init__(self,book_title, sound,theme,window):
        #self.window = window
        
        self.window = window
        self.book_title = book_title
        self.sound = sound
        self.theme = theme
        if __name__ == "__main__":
            self.main()

    def sound_switch(self):
        if self.sound == 'on':
            self.sound = 'off'
        else:
            self.sound = 'on'
        return

    def sound_switch_button(self):
        return

    def get_from_library(self,target_url):
        '''
        This function finds the url to our database in github.
        '''
        response = requests.get(target_url)
        data = response.text
        return(data)

    def music(self,n,song):
        if n == 1:
            pygame.mixer.music.load('ereadmp3/'+song)
            pygame.mixer.music.play(loops=3000)
        else:
            i = 'do nothing'

    def music_player(self,window,title):
        #if title != 'continue':
        #   music(0,title)
        #   return
        if window.counter >= len(audio_map[title]):
            song = prev_song[0]
        else:
            song = audio_map[title].iloc[(window.counter)]
        print(song)
        if self.sound == 'off':
            #do nothing
            sound = 'off'
        elif window.counter == 0:
            prev_song[0] = song
            self.music(1,song)
        elif song != prev_song[0] and window.counter != 0:
            prev_song[0] = song
            self.music(1,song)
        else:
            prev_song[0] = song
            self.music(0,song)

    def diction(self,book):
        '''
        Basically this function creates dictionary
        that links the pages of the story with an index number.
        print(diction) will show you what I am referring too.
        '''
        
        diction = {}
        i = 0
        for row in book_library['Title']:
            diction[book_library['Title'][i]] = i
            print(diction)
            i+=1
        index = diction[book]
        # The line below is how the book is found in the dictionary. 
        story = self.get_from_library(target_url = book_library['URL'][index]) 
        if book != "The Raven":
            story = self.split_function(story)
        else:
            print('working')
        final_pages=story.split('---split---') #this is the page splitting decider.
        # We will either need to write a function to change pdfs into txt files
        return final_pages, book


    def pages(self,window,final_pages, forward_back,title):
        '''
        This creates the pages of the tkinter pop up. Currently only works for
        the story Drifting Towards Purpose as the others text files are not formatted
        yet. 
        '''
        #think of adding mp3 call functions based on page here. 
        #Something like mp3_play(window, window.counter, volume_on == true)
        pages_total = len(final_pages)
        if forward_back == "back" and window.counter > 0:
            window.counter -= 1
        if forward_back == "adv" and window.counter != len(final_pages):
            window.counter += 1
        moderator = len(final_pages) <= window.counter
        if moderator == False:
            self.music_player(window,title)
        canvas = Canvas(bg="dark gray", width=595, height=770)
        canvas.place(relx=.5, rely=.5,x=-60,anchor=CENTER)
        canvas.config(highlightthickness=0)
        text = canvas.create_text(30, 20, text=str(window.counter)+'/'+str(pages_total) if moderator == False else self.thanks(), fill="black", font=('Times 17'),width=510, )
        text = canvas.create_text(300, 400, text=final_pages[window.counter] if moderator == False else self.thanks(), fill="black", font=('Times 17'),width=530, )

    def thanks(self):
        '''
        Currently the last page of the book. It just prints thank you.
        '''
        self.music(0,'none')
        canvas = Canvas(bg="dark gray", width=595, height=770)
        canvas.place(relx=.5, rely=.5,x=-60, anchor=CENTER)
        canvas.config(highlightthickness=0)
        text = canvas.create_text(300, 400, text="Thank you For Reading", fill="black", font=('Times 25'),width=430)
        text = canvas.create_text(300, 550, text="Music by Eric Matyas\nwww.soundimage.org", fill="black", font=('Times 18'),width=430)


    def information(self):
        '''
        Information on book
        '''
        canvas = customtkinter.CTkLabel(width=225, height=500,text="Title:\n"+self.book_title+"\nAuthor:\n\nYear:\n\nInfo:\n\n")
        canvas.place(relx=.5, rely=.5,x=465,y=-100, anchor=CENTER)
        canvas.config(highlightthickness=0)

    def music_information(self):
        '''
        Information on song
        '''
        canvas = customtkinter.CTkLabel(width=250, height=80,text="Song Title:\nExample -By: Example")
        canvas.place(relx=.5, rely=.5,x=410,y=230, anchor=CENTER)
        canvas.config(highlightthickness=0)

    def menu_bar(self,window):
        frame_4 = customtkinter.CTkFrame(width=80, height=500)
        frame_4.place(relx=.5, rely=.5,x=-520, anchor=CENTER)
        frame_4.configure(fg_color=("lightgray"))
        self.library_button(frame_4)
        self.find_button(frame_4)
        self.settings_button(frame_4)
        self.upload_button(frame_4)
        frame_4.tkraise()
    
    def library_return(self):
        None
    def finder(self):
        None
    def settings_link(self):
        None
    def upload_link(self):
        None

    def find_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/book-research.png')
        btn2 = customtkinter.CTkButton(master = frame, width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.finder()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-180, anchor=CENTER)

    def library_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/binder-file.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.library_return()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-60, anchor=CENTER)
    def upload_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/cloud-upload.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.upload_link()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=180, anchor=CENTER)

    def settings_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/settings-gear.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", "lightgray"),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.settings_link()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=60, anchor=CENTER)
    
    def volume(self):
        return

    def vol_slider(self,window):
        slider = customtkinter.CTkSlider(
        width=230,
        height=25,
        border_width=5.5,
        from_=0,
        to=100,
        command=self.volume())
        slider.place(relx=0.5, rely=0.5,x=410,y=300, anchor=CENTER)

    def adv_button(self,window,final_pages,title):
        photo = PhotoImage(file = 'ereadpngs/chevron-right.png')
        photo = photo.subsample(15)
        adv = "adv"
        btn2 = customtkinter.CTkButton(
        width=80,
        height=80,
        border_width=0,
        corner_radius=8,
        text = '',
        image = photo,
        text_color='black',
        command = lambda: self.pages(window,final_pages,adv,title)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=290, anchor=CENTER)

    def back_button(self,window,final_pages,title):
        photo = PhotoImage(file = 'ereadpngs/chevron-left.png')
        photo = photo.subsample(15)
        back = "back"
        btn2 = customtkinter.CTkButton(
        width=80,
        height=80,
        border_width=0,
        corner_radius=8,
        text = '',
        image = photo,
        text_color='black',
        command = lambda: self.pages(window,final_pages,back,title)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=-410, anchor=CENTER)

    def split_function(self,story):
        story = story.splitlines(True)
        new_story = ''
        i = 0
        n=0
        for line in story:
            if i == 18:
                new_story += '\n---split--- '
                i=0
            if line == '---chapter---\n':
                new_story += '\n---split---\n '
                i=3
            elif line[-2:] != '\n':
                new_story+=line+' \n'
            else:
                new_story+=line.strip('\n')
            i+=1
            n+=1
        return new_story

    def main(self):
        ''' 
        Creates the window, and calls this diction function to get a key value pair linked by page number.
        Currently only supports .txt files because pdf files lack the functionality 
        to be manipulated and most domain stories use .txt or .epub not pdf.
        '''
        frame_3 = Frame(width=10000, height=10000)
        frame_3.place(relx=.5, rely=.5, anchor=CENTER)
        frame_3.configure()
        frame_3.tkraise()
        frame_4 = Frame(width=1200, height=800)
        frame_4.place(relx=.5, rely=.5, anchor=CENTER)
        frame_4.configure()
        frame_4.tkraise()
        
        window = frame_4
        window.counter = -1 #this is universal counter funtion that allows a user to traverse a story.
        final_pages, title = self.diction(self.book_title)
        self.vol_slider(window)
        self.adv_button(window, final_pages, title)
        self.back_button(window, final_pages, title) 
        self.information()
        self.music_information()
        self.menu_bar(window)
        #window.mainloop() #basically refreshes the window

music = music_file()
stories = story_file()
sounds = sounds_file()

def create_book(title,two,three,frame):
    Book(title,two,three,frame)

def main():
    # Main window that pops up
    app = tome_to_read()
    app.title("Tome to Read")
    app.resizable(False,False)
    app.geometry("1200x800")
    app.counter = -1
    '''final_pages, title = ereader_page.diction(ereader_page.book_title)
    ereader_page.vol_slider(app)
    ereader_page.adv_button(app, final_pages, title)
    ereader_page.back_button(app,final_pages, title)
    ereader_page.information()
    ereader_page.music_information()
    ereader_page.menu_bar(app)''' # fix up ereader class
    app.mainloop()
    
if __name__ == "__main__":
    main()