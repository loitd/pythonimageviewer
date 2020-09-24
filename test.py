from sys import argv
# from PIL import Image, ImageTk
from tkinter import Tk, Canvas, NW, YES, BOTH, Frame, X, Y, TOP, LEFT, FLAT, ALL, PhotoImage

url = r"piv.png"
root = Tk()
# create main gui
root.iconbitmap("piv.ico")
root.state('zoomed')
row = Frame(root)
row.pack(side=TOP, expand=YES, fill=BOTH, padx=1, pady=1)
cv = Canvas(row)
cv.pack(expand=YES, fill=BOTH)
# drawing
root.title("Python Image Viewer - {0}".format(url))
pi = PhotoImage(file=url) #wrap with pillow resized im
# placing in canvas
cv.delete(ALL)
cv.image = pi #https://stackoverflow.com/a/37214188
cv.create_image(0,0, anchor=NW, image=pi)
# Main loop
root.mainloop()
