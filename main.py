#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project Name: PythonImageViewer - Created Date: Tuesday September 22nd 2020
# Author: loitd - Email: loitranduc@gmail.com
# Description: This is a short project/file description
# Copyright (c) 2020 loitd. WWW: https://github.com/loitd
# -----
# Last Modified: Tuesday September 22nd 2020 2:03:13 pm By: loitd
# -----
# HISTORY:
# Date      	By    	Comments
# ----------	------	----------------------------------------------------------
# 2020-09-22	loitd	Initialized
# 2020-09-24    loitd   Version 1.0 without mousewheel zoom adapt               
###

from sys import argv
from tkinter import Tk, Canvas, NW, YES, BOTH, Frame, X, Y, TOP, LEFT, FLAT, ALL, filedialog, Menu, PhotoImage, messagebox
from PIL import Image, ImageTk

def cal_fitsize(imsize, cvsize):
    global withpil
    if withpil:
        ratiow = cvsize[0]/imsize[0]
        ratioh = cvsize[1]/imsize[1]
        ratio = min(ratiow, ratioh)
    else:
        ratiow = cvsize[0]//imsize[0]
        ratioh = cvsize[1]//imsize[1]
        ratio = min(ratiow, ratioh)
    newsize = (int(imsize[0]*ratio), int(imsize[1]*ratio))
    newpos = int((cvsize[0]-newsize[0])//2), int((cvsize[1]-newsize[1])//2)
    print(imsize, cvsize, newsize, newpos, ratio)
    # return newsize, newpos
    return ratio, newpos, newsize

def get_screensize(root):
    screensize = screenw, screenh = root.winfo_screenwidth(), root.winfo_screenheight()
    return screensize

def get_objsize(obj):
    root.update()
    canvassize = canvasw, canvash = obj.winfo_width(), obj.winfo_height()
    return canvassize

def open_newfile():
    global url
    filename = filedialog.askopenfilename(title = "Open image file",filetypes = (("Image files","*.png;*.jpeg;*.jpg;*.gif"),("All files","*.*")))
    url = filename
    draw_image(cv, url)
    return filename

def save_imageas():
    try:
        if withpil:
            files = [('All Files', '*.*'), ('PNG Files', '*.png'), ('JPEG Files', '*.jpeg')] 
            filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files).name
            im.save(filename)
            messagebox.showinfo(title="Information", message="New file saved successfully")
        else:
            pass
    except Exception as e:
        messagebox.showerror(title="Error", message="There was an error while saving file") 

def show_aboutus():
    messagebox.showinfo(title="About Us", message="""This is PIV - Python Image Viewer
\nA lightweight, 100% free and pure Python image viewer application. Be cross-platformed on Windows, GNU/Linux, Mac OS X, FreeBSD, Solaris and AIX.
\nCreated by Tran Duc Loi at https://github.com/loitd.
\nFirst release was at 2020 September. 
\nThis application is under MIT Licence.
""")

def show_credit():
    messagebox.showinfo(title="Credit", message="""PIV - Python Image Viewer is built under MIT License with contributions of:

Python Developer(s):
- Tran Duc Loi (https://github.com/loitd)

Image/Icon creator(s):
- Tran Duc Loi (https://github.com/loitd)

By me a coffe? 
Paypal: https://paypal.me/loitd
""")

def popup(event):
    try:
        # menu.post(event.x_root, event.y_root)
        menu.tk_popup(event.x_root, event.y_root)
        return event.widget
    finally:
        menu.grab_release()

def create_maingui():
    global withpil
    root.iconbitmap("piv.ico")
    root.state('zoomed')
    # root.attributes('-fullscreen', True)
    # root.bind('<Escape>',lambda e: root.destroy())
    row = Frame(root)
    row.pack(side=TOP, expand=YES, fill=BOTH, padx=1, pady=1)
    cv = Canvas(row)
    cv.pack(expand=YES, fill=BOTH)
    # create a popup menu
    imopen = Image.open(fp=r"open.gif")
    imopen = ImageTk.PhotoImage(image=imopen)
    # piopen = PhotoImage(file=r"open.gif")
    menu.add_command(label="Open new image", image=imopen, compound=LEFT, command=open_newfile)
    if withpil: menu.add_command(label="Save image as", command=save_imageas)
    # Menu item with submenu
    aboutsubmenu = Menu(menu, tearoff=0)
    aboutsubmenu.add_command(label="Credits", command=show_credit)
    aboutsubmenu.add_command(label="About Us", command=show_aboutus)
    menu.add_cascade(label="About", menu=aboutsubmenu)
    # # Menu item next
    menu.add_separator()
    menu.add_command(label="Exit", command=root.quit)
    # Bindings
    root.bind("<Configure>", configure_event)
    root.bind("<Button-3>", popup)
    return cv

def draw_image(cv, url):
    global withpil, im
    root.title("Python Image Viewer - {0}".format(url))
    if withpil:
        im = Image.open(url)
        imsize = im.size
        cvsize = get_objsize(cv)
        ratio, newpos, newsize = cal_fitsize(imsize, cvsize)
        imresize = im.resize(newsize)
        pi = ImageTk.PhotoImage(image=imresize)
    else:
        pi = PhotoImage(file=url) #wrap with pillow resized im
        imsize = pi.width(), pi.height()
        cvsize = get_objsize(cv)
        ratio, newpos, newsize = cal_fitsize(imsize, cvsize)
        pi = pi.zoom(ratio)
    
    # placing in canvas
    cv.delete(ALL)
    cv.image = pi #https://stackoverflow.com/a/37214188
    cv.create_image(newpos[0], newpos[1], anchor=NW, image=pi)
    return 1

def configure_event(event):
    draw_image(cv, url)

if __name__ == "__main__":
    url = None
    withpil = True
    im = None
    print(argv)
    if len(argv) == 1:
        url = r"piv.png"
    elif len(argv) == 2:
        url = argv[1]
    root = Tk()
    menu = Menu(root, tearoff=0)
    # create main gui
    cv = create_maingui()
    # drawing
    draw_image(cv, url)
    # Main loop
    root.mainloop()
    