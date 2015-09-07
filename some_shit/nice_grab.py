"""  
Tkinter grab example.        -Case Roole

When destroyed, a window returns the grab with the original status to
the window that previously  had it. On entering the window that currently
has the grab will light up red. You can dismiss only the window that has
grabbed focus.

There is some extra code for taking care of root being destroyed upon the
destruction of the last toplevel window.

PROGRAMMING TIP:
  grab_set_global can be mighty effective. You'd better provide an escape
  path before unleashing it, as the window manager will be disabled ;-).
  Here is a rude on for in the if __name__ == '__main__' definition:
  root.after(60*1000*2, root.destroy), that is, after two minutes
  get rid of the windows anyway. Of course, a dismiss button is more elegant.

"""

from Tkinter import *

COUNT = 0

class GrabBack( Toplevel ):
    def _makeButton(self):
        self.button = Button(self,text='dismiss',command=self.destroy)
        self.button.place(relx=0.5,rely=0.5,anchor='c')

    def __init__(self,master):
        global COUNT
        COUNT = COUNT + 1
        Toplevel.__init__(self,master)
        self.title("window %d" % COUNT)
        self.bind('<Enter>', lambda e,f=self.configure: f(background='red'))
        self.bind('<Leave>', lambda e,f=self.configure: f(background='gray80'))
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self._makeButton()

    def nice_grab_set(self):
        "Store current grab status before grabbing the focus."
        self.oldgrab = self.grab_current()
        if self.oldgrab:
            self.oldgrabstatus = self.oldgrab.grab_status()
        else:
            self.oldgrabstatus = None
        print "oldgrab = %s (%s)" % (self.oldgrab, self.oldgrabstatus)
        self.grab_set()

    def nice_grab_set_global(self):
        "Store current grab status before grabbing the focus."
        self.oldgrab = self.grab_current()
        if self.oldgrab:
            self.oldgrabstatus = self.oldgrab.grab_status()
        else:
            self.oldgrabstatus = None
        print "oldgrab = %s (%s)" % (self.oldgrab, self.oldgrabstatus)
        self.grab_set_global()

    def destroy(self):
        global COUNT
        if self.grab_current() and self.grab_current() != self:
            print "Won't destroy window while other has grab"
            return
        if self.oldgrab is not None:
            if self.oldgrabstatus == 'local':
                self.oldgrab.grab_set()
            elif self.oldgrabstatus == 'global':
                self.oldgrab.grab_set_global()
            else:
                print "Weird, oldgrab is not None, but it has status."
        Toplevel.destroy(self)
        COUNT = COUNT - 1
        if COUNT == 0:
            self.master.destroy()

def _test():
    root = Tk()
    root.protocol('WM_DELETE_WINDOW',root.quit)
    root.withdraw()
    root.after(60*1000*1,root.quit)

    top = root
    for i in range(4):
        t = GrabBack(top)
        t.update_idletasks()     # global grab requires that window is viewable
        t.nice_grab_set()
        #t.nice_grab_set_global()
    root.mainloop()

if __name__ == '__main__':
    _test() 
