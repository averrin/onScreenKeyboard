__author__ = 'tsa'
from ConfigManager import ConfigManager
from GuiManager import GuiManager
from KeyboardStatus import keyboardStatus
import Tkinter





class ThreadedClient:
    def __init__(self, master):
        self.master = master

        config=ConfigManager('program.conf')
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

root = Tkinter.Tk()
root.attributes("-alpha", 0.5)
client = ThreadedClient(root)

root.mainloop()
