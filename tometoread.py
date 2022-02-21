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
from curses import window
from tkinter import *
import tkinter.scrolledtext as tkst
from turtle import position
import pandas as pd
import requests
from io import StringIO
import PyPDF2
import json
from sys import version_info
import pygame

pygame.mixer.init()
url='https://raw.githubusercontent.com/colbychambers25/immersive-ebook/main/Domain_Free_eBook.csv'
book_library = pd.read_csv(url) #print to see what the panda looks like
#print(book_library)
url= 'https://raw.githubusercontent.com/colbychambers25/immersive-ebook/page_audio_map/Sound_audio_map.csv'
audio_map = pd.read_csv(url)

def get_from_library(target_url):
    '''
    This function finds the url to our database in github.
    '''
    response = requests.get(target_url)
    data = response.text
    return(data)

def music(n,song):
    if n == 1:
        pygame.mixer.music.load('ereadmp3/'+song)
        pygame.mixer.music.play(loops=30)
    else:
        i = 'do nothing'

def music_player(window,title):
    #if title != 'continue':
     #   music(0,title)
     #   return
    song = audio_map[title].iloc[(window.counter)]
    print(song)
    if window.counter == 0:
        music(1,song)
    elif song != audio_map[title].iloc[(window.counter)-1]:
        music(1,song)
    else:
        music(0,song)

def diction():
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
    print("Which book would you like to read?")
    print(book_library["Title"])
    book_to_get = str(input())
    index = diction[book_to_get]
    # The line below is how the book is found in the dictionary. 
    story = get_from_library(target_url = book_library['URL'][index]) 
    if book_to_get != "Drifting Towards Purpose" and book_to_get != "The Raven":
        story = split_function(story)
    else:
        print('working')
    final_pages=story.split('---split---') #this is the page splitting decider.
    # We will either need to write a function to change pdfs into txt files
    return final_pages, book_to_get


def pages(window,final_pages, forward_back,title):
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
        music_player(window,title)
    canvas = Canvas(bg="dark gray", width=595, height=770)
    canvas.place(relx=.5, rely=.5, anchor=CENTER)
    canvas.config(highlightthickness=0)
    text = canvas.create_text(30, 20, text=str(window.counter)+'/'+str(pages_total) if moderator == False else thanks(window), fill="black", font=('Times 17'),width=510, )
    text = canvas.create_text(300, 400, text=final_pages[window.counter] if moderator == False else thanks(window), fill="black", font=('Times 17'),width=530, )

def thanks(window):
    '''
    Currently the last page of the book. It just prints thank you.
    '''
    music(0,'none')
    canvas = Canvas(bg="dark gray", width=595, height=770)
    canvas.place(relx=.5, rely=.5, anchor=CENTER)
    canvas.config(highlightthickness=0)
    text = canvas.create_text(300, 400, text="Thank you For Reading", fill="black", font=('Times 25'),width=430)


def welcome_screen():
    '''
    Welcome Screen so the window isnt just blank until we add the library.
    '''
    title_line = 'Hello and Welcome to Tome To Read'
    canvas = Canvas(bg="dark gray", width=595, height=770)
    canvas.place(relx=.5, rely=.5, anchor=CENTER)
    canvas.config(highlightthickness=0)
    titles = book_library["Title"]
    title_str = ''
    for item in titles:
        title_str += item + '\n'
    print(titles)
    text = canvas.create_text(300, 300, text=title_line, fill="black", font=('Times 25'),width=430)
    text = canvas.create_text(300, 450, text="Which book would you like to read?", fill="black", font=('Times 20'),width=430)
    text = canvas.create_text(300, 600, text=title_str, fill="black", font=('Times 20'),width=430)
    
    return diction()
    

def adv_button(window,final_pages,title):
    adv = 'adv'
    btn = Button(
    window,
    text=">",
    height=3,
    width=3,
    command = lambda: pages(window,final_pages,adv,title)
    )
    btn.pack(side="right")
    btn.place(relx=.5, rely=.5,x=400, anchor=CENTER)

def back_button(window,final_pages,title):
    back = "back"
    btn2 = Button(
    window,
    height = 3,
    width = 3,
    text = '<',
    command = lambda: pages(window,final_pages,back,title)
    )
    btn2.pack(side="right")
    btn2.place(relx=.5, rely=.5,x=340, anchor=CENTER)

def split_function(story):
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

def main():
    ''' 
    Creates the window, and calls this diction function to get a key value pair linked by page number.
    Currently only supports .txt files because pdf files lack the functionality 
    to be manipulated and most domain stories use .txt or .epub not pdf.
    '''
    window = Tk()
    window.title("Immersive Reading")
    window.configure(bg="gray")
    window.geometry("900x800")
    frame = Frame(window)
    frame.pack()
    window.counter = -1 #this is universal counter funtion that allows a user to traverse a story.
    final_pages, title = welcome_screen()
    adv_button(window, final_pages, title)
    back_button(window, final_pages, title) 
    window.mainloop() #basically refreshes the window


if __name__ == "__main__":
    main()
