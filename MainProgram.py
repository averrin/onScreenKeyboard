#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tsa'
from ConfigManager import ConfigManager
from GuiManager import GuiManager
from KeyboardStatus import keyboardStatus

class ThreadedClient:
    def __init__(self, master):
        self.master = master

        self.config=ConfigManager()
        self.keyTrainer=keyboardStatus(self.config)
        keyTrainer=self.keyTrainer

        master.protocol('WM_DELETE_WINDOW', self.kill_and_destroy)

        self.guiManager=GuiManager(master,self.config,keyTrainer.myQueue,keyTrainer)

        keyTrainer.begin_scan()

        self.running = 1
        self.periodicCall()
    def kill_and_destroy(self):
        self.running = 0
        self.keyTrainer.stop_scan()
        if self.config.debug:
            print "Stopping scan..."
        self.master.destroy()


    def periodicCall(self):
        self.guiManager.processQueue()
        if not self.running:
            # import sys
            # sys.exit(1)
            self.kill_and_destroy()
        self.master.after(20, self.periodicCall)

if __name__ == '__main__':
    try:
        import Tkinter
        root = Tkinter.Tk()

        root.attributes("-alpha", 0.5)
        client = ThreadedClient(root)
        root.mainloop()
    except ImportError:
        print("Please install tkinter for python, on Ubuntu, Mint do following:\n"
              "sudo apt-get install python-tk")
