from Tkinter import *

master = Tk()

def callback(button):
    button.flash()
    print "click!"

def createKeyboard():
    group = LabelFrame(master, text="Keyboard", padx=5, pady=5)
    group.pack(padx=10, pady=10)


    b = Button(group, text="OK1")
    b.pack(side=LEFT)

    c = Button(group, text="OK2", command=lambda:callback(b))
    c.pack(side=LEFT)

    b.configure(command=lambda:callback(c))

createKeyboard()

mainloop()
