import subprocess
import threading
import Queue
import os
import time
import signal

class keyboardStatus():
    def __init__(self,config):
        self.current_lang=0
        self.initQueue()
        self.config=config
      #  self.numbers=set(['0','1','2','3','4','5','6','7','8','9'])

    def initQueue(self):
        self.myQueue=Queue.Queue()

    def openReadingLang(self):
        #os.system('killall xinput 2>&1 > /dev/null')

        from subprocess import Popen,PIPE
        if not self.config.wm_is_unity:
            self.myLangProcess=Popen('while true; do xset -q'+'|'+'grep LED'+'|'+' awk \'{ print $10 }\''+'|'+'cut -c5; sleep 0.02; done',shell=True,stdout=subprocess.PIPE)
            self.lang_proc_started=True

            while self.lang_proc_started:
                line = self.myLangProcess.stdout.readline()
                if line!='':
                    lang_index=int(line)
                    if lang_index!=self.current_lang:
                        self.current_lang=lang_index
                        if self.config.debug:
                            print "Current language is "+line
                        self.myQueue.put((-1,lang_index))
        else:
            self.myLangProcess=Popen('while true; do setxkbmap -print '+'|'+' awk -F"+" \'/xkb_symbols/ {print $2}\'; done',shell=True,stdout=subprocess.PIPE)
            self.lang_proc_started=True

            while self.lang_proc_started:
                line = self.myLangProcess.stdout.readline()
                if line!='':
                    if line.find('us')>-1:
                        lang_index=0
                    else:
                        lang_index=1
                    if lang_index!=self.current_lang:
                        self.current_lang=lang_index
                        if self.config.debug:
                            print "Current language is "+line
                        self.myQueue.put((-1,lang_index))

        self.myLangProcess.terminate()
        if self.config.debug:
            print "Waiting for lang process to stop..."
        self.myLangProcess.wait()
        self.myQueue.queue.clear()

        os.system('killall xinput 2>&1 > /dev/null')
        if self.config.debug:
            print 'Stopped language determination process!'

    def openReadingKeys(self):
        from subprocess import Popen,PIPE

        self.myProcess=Popen('xinput list '+'|'+'   grep -Po \'id=\K\d+(?=.*slave\s*keyboard)\' '+'|'+'   xargs -P0 -n1 xinput test',shell=True,stdout=subprocess.PIPE)

        self.proc_started=True

        symbol_index=0
        press_release_dict={'p':1,'r':0}
        symbol_pressed=0

        while self.proc_started:
            symbol=self.myProcess.stdout.read(1)
            if symbol in press_release_dict:
                symbol_pressed=press_release_dict[symbol]
                while symbol!='\n':
                    symbol=self.myProcess.stdout.read(1)
                    if symbol.isdigit():
                        symbol_index=symbol_index*10+int(symbol)

                self.myQueue.put((symbol_index,symbol_pressed))
                symbol_index=0

        self.myProcess.terminate()

        if self.config.debug:
            print "Waiting xinput process to stop..."
        self.myProcess.wait()

        self.myQueue.queue.clear()
        if self.config.debug:
            print 'Stopped xinput process!'

    def begin_scan(self):
        newThread=threading.Thread(target=self.openReadingKeys)
        newThread.start()
        newThread2=threading.Thread(target=self.openReadingLang)
        newThread2.start()

    def stop_scan(self):
        self.proc_started=False
        self.lang_proc_started=False
        os.kill(self.myProcess.pid,signal.SIGTERM)

