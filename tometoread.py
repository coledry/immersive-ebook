'''
TITLE: Tome To Read
AUTHORS: ...
DESCRIPTION: So far this is the ereader. Right now we need a function to prep pre uploaded files, but
                for now this function works on all but The Raven and A Little Journey.
NOTES: 1. There are some imports that im not sure are doing anything.
        2. Main is way to long. I think i need a fuction for our buttons.
        3. Text files work way better for formatting in Tkinter.
        4. We need a function that reads .txt files and adds "---split---" between pages.
        5. Sorry James for taking out what you had changed I just was having trouble with getting
             the window to work on my computer and I am not sure why lol.
'''
from tkinter import *
from turtle import color, position
import pandas as pd
import requests
import pygame
import customtkinter

pygame.mixer.init()
url='https://raw.githubusercontent.com/colbychambers25/immersive-ebook/main/Domain_Free_eBook.csv'
book_library = pd.read_csv(url) #print to see what the panda looks like
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/Sound_audio_map.csv'
audio_map = pd.read_csv(url)
prev_song = ['none']

class Book:
    def __init__(self,book_title, sound,theme,window):
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
        text = canvas.create_text(30, 20, text=str(window.counter)+'/'+str(pages_total) if moderator == False else self.thanks(window), fill="black", font=('Times 17'),width=510, )
        text = canvas.create_text(300, 400, text=final_pages[window.counter] if moderator == False else self.thanks(window), fill="black", font=('Times 17'),width=530, )

    def thanks(self):
        '''
        Currently the last page of the book. It just prints thank you.
        '''
        self.music(0,'none')
        canvas = Canvas(bg="dark gray", width=595, height=770)
        canvas.place(relx=.5, rely=.5, anchor=CENTER)
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
        frame_4 = customtkinter.CTkFrame(master=window, width=80, height=500)
        frame_4.place(relx=.5, rely=.5,x=-520, anchor=CENTER)
        frame_4.configure(fg_color=("lightgray"))
        self.library_button(frame_4)
        self.find_button(frame_4)
        self.settings_button(frame_4)
        self.upload_button(frame_4)
    
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
        slider = customtkinter.CTkSlider(master=window,
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
        window = self.window
        window.counter = -1 #this is universal counter funtion that allows a user to traverse a story.
        final_pages, title = self.diction(self.book_title)
        self.vol_slider(window)
        self.adv_button(window, final_pages, title)
        self.back_button(window, final_pages, title) 
        self.information()
        self.music_information()
        self.menu_bar(window)
        window.mainloop() #basically refreshes the window

        
        
#everything below here should be deleted when using this file but it is here for testing
window = customtkinter.CTk()
#customtkinter.set_default_color_theme(self.theme)
window.title("Immersive Reading")
window.configure(bg = 'gray')
window.geometry("1200x800")
frame= Frame(window)
frame.pack()

Book("Treasure Island",'off','',window)
