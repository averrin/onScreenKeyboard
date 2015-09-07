from Tkinter import Tk, Frame, BOTH
import Tkinter
from PIL import Image, ImageTk

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)            
        self.parent = parent        
        self.initUI()

    def initUI(self):
        self.parent.title("PISE")
        self.pack(fill=BOTH, expand=1)

root = Tk()
root.geometry("1111x675+300+300")
app = Example(root)

im = Image.open('Test1.png')
tkimage = ImageTk.PhotoImage(im)
myvar=Tkinter.Label(root,image = tkimage)
myvar.place(x=0, y=0, relwidth=1, relheight=1)

custName = Tkinter.StringVar(None)
yourName = Tkinter.Entry(root, textvariable=custName)
yourName.pack()

relStatus = Tkinter.StringVar()
relStatus.set(None)

labelText = Tkinter.StringVar()
labelText.set('Accuracy Level')
label1 = Tkinter.Label(root, textvariable=labelText, height=2)
label1.pack()

def beenClicked1(event):
    event.widget.pack_forget()
    pass

def beenClicked5(event):
    event.widget.pack()
    pass

radio1 = Tkinter.Button(root, text='100%')
radio1.bind('<Button-1>',lambda x:beenClicked1(myvar))
radio1.pack()
radio2 = Tkinter.Radiobutton(root, text='50%', value='5', variable = relStatus, command=beenClicked5).pack()
1

print dir(myvar)
root.mainloop()
