'''
TITLE: Tome To Read
AUTHORS: James Thomason, Colby Chambers, Sarah Valine, and Cole Dryer
'''


from distutils.sysconfig import customize_compiler
from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from turtle import bgcolor
from PIL import Image, ImageTk
import customtkinter
import pandas as pd
import requests
import pygame
import os
import os.path
import pdfplumber
import random

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
bg_music_channel = pygame.mixer.Channel(3)
theme_diction = {"dark_mode" : ["dark slate gray", "cadet blue", "DarkOrange3", "light slate blue"],
"light_mode" : ["MistyRose2", "linen", "IndianRed1", "white"],
"tan_mode" : ["PeachPuff2", "bisque", "sandy brown", "dark khaki"] }
user_settings = { 'font' : "Times", 'theme' : theme_diction["light_mode"] }


url='https://raw.githubusercontent.com/colbychambers25/immersive-ebook/main/Domain_Free_eBook.csv'
book_library = pd.read_csv(url) #print to see what the panda looks like
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/Sound_audio_map.csv'
audio_map = pd.read_csv(url)
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/soundeffects_map.csv'
sound_effects_map = pd.read_csv(url)
prev_song = ['none']
library_map = {}
volume=50


class user_audio_map:
    
    def __init__(self):
        global audio_map
        
        if os.path.exists("ereadCSV/tometoread_songConfig.csv"):
            df = pd.read_csv("ereadCSV/tometoread_songConfig.csv")
            audio_map = df
       
    def set_user_audio_config(self):
        self.audio_map_copy = audio_map.copy()
        
    def save_audio_config(self):
        self.audio_map_copy.to_csv("ereadCSV/tometoread_songConfig.csv", index = False)
        print("Song to Book Config has been saved!")
        
class user_sound_map: # INCOMPLETE CLASS

    def __init__(self):
        global sound_effects_map
        if os.path.exists("ereadCSV/tometoread_sound_config.csv"):
            df = pd.read_csv("ereadCSV/tometoread_sound_config.csv")
            sound_effects_map = df
            print(sound_effects_map)

    def set_user_sound_config(self):
        self.sound_fx_map_copy = sound_effects_map.copy()

    def save_sound_config(self):
        self.sound_fx_map_copy.to_csv("ereadCSV/tometoread_sound_config.csv", index = False)
        print("Sound to Book Config has been saved!")
        

class story_file:
    def __init__(self, book_library):
        
        self.userStory = []
        
        # Handling if the user story file already exists within the ereadCSV folder
        if os.path.exists("ereadCSV/tometoread_Stories.csv"):
            df = pd.read_csv("ereadCSV/tometoread_Stories.csv", header=None)
            self.userStory = df
            for index, row in self.userStory.iterrows():
                book_library.loc[len(book_library.index)] = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                audio_map[row[1]] = "None"      

    def set_user_story(self):
        self.userStory = book_library.loc[book_library['Provider'] == "User"]
        
    def save_stories(self):
        self.userStory.to_csv("ereadCSV/tometoread_Stories.csv", header=False,index=False)
        print("Story has been saved to csv file!")
        

class sounds_file:
    def __init__(self):
        self.sounds = []
        self.userSounds = []
        if os.path.exists("ereadCSV/tometoread_sounds.csv"):
            df = pd.read_csv("ereadCSV/tometoread_sounds.csv")
            self.sounds = df['0'].tolist()

        else:
            path = "./ereadSounds"
            self.curdir = os.getcwd()
            os.chdir(path)
            for file in os.listdir():
                if not file.startswith("C:"):
                    self.sounds.append("ereadSounds/" + file)
                else:
                    self.userSounds.append(file)
            self.sounds = self.sounds + self.userSounds
            os.chdir(self.curdir)
            

    def save_sounds(self):
        self.sound_df = pd.DataFrame(self.sounds)

        os.chdir(self.curdir)

        if not os.path.exists("ereadCSV/tometoread_sounds.csv"):
            self.sound_df.to_csv("ereadCSV/tometoread_sounds.csv", header='column_names', index=False)
        else:
            df_check = pd.read_csv('ereadCSV/tometoread_sounds.csv')['0'].tolist()

            self.new_sounds = []
            for sound in self.sounds:
                if sound not in df_check:
                    self.new_sounds.append(sound)
            self.new_sounds_df = pd.DataFrame(self.new_sounds)
            self.new_sounds_df.to_csv("ereadCSV/tometoread_sounds.csv", mode='a', header=False, index=False)
        print("Sound has been saved!")

    def add_sound(self, filename):
        self.sounds.append(filename)
        print("Sound has been added!")
    
class music_file:
    def __init__(self):
        
        self.files = []
        self.userFiles = []
        # checking to see if the tometoread.csv file exists
        # if it exists, reads the file, and appends the name of each song or path to self.files
        if os.path.exists("ereadCSV/tometoread_music.csv"):
            df = pd.read_csv('ereadCSV/tometoread_music.csv')            
            self.files = df['0'].tolist()
            
        else:
            # If tometoread_music.csv does not exist, reads the ereadmp3 folder
            # and grabs all the names and appends them into self.files
            path = "./ereadmp3"
            self.curdir = os.getcwd()
            os.chdir(path)
            for file in os.listdir():
                if not file.startswith("C:"):
                    self.files.append("ereadmp3/" + file)
                else:
                    self.userFiles.append(file)
            self.files = self.files + self.userFiles
            os.chdir(self.curdir)
        
        
    def save_files(self):
        # creates a dataframe from the self.files list
        self.song_dataframe = pd.DataFrame(self.files)

        # changes the directory back into the main folder
        os.chdir(self.curdir)

        # check to see if tometoread.csv exists
        if not os.path.exists("ereadCSV/tometoread_music.csv"):
            self.song_dataframe.to_csv("ereadCSV/tometoread_music.csv", header='column_names', index=False)
        else:
        # If tometoread.csv exists, simply appends the NEWEST contents of self.song_dataframe

            # Making a Dataframe from tometoread_music for checking purposes
            df_check = pd.read_csv('ereadCSV/tometoread_music.csv')['0'].tolist()

            # Loop over each song in self.files
            #   if song not in df_check
            #       add the NEW song into a separate structure
            # Add separate structure into the csv file
            self.new_songs = []
            for song in self.files:
                if song not in df_check:
                    self.new_songs.append(song)
            self.new_songs_df = pd.DataFrame(self.new_songs)
            self.new_songs_df.to_csv('ereadCSV/tometoread_music.csv',mode = 'a', header=False, index= False)
        print("Songs have been saved.")

    def add_file(self,filename):
        self.files.append(filename)
        print("Song has been added!")

class tome_to_read(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        pygame.mixer.music.load("ereadmp3/main_bg_music.mp3")
        pygame.mixer.music.play(loops=0)

        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = customtkinter.CTkFrame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (start_page,main_menu, settings_page, upload_page,library_page, Configure, FAQ, about_us, about_us2): 
            frame = F(self.container,self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame(start_page)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        
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
        
            sound_obj = pygame.mixer.Sound(file)
            pygame.mixer.find_channel().play(sound_obj)
            # pygame.mixer.music.load(file.name)
            # pygame.mixer.music.play(loops=0)
            music.save_files()
        
        # Handles adding Story files !!! NOT DONE NOT DONE NOT DONE NOT DONE !IMPORTANT
        if type_of_upload == "Story" and file:
            self.story.add_story(file)
            self.story.save_files()

        # Handles adding Sound files 
        if type_of_upload == "Sound" and file:
            soundFiles.add_sound(file.name)
            # TESTING PURPOSES
            sound_obj = pygame.mixer.Sound(file)
            pygame.mixer.find_channel().play(sound_obj)
            # ]
            soundFiles.save_sounds()

    def mute_bg_music(self):
        pygame.mixer.music.pause()
    
    def change_font_options_global(self, font_options, var):
        if font_options == "Style":
            self.option_add('*Font', var)
        if font_options == "Size":
            self.option_add('*Font', var)
        
        
class start_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        img = ImageTk.PhotoImage(Image.open("ereadpngs/welcome page.jpg"), Image.ANTIALIAS)
        labl = tk.Label(self, image=img)
        labl.img = img
        labl.place(relx=0.5, rely=0.5, anchor= CENTER)

        # main logo creation, implementation, placing into frame
        #logo = Image.open("TomeToRead_Logo.png")
        #logo = logo.resize((350,380))
        #logo = ImageTk.PhotoImage(logo)
        #logo_label = Label(self,image=logo)
        #logo_label.image = logo
        #logo_label.place(relx=.55, rely=.4, anchor= CENTER)
        # end of main logo creation, implementation, placing into frame

        instructions = customtkinter.CTkButton(self, fg_color="sienna3",text="Click here to begin!", text_font=("Raleway", 32), command=lambda: controller.show_frame(main_menu), corner_radius=10)
        instructions.place(relx=.5,rely=.90, anchor= CENTER)

# Music is supposed to play when this screen is shown, 
class main_menu(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent) 
        self.config(bg='wheat1')       
        # button layout
        # library button, upload button
        # about us button, settings button
        img = ImageTk.PhotoImage(Image.open("ereadpngs/nav page.jpg"), Image.ANTIALIAS)
        labl = tk.Label(self, image=img)
        labl.img = img
        labl.place(relx=0.5, rely=0.5, anchor= CENTER)
        # button for about us page | Page not implemented 
        about_us_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=10,
            text="About Us",
            fg_color="sienna3",
            text_font = ("Raleway", 15),
            command = lambda: controller.show_frame(about_us)

        )
        about_us_btn.pack(side="left")
        about_us_btn.place(relx=.5, rely=.925, anchor=CENTER)
        
        # button for library page | Page not implemented
        library_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=10,
            text="Library",
            fg_color="sienna3",
            text_font = ("Raleway", 15),
            command = lambda: controller.show_frame(library_page)
        )
        library_btn.pack(anchor=CENTER)
        library_btn.place(relx=.282,rely=.85,anchor=CENTER)

        # button for upload page
        
        upload_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=10,
            text="Upload",
            fg_color="sienna3",
            text_font=("Raleway", 15),
            command = lambda: controller.show_frame(upload_page)
        )
        upload_btn.pack(anchor=CENTER)
        upload_btn.place(relx=.382,rely=.85,anchor=CENTER)

        # button for settings page
        settings_btn = customtkinter.CTkButton(
            self,
            width = 100,
            height = 50,
            border_width=0,
            corner_radius=10,
            text="Settings",
            fg_color="sienna3",
            text_font= ("Raleway", 15),
            command = lambda: controller.show_frame(settings_page)
        )
        settings_btn.pack(anchor=CENTER)
        settings_btn.place(relx=.621, rely=.85, anchor=CENTER)

        configure_button = customtkinter.CTkButton(
            self,
            width=100, height = 50,
            border_width=0, corner_radius=10,
            text="Configure Books",
            fg_color="sienna3",
            text_font = ("Raleway",15),
            command = lambda: controller.show_frame(Configure)
        )
        configure_button.pack(anchor=CENTER)
        configure_button.place(relx=.5,rely=.85,anchor=CENTER)

        faq_btn = customtkinter.CTkButton(
            self,
            width=100, height = 50,
            border_width=0,
            corner_radius=10,
            text="FAQ",
            fg_color="sienna3",
            text_font = ("Raleway",12),
            command = lambda: controller.show_frame(FAQ)
        )
        faq_btn.pack(anchor=CENTER)
        faq_btn.place(relx=.72,rely=.85,anchor=CENTER)

        # logo in main menu

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

class about_us(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        # ============== About Us (au) Frame Set Up ==================

        au_header = Frame(self, width= 1200, height=100, bg="sienna4")
        au_header.grid(columnspan=3,rowspan=2,row=0)
        au_label = Label(au_header, text = "Meet the Team!", font = ("Raleway", 32), fg="light gray", bg="sienna4")
        au_label.place(relx=.5,rely=.5,anchor=CENTER)

        # ============== Back Arrow ==================================
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        
        back_arrow = customtkinter.CTkButton(
            au_header,
            width=50,
            height=50,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            image=back_arrow_img,
            text = '',
            command= lambda: controller.show_frame(main_menu)
        )

        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        au_descr = Frame(self, width= 1000, height=300, bg="white")
        au_descr.grid(columnspan=4,rowspan=4,row=4)
        au_descr.place(x=100,y=350,anchor=W)

        # =============== COLBY =============================
        
        # =========== Image and Button ======================

        colbpic = PhotoImage(file = 'ereadpngs/colby.png')
        colbpic = colbpic.subsample(7)

        picture1 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = colbpic,
            text_color= 'black',
            command= lambda: controller.show_frame(about_us2)
        )
        picture1.pack(side= "right")
        picture1.place(relx= .5, rely= .5, x= -375, anchor= CENTER)

        # =========== Frame for Name Tag/ Bio ===============

        cb_name = Frame(self, width=175, height=50, bg="white")
        cb_name.grid(columnspan=2,rowspan=2,row=4)
        cb_name.place(x=140, y=150, anchor=W)

        cb_facts = Frame(self, width=200, height=250, bg="white")
        cb_facts.grid(columnspan=2, rowspan=2, row=4)
        cb_facts.place(x=125, y=650, anchor=W)

        # ====== Colby's Name Tag and Bio Labels ============

        name1 = "Colby Chambers"
        about1 = "Major: Information Science \n and Technology \n Role: Team Lead, Ereader, \n and App Design"

        n1_label = Label(cb_name, text = name1, font = ("Raleway", 15), fg="black", bg="white")
        n1_label.place(relx=.5,rely=.5,anchor=CENTER)

        a1_label = Label(cb_facts, text= about1, font= ("Railway", 12), fg = "black", bg= "White")
        a1_label.place(relx=.5, rely=.5, anchor= CENTER)

        # ================= JAMES ========================

        # ========= James's Image and Button =============

        jampic = PhotoImage(file = 'ereadpngs/james.png')
        jampic = jampic.subsample(7)

        picture2 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = jampic,
            text_color= 'black',
            command= lambda: controller.show_frame(about_us2)
        )
        picture2.pack(side= "right")
        picture2.place(relx= .5, rely= .5, x= -125, anchor= CENTER)

        # ============= Frame for Name Tag =================

        jm_name = Frame(self, width=175, height=50, bg="white")
        jm_name.grid(columnspan=2,rowspan=2,row=4)
        jm_name.place(x=390, y=150,anchor=W)

        jm_facts = Frame(self, width=200, height=250, bg="white")
        jm_facts.grid(columnspan=2, rowspan=2, row=4)
        jm_facts.place(x=375, y=650, anchor=W)


        # ====== James's Name Tag and Bio Labels ===========

        name2 = "James Thomason"
        about2 = "Major: Information Science \n and Technology \n Role: Team Lead, \nUpload Page, \n and UI Design"

        n2_label = Label(jm_name, text = name2, font = ("Raleway", 15), fg="black", bg="white")
        n2_label.place(relx=.5,rely=.5,anchor=CENTER)

        a2_label = Label(jm_facts, text= about2, font= ("Railway", 12), fg = "black", bg= "White")
        a2_label.place(relx=.5, rely=.5, anchor= CENTER)


        # ================ COLE ========================

        # ========= Cole's Image and Button ============

        colpic = PhotoImage(file = 'ereadpngs/cole.png')
        colpic = colpic.subsample(7)
        picture3 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = colpic,
            text_color= 'black',
            command= lambda: controller.show_frame(about_us2)
        )
        picture3.pack(side= "right")
        picture3.place(relx= .5, rely= .5, x= 120, anchor= CENTER)

        # ============= Frame for Name Tag =================

        cl_name = Frame(self, width=175, height=50, bg="white")
        cl_name.grid(columnspan=2,rowspan=2,row=4)
        cl_name.place(x=640, y=150,anchor=W)

        cl_facts = Frame(self, width=200, height=250, bg="white")
        cl_facts.grid(columnspan=2, rowspan=2, row=4)
        cl_facts.place(x=625, y=650, anchor=W)
        

        # ====== Cole's Name Tag and Bio Labels ============

        name3 = "Cole Dryer"
        about3 = "Major: Information Science \n and Technology \n Role: Settings Page"

        n3_label = Label(cl_name, text = name3, font = ("Raleway", 15), fg="black", bg="white")
        n3_label.place(relx=.5,rely=.5,anchor=CENTER)

        a3_label = Label(cl_facts, text= about3, font= ("Railway", 12), fg = "black", bg= "White")
        a3_label.place(relx=.5, rely=.5, anchor= CENTER)


        # ================== SARAH ===========================

        # ============== Image and Button ====================
        sarpic = PhotoImage(file = 'ereadpngs/sarah.png')
        sarpic = sarpic.subsample(7)

        picture4 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = sarpic,
            text_color= 'black',
            command= lambda: controller.show_frame(about_us2)
        )
        picture4.pack(side= "right")
        picture4.place(relx= .5, rely= .5, x= 375, anchor= CENTER)

        # ========== Frame for Name Tag/ Bio ================

        sa_name = Frame(self, width=175, height=50, bg="white")
        sa_name.grid(columnspan=2,rowspan=2,row=4)
        sa_name.place(x=890, y=150,anchor=W)

        sa_facts = Frame(self, width=200, height=250, bg="white")
        sa_facts.grid(columnspan=2, rowspan=2, row=4)
        sa_facts.place(x=875, y=650, anchor=W)

        # ====== Sarah's Name Tag and Bio Labels ============

        name4 = "Sarah Valine"
        about4 = "Major: Information Science \n and Technology \n Role: Main Menu and \n About Us Pages"

        n4_label = Label(sa_name, text= name4, font= ("Raleway", 15), fg= "black", bg= "white")
        n4_label.place(relx=.5, rely=.5, anchor= CENTER)

        a4_label = Label(sa_facts, text= about4, font= ("Railway", 12), fg = "black", bg= "White")
        a4_label.place(relx=.5, rely=.5, anchor= CENTER)

        # ================ Mute ======================

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            fg_color="sienna3",
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

class about_us2(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        color = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        others = ['pink', 'grey', 'brown', 'light green', 'light blue']
        rand1 = random.choice(color)
        rand2 = random.choice(color)
        rand3 = random.choice(color)
        rand4 = random.choice(color)

        text = [rand1, rand2, rand3, rand4]

        for i in text:
            if i in text:
                i = 'pink'

        
        # ============== About Us (au) Frame Set Up ==================

        au_header = Frame(self, width= 1200, height=100, bg="sienna4")
        au_header.grid(columnspan=3,rowspan=2,row=0)
        au_label = Label(au_header, text = "Thank you for using Tome to Read! \n Here's some Fun Facts About Us!", font = ("Raleway", 32), fg="light gray",bg="sienna4")
        au_label.place(relx=.5,rely=.5,anchor=CENTER)

        # ============== Back Arrow ==================================
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        
        back_arrow = customtkinter.CTkButton(
            au_header,
            width=50,
            height=50,
            border_width=0,
            corner_radius=10,
            image=back_arrow_img,
            fg_color="sienna3",
            text = '',
            command= lambda: controller.show_frame(main_menu)
        )

        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        au_descr = Frame(self, width= 1000, height=300, bg="white")
        au_descr.grid(columnspan=4,rowspan=4,row=4)
        au_descr.place(x=100,y=350,anchor=W)

        # =============== COLBY =============================
        
        # =========== Image and Button ======================

        colbpic = PhotoImage(file = 'ereadpngs/colby.png')
        colbpic = colbpic.subsample(7)

        picture1 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = colbpic,
            text_color= 'black',
            command= lambda: controller.show_frame(library_page)
        )
        picture1.pack(side= "right")
        picture1.place(relx= .5, rely= .5, x= -375, anchor= CENTER)

        # =========== Frame for Name Tag/ Bio ===============

        cb_name = Frame(self, width=175, height=50, bg="white")
        cb_name.grid(columnspan=2,rowspan=2,row=4)
        cb_name.place(x=140, y=150, anchor=W)

        cb_facts = Frame(self, width=200, height=250, bg="white")
        cb_facts.grid(columnspan=2, rowspan=2, row=4)
        cb_facts.place(x=125, y=650, anchor=W)

        # ====== Colby's Name Tag and Bio Labels ============

        name1 = "Colby Chambers"
        about1 = "Likes Molding Clay Figures \n and \n Reading Manga"

        n1_label = Label(cb_name, text = name1, font = ("Raleway", 15), fg=rand1, bg="white")
        n1_label.place(relx=.5,rely=.5,anchor=CENTER)

        a1_label = Label(cb_facts, text= about1, font= ("Railway", 12), fg = rand1, bg= "White")
        a1_label.place(relx=.5, rely=.5, anchor= CENTER)

        # ================= JAMES ========================

        # ========= James's Image and Button =============

        jampic = PhotoImage(file = 'ereadpngs/james.png')
        jampic = jampic.subsample(7)

        picture2 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = jampic,
            text_color= 'black',
            command= lambda: controller.show_frame(upload_page)
        )
        picture2.pack(side= "right")
        picture2.place(relx= .5, rely= .5, x= -125, anchor= CENTER)

        # ============= Frame for Name Tag =================

        jm_name = Frame(self, width=175, height=50, bg="white")
        jm_name.grid(columnspan=2,rowspan=2,row=4)
        jm_name.place(x=390, y=150,anchor=W)

        jm_facts = Frame(self, width=200, height=250, bg="white")
        jm_facts.grid(columnspan=2, rowspan=2, row=4)
        jm_facts.place(x=375, y=650, anchor=W)


        # ====== James's Name Tag and Bio Labels ===========

        name2 = "James Thomason"
        about2 = "Played Volleyball in \n High School \n and also reads Manga. "

        n2_label = Label(jm_name, text = name2, font = ("Raleway", 15), fg=rand2, bg="white")
        n2_label.place(relx=.5,rely=.5,anchor=CENTER)

        a2_label = Label(jm_facts, text= about2, font= ("Railway", 12), fg = rand2, bg= "White")
        a2_label.place(relx=.5, rely=.5, anchor= CENTER)


        # ================ COLE ========================

        # ========= Cole's Image and Button ============

        colpic = PhotoImage(file = 'ereadpngs/cole.png')
        colpic = colpic.subsample(7)
        picture3 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = colpic,
            text_color= 'black',
            command= lambda: controller.show_frame(settings_page)
        )
        picture3.pack(side= "right")
        picture3.place(relx= .5, rely= .5, x= 120, anchor= CENTER)

        # ============= Frame for Name Tag =================

        cl_name = Frame(self, width=175, height=50, bg="white")
        cl_name.grid(columnspan=2,rowspan=2,row=4)
        cl_name.place(x=640, y=150,anchor=W)

        cl_facts = Frame(self, width=200, height=250, bg="white")
        cl_facts.grid(columnspan=2, rowspan=2, row=4)
        cl_facts.place(x=625, y=650, anchor=W)
        

        # ====== Cole's Name Tag and Bio Labels ============

        name3 = "Cole Dryer"
        about3 = "Likes to surf \n and \n makes techno/ electronic \n music in free time"

        n3_label = Label(cl_name, text = name3, font = ("Raleway", 15), fg=rand3, bg="white")
        n3_label.place(relx=.5,rely=.5,anchor=CENTER)

        a3_label = Label(cl_facts, text= about3, font= ("Railway", 12), fg = rand3, bg= "White")
        a3_label.place(relx=.5, rely=.5, anchor= CENTER)


        # ================== SARAH ===========================

        # ============== Image and Button ====================
        sarpic = PhotoImage(file = 'ereadpngs/sarah.png')
        sarpic = sarpic.subsample(7)

        picture4 = customtkinter.CTkButton(
            au_descr,
            width= 80,
            height= 80,
            border_width= 0,
            corner_radius= 8,
            text = '',
            image = sarpic,
            text_color= 'black',
            command= lambda: controller.show_frame(main_menu)
        )
        picture4.pack(side= "right")
        picture4.place(relx= .5, rely= .5, x= 375, anchor= CENTER)

        # ========== Frame for Name Tag/ Bio ================

        sa_name = Frame(self, width=175, height=50, bg="white")
        sa_name.grid(columnspan=2,rowspan=2,row=4)
        sa_name.place(x=890, y=150,anchor=W)

        sa_facts = Frame(self, width=200, height=250, bg="white")
        sa_facts.grid(columnspan=2, rowspan=2, row=4)
        sa_facts.place(x=875, y=650, anchor=W)

        # ====== Sarah's Name Tag and Bio Labels ============

        name4 = "Sarah Valine"
        about4 = "Is writing a book \n and \n loves art"

        n4_label = Label(sa_name, text= name4, font= ("Raleway", 15), fg= rand4, bg= "white")
        n4_label.place(relx=.5, rely=.5, anchor= CENTER)

        a4_label = Label(sa_facts, text= about4, font= ("Railway", 12), fg = rand4, bg= "White")
        a4_label.place(relx=.5, rely=.5, anchor= CENTER)

        # ================ Mute ======================

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            corner_radius=2,
            fg_color="sienna3",
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

class upload_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        # top portion of the user upload page
        upload_header = Frame(self, width = 10000, height = 100, bg = "sienna4")
        upload_header.grid(columnspan=3,rowspan=2,row=0)
        upload_label = Label(self, text = "Add in your own story, music, or sound!", font = ("Raleway", 32), fg="light gray", bg="sienna4")
        upload_label.place(relx=.5,y=50,anchor=CENTER)
        # Placing button into the top section of settings page
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)

        back_arrow = customtkinter.CTkButton(
        upload_header,
        width=50,
        height=50,
        border_width=0,
        corner_radius=10,
        fg_color="sienna3",
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        # upload story button
        upload_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=10,
            text="Add to Library",
            fg_color="sienna3",
            text_font = ("Raleway", 15),
            command = lambda: self.submit_story(self.story_file_path,self.cover_image_path)
        )

        self.author_var = tk.StringVar()
        self.year_pub_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.book_title = tk.StringVar()

        title_entry = Entry(self,textvariable=self.book_title,bg='sienna4')
        title_entry.place(relx=.2,rely=.15)
        title_label = Label(self,text="Title:",font=("Raleway",10), bg='wheat1',fg='sienna4')
        title_label.place(relx=.19,rely=.16,anchor=E)


        author_entry = Entry(self, textvariable=self.author_var,bg='sienna4')
        author_entry.place(relx=.2,rely=.2)
        author_entry_label = Label(self,text="Author:", font=("Raleway",10), bg='wheat1',fg='sienna4')
        author_entry_label.place(relx=.19,rely=.21,anchor=E)

        year_published_entry = Entry(self, textvariable=self.year_pub_var,bg='sienna4')
        year_published_entry.place(relx=.2,rely=.25)
        year_published_label = Label(self,text="Year Published:", font=("Raleway",10), bg='wheat1',fg='sienna4')
        year_published_label.place(relx=.19,rely=.26,anchor=E)

        genre_entry = Entry(self, textvariable=self.genre_var,bg='sienna4')
        genre_entry.place(relx=.2,rely=.3)
        genre_entry_label = Label(self, text="Genre:", font=("Raleway", 10), bg='wheat1',fg='sienna4')
        genre_entry_label.place(relx=.19, rely=.31,anchor=E)

        self.cover_image_path = "None Given"
        self.story_file_path = "fileCheck"

        cover_image_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            text="Add Book Cover",
            command = lambda: self.upload_book_cover()
        )
        cover_image_upload.place(relx=.25,rely=.35)
        
        actual_book_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            text="Add Story File",
            command = lambda : self.add_story()
        )
        actual_book_upload.place(relx=.255,rely=.42)

        upload_btn.place(relx=.3, rely=.53, anchor= CENTER)
    
        # Upload Music button, only allows upload of mp3 files
        music_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            text="Add to Music",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Music")
        )
        music_upload.place(relx=.7,rely=.53,anchor = CENTER)

        # Upload Sound button, only allows upload of mp3 files
        sound_upload = customtkinter.CTkButton(
            self,
            width=100,
            height=50,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            text="Add to Sounds",
            text_font = ("Raleway", 15),
            command = lambda: controller.upload_file("Sound")
        )
        sound_upload.place(relx=.5,rely=.53,anchor=CENTER)

        # frame that showcases all the songs that are stored
        all_songs = Label(self,font=("Raleway",16), text = "All Songs", anchor=CENTER, bg='wheat1', fg='sienna4')
        all_songs.place(relx=.66,rely=.15)
        self.songlistbox = Listbox(self,width=25,height=10,background="light grey", selectmode=BROWSE)
        self.songlistbox.place(relx=.7,rely=.3,anchor=CENTER)
        for i, song in enumerate(music.files):
            self.songlistbox.insert(i,song)

        all_sounds = Label(self,font=("Raleway",16), text="All Sounds", anchor=CENTER, bg='wheat1', fg='sienna4')
        all_sounds.place(relx=.45, rely=.15)
        self.soundlistbox = Listbox(self,width=25, height= 10, background="light grey", selectmode=BROWSE)
        self.soundlistbox.place(relx=.5,rely=.3, anchor=CENTER)
        for i,song in enumerate(soundFiles.sounds):
            self.soundlistbox.insert(i,song)

        preview_song_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            fg_color="sienna3",
            corner_radius=10,
            text="Preview Song",
            command = lambda: self.preview_sound_song_file("Song")
        )
        preview_song_btn.place(relx=.655,rely=.6)

        preview_sound_btn = customtkinter.CTkButton(
            self,
            width=100,
            height=25,
            border_width=0,
            fg_color="sienna3",
            corner_radius=10,
            text="Preview Sound",
            command = lambda: self.preview_sound_song_file("Sound")
        )
        preview_sound_btn.place(relx=.455,rely=.6)

        disclaimer = Label(self,text="Before you upload, please make sure that the file you upload will NOT BE MOVED after uploading.\nIf the file is moved, it will cause issues with Tome to Read", fg="sienna4", bg='wheat1', font=("Raleway",12))
        disclaimer.place(relx=.23,rely=.7)

        disclaimer_two = Label(self,text="Please do not upload the same file twice. It may/will cause problems with the application.",fg="sienna4", bg='wheat1', font=("Raleway",12))
        disclaimer_two.place(relx=.24,rely=.8)



        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            fg_color="sienna3",
            corner_radius=10,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)

        self.fail_or_success = StringVar(self)
        self.output_of_upload = Label(self, bg='wheat1')
        self.output_of_upload.place(relx=.2,rely=.6)

    def upload_book_cover(self):
        book_cover = askopenfilename(filetypes=[('image files','.png'),('image files','.jpg')])

        if book_cover:
            self.cover_image_path = book_cover
            cover_success = Label(self, text="Success!", font=("Raleway",10))
            cover_success.place(relx=.27,rely=.385)
            print(f'New Book Cover is: {self.cover_image_path}')

    def add_story(self):
        storyfile = askopenfilename(filetypes=(("text files", '.txt'),("text files",'.pdf')))
        if storyfile:
            self.story_file_path = storyfile
            story_success = Label(self,text="Success!", font=("Raleway",10))
            story_success.place(relx=.27,rely=.455)
            print(f'New Story is: {self.story_file_path}')
    
    def submit_story(self,book_path="fileCheck",book_cover="None Given"):
        if book_path == "fileCheck":
            self.fail_or_success.set("Please upload a story file to add new story.")
            self.output_of_upload.config(text=self.fail_or_success.get(),font=("Raleway",10), fg="sienna4", bg="wheat1")
        else:
            if book_cover == "None Given":
                book_cover = "ereadpngs/tome2.png"
            provider = "User"
            views = 0
            title = self.book_title.get()
            author = self.author_var.get()
            year = self.year_pub_var.get()
            genre = self.genre_var.get()

            # adding new row to book_library with information
            book_library.loc[len(book_library.index)] = [book_path,title,author,year, provider, views, genre, book_cover]

            audio_map[title] = "None"
            sound_effects_map[title] = "None"
            # MAKE A CALL TO SAVE THE AUDIO MAP USING THE PROVIDED CLASS
            # MAKE A CALL TO SAVE THE SOUND EFFECTS MAP TO CSV USING PROVIDED CLASS
            # make a call to set the audio_map and sound_fx map
            
            
            self.fail_or_success.set("Story has been added!")
            self.output_of_upload.config(text=self.fail_or_success.get(), font=("Raleway",10), fg="sienna4", bg="wheat1")
            self.output_of_upload.place(relx=.25,rely=.6)

            stories.set_user_story()
            stories.save_stories()

    def preview_sound_song_file(self,song_or_sound):
        if song_or_sound == "Song":
            song = self.songlistbox.get(self.songlistbox.curselection())
            song_Sound_obj = pygame.mixer.Sound(song)
            channel3.play(song_Sound_obj)
        if song_or_sound == "Sound":
            sound = self.soundlistbox.get(self.soundlistbox.curselection())
            ttr_sound_Sound_obj = pygame.mixer.Sound(sound)
            channel3.play(ttr_sound_Sound_obj)
        
class settings_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        # Top portion of the settings page
        settings_header = Frame(self, width= 1200, height=100, bg="sienna4")
        settings_header.grid(columnspan=3,rowspan=2,row=0)
        settings_label = Label(settings_header, text = "Settings", font = ("Raleway", 32), fg="light gray", bg="sienna4")
        settings_label.place(relx=.5,rely=.5,anchor=CENTER)
        # Placing button into the top section of settings page
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        # Create back button
        back_arrow = customtkinter.CTkButton(
        settings_header,
        fg_color="sienna3",
        width=50,
        height=50,
        border_width=0,
        corner_radius=10,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)
        # Create interface section
        interface_sec = customtkinter.CTkFrame(self, width=300, height=300,fg_color='sienna4')
        interface_sec.place(relx=0.5,x=-150 ,y=150)
        # Create volume section
        volume_sec = customtkinter.CTkFrame(self, width=300, height=300,fg_color='sienna4')
        volume_sec.place(relx=0.5,x=-150,y=460)

        self.setup_interfacesec(interface_sec)
        self.volume_labels(volume_sec)
        self.music_slider(volume_sec)
        self.sfx_slider(volume_sec)
    

    # Set up interface section
    def setup_interfacesec(self, interface_sec):
        self.current_theme = tk.StringVar(value='Light')
        # Create interface section label
        int_lbl = customtkinter.CTkLabel(
            master=interface_sec,
            text="Interface Settings",
            text_font=('Raleway 22'))
        int_lbl.place(x=50,y=40)
        # Create interface radio buttons
        light_mode_btn = customtkinter.CTkRadioButton(
            master=interface_sec,
            fg_color="sienna3",
            text="Light Mode",
            command= lambda: self.change_theme("light_mode"),
            variable=self.current_theme,
            value="Light",
        )
        light_mode_btn.place(x=50,y=110)
        
        dark_mode_btn = customtkinter.CTkRadioButton(
            master=interface_sec,
            fg_color="sienna3",
            text="Dark Mode",
            command= lambda: self.change_theme("dark_mode"),
            variable=self.current_theme,
            value="Dark",
        )
        dark_mode_btn.place(x=50,y=160)
        
        tan_mode_btn =  customtkinter.CTkRadioButton(
            master=interface_sec,
            fg_color="sienna3",
            text=" Tan Mode",
            command= lambda: self.change_theme("tan_mode"),
            variable=self.current_theme,
            value="Tan",
        )
        tan_mode_btn.place(x=50,y=210)

    # Apply themes to radio buttons
    def change_theme(self,theme):
        print("button toggled" + self.current_theme.get())
        self.current_theme.set(self.current_theme.get())
        user_settings["theme"]=theme_diction[str(theme)]
        print(user_settings)

    # Create volume section labels
    def volume_labels(self, volume_sec):
        vol_lbl = customtkinter.CTkLabel(
            master=volume_sec,
            text="Volume Settings",
            text_font=('Raleway 22'))
        vol_lbl.place(x=65,y=40)
        
        mus_lbl = customtkinter.CTkLabel(
            master=volume_sec,
            text="Music:",
            text_font=('Raleway 12'))
        mus_lbl.place(x=5, y=110)
        
        sfx_lbl = customtkinter.CTkLabel(
            master=volume_sec,
            text="Sound FX:",
            text_font=('Raleway 12'))
        sfx_lbl.place(x=20, y=185)
    
    def music_slider(self, volume_sec):
        # Connect music slider to channel 1
        def volume(self):
            val = round(slider.get()/100,1)
            print(val)
            channel1.set_volume(val)
            print("MUSIC VOLUME:"+str(channel1.get_volume()))
            return
        # Create music slider
        slider = customtkinter.CTkSlider(
        volume_sec,
        width=230,
        height=25,
        border_width=5.5,
        from_=0,
        to=100,
        fg_color="sienna3",
        button_color="SlateBlue2",
        command=volume)
        self.slider = slider
        slider.place(relx=0.5, rely=0.5, anchor=CENTER)

    def sfx_slider(self, volume_sec):
        # Connect sfx slider to channel 2
        def volume(self):
            val = round(slider.get()/100,1)
            print(val)
            channel2.set_volume(val)
            print("SFX VOLUME:"+str(channel2.get_volume()))
            return
        # Create sfx slider
        slider = customtkinter.CTkSlider(
        volume_sec,
        width=230,
        height=25,
        border_width=5.5,
        fg_color="sienna3",
        button_color="SlateBlue2",
        from_=0,
        to=100,
        command= volume)
        slider.place(relx=0.5, rely=0.5,y=75, anchor=CENTER)



class library_page(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        # Top portion of the settings page
        library_header = Frame(self, bg="sienna4", width=1200,height=100)
        library_label = Label(library_header, text = "Library", font = ("Raleway", 32), fg="light gray", bg="sienna4")
        library_label.pack(anchor=CENTER,fill="none",expand=False)
        library_label.place(relx=.5,y=50,anchor=CENTER)
        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)

        refresh_img = PhotoImage(file="ereadpngs/free-refresh-icon-3104-thumb.png")

        back_arrow = customtkinter.CTkButton(
        library_header,
        fg_color="sienna3",
        width=50,
        height=50,
        border_width=0,
        corner_radius=10,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side=LEFT,expand=False,pady=25,padx=25)
        library_header.pack(fill=BOTH)

        to_configure = customtkinter.CTkButton(
            library_header,
            width=55,height=50,fg_color="sienna3",
            border_width=0, corner_radius=10,
            text="Configure Books",
            command = lambda: controller.show_frame(Configure)
        )
        to_configure.pack(side=LEFT,expand=False,pady=25,padx=10)
        
        refresh_button = customtkinter.CTkButton(
            library_header,
            width = 50,
            height = 50,
            border_width=0,
            fg_color="sienna3",
            corner_radius=10,
            image=refresh_img,
            text='',
            command = lambda: self.render_books()
        )
        refresh_button.pack(side=RIGHT, expand=False,pady=25,padx=25)


        # Creating the canvas
        self.scrollable_canvas = Canvas(self)
        self.scrollable_canvas.config(width=950, height = 4000)
        self.scrollable_canvas.place(relx=.5)
        self.scrollable_canvas.pack(side=LEFT,fill="y",expand=1)

        # Creating a scrollbar
        library_scrollbar = Scrollbar(self, orient = VERTICAL, command = self.scrollable_canvas.yview)
        library_scrollbar.pack(side = RIGHT, fill = Y)

        # Configuring Canvas with scrollbar
        self.scrollable_canvas.configure(yscrollcommand=library_scrollbar.set)

        # Binding configure
        self.scrollable_canvas.bind('<Configure>', lambda e: self.scrollable_canvas.configure(scrollregion = self.scrollable_canvas.bbox("all")))

        # Creating another frame inside canvas
        self.canvas_frame = Frame(self.scrollable_canvas,bg='wheat1')
        self.canvas_frame.bind("<Configure>", self.reset_scrollregion)

        # adding new frame to window in canvas
        self.scrollable_canvas.create_window((0,125), window=self.canvas_frame, anchor="nw")

        # Renders all books into the canvas
        
        self.render_books()

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            fg_color="sienna3",
            border_width=0,
            corner_radius=10,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)
    
    def reset_scrollregion(self, event):
        self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all"))

    def action(self, item):
        temp = book_library.loc[book_library['Title'] == item]
        #temp['Cover'].item()
        
        logo = Image.open(temp['Cover'].item())
        
        logo = logo.resize((170,280))
        logo = ImageTk.PhotoImage(logo)
            
        return customtkinter.CTkButton(self.canvas_frame,width=200,height=300,border_width=0, 
        corner_radius=10,image = logo, text = '',command = lambda: self.func(item), fg_color = "sienna3"
        )
    def name(self, item):
        return customtkinter.CTkLabel(self.canvas_frame, width=196, height=30,text=item, text_font= ("Railway",12),corner_radius=0,fg_color='sienna3')

    def func(self, item):
        create_book(item,'on','',self.scrollable_canvas)

    def render_books(self):
        rows = 0
        columns = 0
        col_adv = 0
        for i, item  in enumerate(book_library['Title']):
            b = self.action(item)
            c = self.name(item)
                #create_book(item,'on','',tk.Frame)
                #btn2.pack(side="right")
                # if line % 5 == 0:
                
                # First 3 buttons should be placed in (0,0),(0,1),(0,2)
            b.grid(row = rows, column = columns, padx = 20, pady = 10)

            c.grid(row = rows, column = columns)
                # Then condition hits and then the next set of buttons should be placed in 
                # (1,0),(1,1),(1,2), and so forth for every 3 or 4 buttons
            print("("+str(rows)+","+str(columns)+")")
            if columns % 3 == 0 and columns > 0:
                rows += 1
                columns=-1
            if columns != 3:
                columns+=1

    def refresh_library(self):
        self.render_books() 

class Configure(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        # self.all_books_in_df = book_library["Title"].tolist() # getting all book names in book_library df so we can display it for configuring
        configure_header = Frame(self, width=1200,height=100,bg="sienna4")
        configure_label = Label(configure_header, text = "Configure Books", font = ("Raleway", 32), fg="light gray", bg="sienna4")
        configure_label.pack(anchor=CENTER,fill="none",expand=False)
        configure_label.place(relx=.5,y=50,anchor=CENTER)
        refresh_img = PhotoImage(file="ereadpngs/free-refresh-icon-3104-thumb.png")
        
        to_library = customtkinter.CTkButton(
            configure_header,
            width=50,
            height=50,
            border_width=0,
            fg_color="sienna3",
            corner_radius=10,
            text = 'To Library',
            command= lambda: controller.show_frame(library_page)
        )
        to_library.pack(side=LEFT,expand=False,pady=25,padx=10)

        to_main = customtkinter.CTkButton(
            configure_header,
            width=50,height=50,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            text = 'To Main Menu',
            command = lambda: controller.show_frame(main_menu)
        )
        to_main.pack(side=LEFT,expand=False,pady=25,padx=10)

        refresh_button = customtkinter.CTkButton(
            configure_header,
            width = 50,
            height = 50,
            border_width=0,
            corner_radius=10,
            fg_color="sienna3",
            image=refresh_img,
            text='',
            command = lambda: self.render_all_stories()
        )
        refresh_button.pack(side=RIGHT, expand=False,pady=25,padx=25)

        configure_header.pack(fill=BOTH)

        self.render_all_stories()

        configure_selected_story_btn = customtkinter.CTkButton(
            self,
            width=25,height=50,
            border_width=0,corner_radius=10,
            fg_color="sienna3",
            command = lambda: (self.configure_story_song(self.Storylistbox.get(self.Storylistbox.curselection())),self.configure_story_sound(self.Storylistbox.get(self.Storylistbox.curselection()))),
            text="Configure Selected Book",
            text_font=("Raleway",15)
        )
        configure_selected_story_btn.place(relx=.04,rely=.75)

        self.story_length_lbl_songs = Label(self,fg="sienna4",bg="wheat1")
        self.story_length_lbl_sounds = Label(self,fg="sienna4",bg="wheat1")
        self.page_warning_or_success = Label(self,fg="sienna4",bg="wheat1")
        self.song_warning_or_success = Label(self,fg="sienna4",bg="wheat1")

        self.story_length_lbl_songs.place(relx=.4,rely=.35)
        self.story_length_lbl_sounds.place(relx=.72,rely=.35)
        self.page_warning_or_success.place(relx=.68,rely=.7)
        self.song_warning_or_success.place(relx=.4,rely=.66)

        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            border_width=0,
            fg_color="sienna3",
            corner_radius=10,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)
    
    def render_all_stories(self):
        self.all_books_in_df = book_library["Title"].tolist()
        all_storys_configurable = Label(self, text="All Stories", bg='wheat1', font=("Raleway",20),  fg='sienna4')
        all_storys_configurable.place(relx=.01,rely=.35)
        self.Storylistbox = Listbox(self,width=30,height=15,background="sienna4", selectmode=BROWSE)
        self.Storylistbox.place(relx=.01,rely=.4)
        for i,story in enumerate(self.all_books_in_df):
            self.Storylistbox.insert(i,story)

    def configure_story_song(self,listbox_selection):
        # Need to get the length of the book somehow? 
        # display number of pages
        # Display from entry box
        # Display to entry box
        # display listbox of all songs.
        # Get the starting index from the "from entry box"
        # Get the ending index from the "to entry box"
        # update the audio_map with the from-to by indexing with book name
        # save the information into song config csv
        
        self.story_name = listbox_selection
        self.length_of_story = len(self.get_book_length(self.story_name))

        story_length_stringvar = StringVar()
        story_length_stringvar.set(f'{self.story_name}\'s number of pages: {self.length_of_story}')
        self.story_length_lbl_songs.config(text=story_length_stringvar.get())

        self.start_index_label = Label(self,text="From page:",fg="sienna4",bg="wheat1")
        self.start_index_label.place(relx=.3,rely=.38)
        self.start_index_stringvar = IntVar()
        self.start_index_stringvar.set(1)
        self.start_index = Entry(self, textvariable=self.start_index_stringvar,bg="sienna4")
        self.start_index.place(relx=.37,rely=.38)
        
        self.end_index_label = Label(self,text="To page:",fg="sienna4",bg="wheat1")
        self.end_index_label.place(relx=.3,rely=.42)
        self.end_index_stringvar = IntVar()
        self.end_index_stringvar.set(1)
        self.end_index = Entry(self,textvariable=self.end_index_stringvar,bg="sienna4")
        self.end_index.place(relx=.37,rely=.42)

        self.select_a_song = Label(self,text="Select a Song!",font=("Raleway",15),fg="sienna4",bg="wheat1")
        self.select_a_song.place(relx=.3,rely=.46)
        self.all_songs_listbox = Listbox(self,width=50,height=5,bg="sienna4", selectmode=BROWSE)
        self.all_songs_listbox.place(relx=.3,rely=.5)
        for i,song in enumerate(music.files):
            self.all_songs_listbox.insert(i,song)

        submit_song_config = customtkinter.CTkButton(
            self,
            width=15,height=10,
            fg_color="sienna3",
            border_width=0,corner_radius=10,
            command = lambda: self.add_song_to_book(
                self.start_index_stringvar.get(),
                self.end_index_stringvar.get(),
                self.all_songs_listbox.get(self.all_songs_listbox.curselection())
            ),
            text="Configure Song",
            text_font=("Raleway",12)
        )
        submit_song_config.place(relx=.27,rely=.63)

        remove_song_config = customtkinter.CTkButton(
            self,
            width = 15, height = 10,
            border_width= 0, corner_radius= 10,fg_color="sienna3",
            command = lambda: self.remove_song_from_pages(
                self.start_index_stringvar.get(),
                self.end_index_stringvar.get(),
                self.story_name
            ),
            text="Remove Song from Pages",
            text_font=("Raleway",12)
        )
        remove_song_config.place(relx=.39,rely=.63)

    def configure_story_sound(self,listbox_selection):
        # For sound config
        # Display page num entry box
        # Since user can only use one sound on page
        # display listbox of all sounds
        # have user enter what page they want to put a sound on.
        # sanity check if the entered number is not greater or negative than the length of the pages
        # sanity check if the entry is not a number
        # have user select a sound
        # map the number to sound in sound_library using sound listbox selection and listbox_selection param, save the sound_library to local file using user_sound_map class
        self.story_name = listbox_selection
        self.length_of_story = len(self.get_book_length(self.story_name))
        story_length_stringvar = StringVar()
        story_length_stringvar.set(f'{self.story_name}\'s number of pages: {self.length_of_story}')
        self.story_length_lbl_sounds.config(text=story_length_stringvar.get())

        sound_per_page_warning = Label(self,text="Only ONE sound can be linked to an individual page.",fg="sienna4",bg="wheat1")
        sound_per_page_warning.place(relx=.7,rely=.38)

        self.page_warning_stringvar = StringVar()
        self.page_warning_song_stringvar = StringVar()

        self.which_page_lbl = Label(self,text="Page # : ",fg="sienna4",bg="wheat1")
        self.which_page_lbl.place(relx=.7,rely=.42)
        self.which_page_stringvar = IntVar()
        self.which_page_stringvar.set(1)
        self.which_page = Entry(self,textvariable=self.which_page_stringvar,bg="sienna4")
        self.which_page.place(relx=.75,rely=.42)

        self.select_a_sound = Label(self,text="Select a Sound!",font=("Raleway",15),fg="sienna4",bg="wheat1")
        self.select_a_sound.place(relx=.7,rely=.46)

        self.all_sounds_listbox = Listbox(self,width=50,height=5,bg="sienna4", selectmode=BROWSE)
        self.all_sounds_listbox.place(relx=.7,rely=.5)
        for i,sound in enumerate(soundFiles.sounds):
            self.all_sounds_listbox.insert(i,sound)
        
        submit_sound_config = customtkinter.CTkButton(
            self,
            width=15,height=10,fg_color="sienna3",
            border_width=0,corner_radius=10,
            command = lambda: self.add_sound_to_page(
                self.which_page_stringvar.get(),
                self.all_sounds_listbox.get(self.all_sounds_listbox.curselection())
            ),
            text="Configure Sound",
            text_font=("Raleway",12)
        )
        submit_sound_config.place(relx=.68,rely=.63)

        remove_sound_config = customtkinter.CTkButton(
            self,
            width=15,height=10,fg_color="sienna3",
            border_width=0,corner_radius=10,
            command = lambda: self.remove_sound_from_page(
                self.which_page_stringvar.get()
            ),
            text="Remove Sound from Page",
            text_font=("Raleway",12)
        )
        remove_sound_config.place(relx=.81,rely=.63)

    def add_song_to_book(self,start_index,end_index,song):
        global audio_map
        '''
        Takes information from the configure_story_song function and adds the necessary song to the audio_map dataframe. I think that the user added stories should automatically be added
        as columns to the audio_map dataframes and sound_map dataframes
        '''
        if start_index > end_index:
            self.page_warning_song_stringvar.set("First page Cannot be higher than the last page for config!")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get(), fg="red",font=("Raleway",9))
        if start_index < 0 or end_index > self.length_of_story:
            self.page_warning_song_stringvar.set("The first page CANNOT be less than 0.\nThe ending page CANNOT be higher than the length of the book.")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get(), fg="red",font=("Raleway",9))
        elif start_index == end_index:
            self.page_warning_song_stringvar.set("Song has been successfuly configured!")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get())
            audio_map.loc[start_index:end_index, self.story_name] = song
            user_songs_map.set_user_audio_config()
            user_songs_map.save_audio_config()

        elif start_index >= 0 and end_index <= self.length_of_story:
            for i in range(start_index,end_index + 1):
                audio_map.loc[i, self.story_name] = song
            self.page_warning_song_stringvar.set("Song has been successfully configured!")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get())
            user_songs_map.set_user_audio_config()
            user_songs_map.save_audio_config()
        
    
    def add_sound_to_page(self,page_number,sound):
        global sound_effects_map

        if page_number < -1 or page_number > self.length_of_story:
            self.page_warning_stringvar.set("Page number cannot be less than 0 OR greater than the length of the book!")
            self.page_warning_or_success.config(text=self.page_warning_stringvar.get(), fg="red",font=("Raleway",8))
            self.page_warning_or_success.place(relx=.65,rely=.7)
        else:
            self.page_warning_stringvar.set(f'Sound has been added to page {page_number}!')
            self.page_warning_or_success.config(text=self.page_warning_stringvar.get(), font=("Raleway",12))
            self.page_warning_or_success.place(relx=.73,rely=.7)
            sound_effects_map.loc[page_number, self.story_name] = sound
            # after adding the new sound to the sound_effects_map, set the copy in the user_sound_file class and SAVE
            user_sounds_map.set_user_sound_config()
            user_sounds_map.save_sound_config()
            

    def remove_sound_from_page(self,page_number):
        global sound_effects_map

        if page_number < -1 or page_number > self.length_of_story:
            self.page_warning_stringvar.set("Page number cannot be less than 0 OR greater than the length of the book!")
            self.page_warning_or_success.config(text=self.page_warning_stringvar.get(), fg="red",font=("Raleway",8))
        else:
            self.page_warning_stringvar.set(f'Sound successfully removed from page {page_number}')
            self.page_warning_or_success.config(text=self.page_warning_stringvar.get(),font=("Raleway",9))
            sound_effects_map.loc[page_number,self.story_name] = "None"
            user_sounds_map.set_user_sound_config()
            user_sounds_map.save_sound_config()
            print("Sound has been removed!")

    def remove_song_from_pages(self,start,end, book):
        global audio_map
        if start > end:
            self.page_warning_song_stringvar.set("First page Cannot be higher than the last page for config!")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get(), fg="red",font=("Raleway",9))
        if start < 0 or end > self.length_of_story:
            self.page_warning_song_stringvar.set("The first page CANNOT be less than 0.\nThe ending page CANNOT be higher than the length of the book.")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get(), fg="red",font=("Raleway",9))
        elif start == end:
            self.page_warning_song_stringvar.set("Song has been successfuly removed!")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get())
            audio_map.loc[start:end, book] = "None"
            user_songs_map.set_user_audio_config()
            user_songs_map.save_audio_config()
        elif start >= 0 and end <= self.length_of_story:
            for i in range(start,end):
                audio_map.loc[i, book] = "None"
            self.page_warning_song_stringvar.set("Song has been successfully removed!")
            self.song_warning_or_success.config(text=self.page_warning_song_stringvar.get())
            user_songs_map.set_user_audio_config()
            user_songs_map.save_audio_config()
        
    def get_book_length(self,book):
        diction = {}
        i = 0
        for row in book_library['Title']:
            diction[book_library['Title'][i]] = i
            i+=1
        index = diction[book]
        # The line below is how the book is found in the dictionary. vl
        if book_library['URL'][index][0] == 'h':
            story = self.get_from_library('url',target_url = book_library['URL'][index]) 
        elif book_library['URL'][index][-1] == 't':
            story = self.get_from_library('file',target_url = book_library['URL'][index]) 
        elif book_library['URL'][index][-1] == 'f':                                                                                                                                                                                                                   
            story = self.read_user_story(book_library['URL'][index])
            
        if book != "The Raven":
            story = self.split_function(story)
        else:
            print('working')
        final_pages=story.split('---split---') #this is the page splitting decider.
        # We will either need to write a function to change pdfs into txt files
        return final_pages
    
    def get_from_library(self,file_url,target_url):
        '''
        This function finds the url to our database in github.
        '''
        if file_url == "file":
            response  = open(target_url,encoding="utf-8")
            #read whole file to a string
            data = response.read()
            
            response.close()   
        else:
            response = requests.get(target_url)
            data = response.text
        return(data)

    def read_user_story(self, file_path): # !IMPORTANT
        processed = []
        pdf_str = ''
        if file_path[-4:] == ".pdf":
            pdf = pdfplumber.open(file_path)
            for i in range(len(pdf.pages)):
                processed.append(pdf.pages[i])
            for page in processed:
                pdf_str += page.extract_text()
            return pdf_str
    
    def split_function(self,story):
        story = story.splitlines(True)
        if len(story[1]) > 20:
            new_story = ''
            i = 0
            n=0
            for line in story:
                i = 0
                for word in line.split(' '):
                    if i == 11:
                        new_story += '\n'
                        i=0
                    else:
                        new_story+=word+' '
                    i+=1
            story = new_story.splitlines()

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

class FAQ(tk.Frame):
     def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg='wheat1')
        faq_header = Frame(self, width=1200,height=100,bg='sienna4')
        faq_label = Label(faq_header, text = "Frequently Asked Questions", font = ("Raleway", 32),fg="light gray", bg='sienna4')
        faq_label.pack(anchor=CENTER,fill="none",expand=False)
        faq_label.place(relx=.5,y=50,anchor=CENTER)

        back_arrow_img = PhotoImage(file="ereadpngs/chevron-left.png")
        back_arrow_img = back_arrow_img.subsample(15)
        back_arrow = customtkinter.CTkButton(
        faq_header,
        width=50,
        height=50,
        fg_color="sienna3",
        border_width=0,
        corner_radius=10,
        image=back_arrow_img,
        text = '',
        command= lambda: controller.show_frame(main_menu)
        )
        back_arrow.pack(side="left")
        back_arrow.place(x=50, y= 50, anchor=W)

        faq_header.pack(fill=BOTH)
    
        mute_btn = customtkinter.CTkButton(
            self,
            width=25,
            height=25,
            fg_color="sienna3",
            border_width=0,
            corner_radius=100,
            text="Mute Music",
            command = lambda: controller.mute_bg_music()
        )
        mute_btn.place(relx=0,rely=.97)
    

    
class Book:
    def __init__(self,book_title, sound,theme,window):
        #self.window = window
        self.window = window
        self.book_title = book_title
        self.sound = sound
        self.theme = theme
        self.status = 'play'
        self.frame_4_1 =None
        self.frame_4 = None
        self.frame_3 = None
        self.canvas = None
        self.canvas_2 = None
        self.canvas_3 = None
        self.info = None
        self.music_info = None
        self.advbutton = None
        self.backbutton = None
        self.mute = None
        self.volup = None
        self.slider = None
        self.search_button = None
        self.search_directions = None
        self.bookmark1 = None
        self.bookmark2 = None
        if __name__ == "__main__":
            self.main_book_run()

    def sound_switch(self,var):
        if var == "off":
            self.sound = var
            channel2.pause()
            channel1.pause()
        elif var == 'on':
            self.sound = var
            channel2.unpause()
            channel1.unpause()
        return

    def sound_switch_button(self,window):
        photo = PhotoImage(file = 'ereadpngs/mute.png')
        btn2 = customtkinter.CTkButton(window,  width=45,height=45,border_width=0, 
        corner_radius=8,text = '',image = photo,text_color='black', fg_color=user_settings["theme"][2],
        command = lambda: self.sound_switch('off')
        )
        self.mute = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=300,x=270, anchor=CENTER)
        return
    
    def sound_switch_button2(self,window):
        photo = PhotoImage(file = 'ereadpngs/volume.png')
        btn2 = customtkinter.CTkButton(window, width=45,height=45,border_width=0,
        corner_radius=8,text = '',image = photo,text_color='black',fg_color=user_settings["theme"][2],
        command = lambda: self.sound_switch('on')
        )
        self.volup = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=300,x=550, anchor=CENTER)
        return

    def get_from_library(self,file_url,target_url):
        '''
        This function finds the url to our database in github.
        '''
        if file_url == "file":
            response  = open(target_url,encoding="utf-8")
            #read whole file to a string
            data = response.read()
            
            response.close()   
        else:
            response = requests.get(target_url)
            data = response.text
        return(data)

    def read_user_story(self, file_path): # !IMPORTANT
        # ask rich if he knows how to process pdf files or txt files. How can we know when there is a next page, especially for pdf files, Important for reading pdf files.
        # semi works
        processed = []
        extracted = []
        pdf_str = ''
        if file_path[-4:] == ".pdf":
            pdf = pdfplumber.open(file_path)
            for i in range(len(pdf.pages)):
                processed.append(pdf.pages[i])
            for page in processed:
                pdf_str += page.extract_text()
            return pdf_str
        

    def music(self,n,song):
        if n == 1 and song != 'None':
            if song.startswith("C:"):
                song = pygame.mixer.Sound(song)
            elif "ereadmp3/" not in song:
                song = pygame.mixer.Sound("ereadmp3/"+song)
            else:
                song = pygame.mixer.Sound(song)
            channel1.play(song,loops=3000)
        elif self.status == "paused":
            channel1.unpause()
        else:
            i = 'do nothing'

    def sound_effects(self,n,sound):
        if n == 1:
            if sound.startswith("C:"):
                sound = pygame.mixer.Sound(sound)
            elif "ereadSounds" not in sound:
                sound = pygame.mixer.Sound("ereadSounds/"+sound)
            else:
                sound = pygame.mixer.Sound(sound)
            channel2.play(sound,loops=0)
        elif self.status == "paused":
            channel2.unpause()
        else:
            i = 'do nothing'


    def music_player(self,window,title):
        #if title != 'continue':
        #   music(0,title)
        #   return
        if title in audio_map:
            if window.counter >= len(audio_map[title]):
                song = prev_song[0]
            else:
                song = audio_map[title].iloc[(window.counter)]
        else:
            song = audio_map["The Raven"][1]
            
        if title in sound_effects_map.columns and window.counter < len(sound_effects_map[title]) and  sound_effects_map[title].iloc[(window.counter)] != 'None':
            print(sound_effects_map[title].iloc[(window.counter)])
            self.sound_effects(1,sound_effects_map[title].iloc[(window.counter)])
        print(song)
        if self.sound == 'off':
            #do nothing
            self.status = 'paused'
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
        # The line below is how the book is found in the dictionary. vl
        if book_library['URL'][index][0] == 'h':
            story = self.get_from_library('url',target_url = book_library['URL'][index]) 
        elif book_library['URL'][index][-1] == 't':
            story = self.get_from_library('file',target_url = book_library['URL'][index]) 
        elif book_library['URL'][index][-1] == 'f':                                                                                                                                                                                                                   
            story = self.read_user_story(book_library['URL'][index])
            
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
        channel2.fadeout(5)
        print(self.sound)
        pages_total = len(final_pages)
        if forward_back == "back" and window.counter > 0:
            window.counter -= 1
        if forward_back == "adv" and window.counter != len(final_pages):
            window.counter += 1
        moderator = len(final_pages) <= window.counter
        if moderator == False:
            self.music_player(window,title)
        if self.canvas_2 != None:
            self.canvas_2.destroy()
        self.canvas_2 = Canvas(bg=user_settings["theme"][1], width=595, height=770)
        self.canvas_2.place(relx=.5, rely=.5,x=-60,anchor=CENTER)
        self.canvas_2.config(highlightthickness=0)
        self.music_information(window)
        self.information(pages_total,window)
        text = self.canvas_2.create_text(30, 20, text=str(window.counter) if moderator == False else self.thanks(), fill="black", font=('Times 16'),width=540, )
        text = self.canvas_2.create_text(300, 400, text=final_pages[window.counter] if moderator == False else self.thanks(), fill="black", font=('Times 16'),width=540, anchor=CENTER)

    def thanks(self):
        '''
        Currently the last page of the book. It just prints thank you.
        '''
        self.music(0,'none')
        if self.canvas_3 != None:
            self.canvas_3.destroy()
        self.canvas_3 = Canvas(bg=user_settings["theme"][1], width=595, height=770)
        self.canvas_3.place(relx=.5, rely=.5,x=-60, anchor=CENTER)
        self.canvas_3.config(highlightthickness=0)
        text = self.canvas_3.create_text(300, 400, text="Thank you For Reading", fill="black", font=('Times 25'),width=430)
        text = self.canvas_3.create_text(300, 550, text="Music by Eric Matyas\nwww.soundimage.org", fill="black", font=('Times 18'),width=430)


    def information(self,pages_total,window):
        '''
        Information on book
        '''
        temp = book_library.loc[book_library['Title'] == self.book_title]
        #temp['Cover'].item()
        if self.info!= None:
            self.info.destroy()
        self.info = customtkinter.CTkLabel( window,width=225, height=500,text_color='black',text="Title:\n"+self.book_title+"\n\nAuthor:\n"+temp['Author'].item()+"\n\nYear:\n"+ str(temp['Year Published'].item())+"\n\nGenre:\n"+str(temp['Genre'].item())+"\n\n"+"Page Count: \n"+str(pages_total), text_font= ("Railway",14),fg_color=user_settings["theme"][1])
        self.info.place(relx=.5, rely=.5,x=465,y=-100, anchor=CENTER)
        self.info.config(highlightthickness=0,)

    def music_information(self,window):
        '''
        Information on song
        '''
        title = self.book_title
        if title in audio_map:
            if window.counter >= len(audio_map[title]):
                song = prev_song[0]
            else:
                song = audio_map[title].iloc[(window.counter)]
        else:
            song = audio_map["The Raven"][1]
        if self.music_info != None:
            self.music_info.destroy()
        self.music_info = customtkinter.CTkLabel( window,width=280, height=80,text_color='black',text="Song Title: "+song+"\nBy: Eric Matyas\nwww.soundimage.org",fg_color=user_settings["theme"][1])
        self.music_info.place(relx=.5, rely=.5,x=410,y=230, anchor=CENTER)
        self.music_info.config(highlightthickness=0)

    def menu_bar(self,window,final_pages):
        frame_4 = customtkinter.CTkFrame( window,width=80, height=500,fg_color=user_settings["theme"][1])
        frame_4.place(rely=.5, anchor=W)
        frame_4.configure()
        self.library_button(frame_4)
        self.find_button(frame_4,window,final_pages)
        self.settings_button(frame_4,window)
        self.upload_button(frame_4)
        frame_4.tkraise()
        self.frame_4_1 = frame_4
    
    def library_return(self):
        self.mute.destroy()
        self.volup.destroy()
        self.slider.destroy()
        self.advbutton.destroy()
        self.backbutton.destroy()
        self.frame_3.destroy()
        self.frame_4.destroy()
        self.canvas.destroy()
        if self.canvas_2 != None:
            self.canvas_2.destroy()
        if self.canvas_3 != None:
            self.canvas_3.destroy()
        channel1.stop()
        channel2.stop()

    def finder(self,window,final_pages):
        if self.search_button != None:
                self.search_button.destroy()
        if self.search_directions != None:
            self.search_directions.destroy()
        self.page_name = tk.IntVar()
        title_entry = Entry(window,width=3, textvariable= self.page_name)
        directions = Label(text="Select the go button\nto jump.", font=("Raleway",10))
        title_entry.pack(side="right")
        title_entry.place(relx=.5, rely=.5,x= -480, y=-180, anchor=CENTER)
        directions.place(relx=.5, rely=.5,x= -450, y=-210, anchor=CENTER)
        btn = customtkinter.CTkButton(width=40,height=20,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = 'Go',text_color='black',
        command = lambda: self.page_jump(title_entry,window,final_pages) 
        )
        self.search_button = btn
        self.search_directions= directions
        btn.place(relx=.5, rely=.5,x= -420, y=-180, anchor=CENTER)
        print(title_entry.get())
        #window.counter = int(title_entry.get())

    def page_jump(self, val, window,final_pages):
        window.counter = int(val.get())-1
        adv = 'adv'
        self.pages(window,final_pages,adv,self.book_title)
        

    def settings_link(self,window):
        if self.bookmark1 != None:
            self.bookmark1.destroy()
        if self.bookmark2 != None:
            self.bookmark2.destroy()
        df = pd.read_csv('ereadbookmarks/bookmarks.csv')
        if self.book_title in df.columns:
            directions2 = Label(text="You left off on page "+str(df.iloc[0][self.book_title].item())+'.', font=("Raleway",10))
            directions2.place(relx=.5, rely=.5,x= -440, y=60, anchor=CENTER)
        df[self.book_title] = window.counter
        #df = df.to_csv(index=False)
        #os.makedirs('/ereadbookmarks', exist_ok=True)  
        df.to_csv('ereadbookmarks/bookmarks.csv') 
        
        directions1 = Label(text="Page "+str(df.iloc[0][self.book_title].item())+" Bookmarked!", font=("Raleway",10))
        directions1.place(relx=.5, rely=.5,x= -440, y=80, anchor=CENTER)
        self.bookmark2 = directions1
        self.bookmark1= directions2


        
    def upload_link(self):
        exit()

    def find_button(self,frame,window,final_pages):
        photo = PhotoImage(file = 'ereadpngs/book-research.png')
        btn2 = customtkinter.CTkButton(master = frame, width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.finder(window,final_pages)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-180, anchor=CENTER)

    def library_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/home.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.library_return()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=-60, anchor=CENTER)

    def upload_button(self,frame):
        photo = PhotoImage(file = 'ereadpngs/exit.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.upload_link()
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=180, anchor=CENTER)

    def settings_button(self,frame,window):
        photo = PhotoImage(file = 'ereadpngs/bookmark.png')
        btn2 = customtkinter.CTkButton(master = frame,width=200,height=80,border_width=2,fg_color=("white", user_settings["theme"][1]),
        corner_radius=8,text = '',image = photo,text_color='black',
        command = lambda: self.settings_link(window)
        )
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,y=60, anchor=CENTER)
    
    
    def vol_slider(self,window):
        def volume(self):
            val = round(slider.get()/100,1)
            print(val)
            channel1.set_volume(val)
            channel2.set_volume(val)
            return

        slider = customtkinter.CTkSlider(
        window,
        width=230,
        height=25,
        border_width=5.5,
        from_=0,
        to=100,
        fg_color=user_settings["theme"][2],
        button_color=user_settings["theme"][1],
        command=volume)
        self.slider = slider
        slider.place(relx=0.5, rely=0.5,x=410,y=300, anchor=CENTER)
        
    def adv_button(self,window,final_pages,title):
        photo = PhotoImage(file = 'ereadpngs/chevron-right.png')
        photo = photo.subsample(15)
        adv = "adv"
        btn2 = customtkinter.CTkButton(
        window,
        width=80,
        height=80,
        border_width=0,
        corner_radius=8,
        text = '',
        image = photo,
        text_color='black',
        fg_color=user_settings["theme"][2],
        border_color="dark slate gray",
        command = lambda: self.pages(window,final_pages,adv,title)
        )
        self.advbutton = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=290, anchor=CENTER)

    def back_button(self,window,final_pages,title):
        photo = PhotoImage(file = 'ereadpngs/chevron-left.png')
        photo = photo.subsample(15)
        back = "back"
        btn2 = customtkinter.CTkButton(
        window,
        width=80,
        height=80,
        border_width=0,
        corner_radius=8,
        fg_color=user_settings["theme"][2],
        text = '',
        image = photo,
        text_color='black',
        command = lambda: self.pages(window,final_pages,back,title)
        )
        self.backbutton = btn2
        btn2.pack(side="right")
        btn2.place(relx=.5, rely=.5,x=-410, anchor=CENTER)

    def split_function(self,story):
        story = story.splitlines(True)
        if len(story[1]) > 12:
            print('got it')
            new_story = ''
            i = 0
            n=0
            for line in story:
                i = 0
                for word in line.split(' '):
                    if i == 11:
                        new_story += '\n'
                        i=0
                    else:
                        new_story+=word+' '
                    i+=1
            story = new_story.splitlines()

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

    def main_book_run(self):
        ''' 
        Creates the window, and calls this diction function to get a key value pair linked by page number.
        Currently only supports .txt files because pdf files lack the functionality 
        to be manipulated and most domain stories use .txt or .epub not pdf.
        '''
        bg_music_channel.pause()
        frame_3 = Frame(width=10000, height=10000)
        frame_3.place(relx=.5, rely=.5, anchor=CENTER)
        frame_3.configure()
        frame_3.tkraise()
        self.frame_3 = frame_3
        frame_4 = customtkinter.CTkFrame(width=1200, height=800,fg_color = user_settings["theme"][0],corner_radius=0)
        frame_4.place(relx=.5, rely=.5, anchor=CENTER)
        frame_4.configure()
        frame_4.tkraise()
        #customtkinter.set_default_color_theme("darkblue")
        
        self.frame_4 = frame_4
        window = frame_4
        window.counter = -1 #this is universal counter funtion that allows a user to traverse a story.
        pygame.mixer.music.pause()
        final_pages, title = self.diction(self.book_title)
        self.vol_slider(window)
        self.adv_button(window, final_pages, title)
        self.back_button(window, final_pages, title) 
        self.sound_switch_button(window)
        self.sound_switch_button2(window)
        self.music(0,'none')
        self.canvas = Canvas(bg="dark gray", width=595, height=770)
        self.canvas.place(relx=.5, rely=.5,x=-60, anchor=CENTER)
        self.canvas.config(highlightthickness=0)
        temp = book_library.loc[book_library['Title'] == self.book_title]
        logo = Image.open(temp['Cover'].item())
        logo = logo.resize((595,770))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self.canvas,image=logo)
        logo_label.image = logo
        logo_label.place(relx=.5, rely=.5, anchor= CENTER)
        #canvas.create_text(300, 400, text="Good Luck On Your Fictional Journey!", fill="white", font=('Times 25'),width=430)
        #canvas.create_text(300, 550, text="Music by Eric Matyas\nwww.soundimage.org", fill="white", font=('Times 10'),width=430)
        self.menu_bar(window,final_pages)
        #window.mainloop() #basically refreshes the window


def create_book(title,two,three,frame):
    Book(title,two,three,frame)

music = music_file()
stories = story_file(book_library)
user_songs_map = user_audio_map()
user_sounds_map = user_sound_map()
soundFiles = sounds_file()

def main():
    app = tome_to_read()
    app.title("Tome to Read")
    #app.resizable(False,False)
    app.geometry("1200x800")
    app.counter = -1
    '''final_pages, title = ereader_page.diction(ereader_page.book_title)
    ereader_page.vol_slider(app)
    ereader_page.adv_button(app, final_pages, title)
    ereader_page.back_button(app,final_pages, title)
    ereader_page.information()
    ereader_page.music_information()
    ereader_page.menu_bar(app)''' 
    app.mainloop()
    
if __name__ == "__main__":
    main()
