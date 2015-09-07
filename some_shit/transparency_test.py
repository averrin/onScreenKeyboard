# semi-transparent-stipple-demo.py
# note: stipple only works for some objects (like rectangles)
# and not others (like ovals).  But it's better than nothing...

from Tkinter import *

def redrawAll(canvas):
    canvas.delete(ALL)
    # draw a red rectangle on the left half
    canvas.create_rectangle(0, 0, 250, 600, fill="red")
    # draw semi-transparent rectangles in the middle
    canvas.create_rectangle(200,  75, 300, 125, fill="blue", stipple="")
    canvas.create_rectangle(200, 175, 300, 225, fill="blue", stipple="gray75")
    canvas.create_rectangle(200, 275, 300, 325, fill="blue", stipple="gray50")
    canvas.create_rectangle(200, 375, 300, 425, fill="blue", stipple="gray25")
    canvas.create_rectangle(200, 475, 300, 525, fill="blue", stipple="gray12")

def init(canvas):
    redrawAll(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=500, height=600)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", mousePressed)
    # root.bind("<Key>", keyPressed)
    # timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
