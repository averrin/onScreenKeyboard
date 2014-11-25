__author__ = 'tsa'
from ConfigManager import ConfigManager
from GuiManager import GuiManager
from KeyboardStatus import keyboardStatus

class ThreadedClient:
    def __init__(self, master):
        self.master = master

        config=ConfigManager()
        self.keyTrainer=keyboardStatus(config)
        keyTrainer=self.keyTrainer

        def kill_and_destroy():
            self.running = 0
            self.keyTrainer.stop_scan()
            self.master.destroy()

        master.protocol('WM_DELETE_WINDOW', kill_and_destroy)

        self.guiManager=GuiManager(master,config,keyTrainer.myQueue,keyTrainer)

        keyTrainer.begin_scan()

        self.running = 1
        self.periodicCall()

    def periodicCall(self):
        self.guiManager.processQueue()
        if not self.running:
            import sys
            sys.exit(1)
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

