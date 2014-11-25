import subprocess
import threading
import Queue

def print_function(x):
    print x

class keyboardStatus():
    def __init__(self,config):
        self.current_lang=0
        self.initQueue()
        self.config=config

    def initQueue(self):
        self.myQueue=Queue.Queue()

    def openReadingLang(self):
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

        self.myQueue.queue.clear()
        self.myLangProcess.terminate()
        import os
        os.system('killall xinput 2>&1 > /dev/null')
        if self.config.debug:
            print 'Killed language determination process!'

    def openReadingKeys(self):
        from subprocess import Popen,PIPE
        self.myProcess=Popen('xinput list '+'|'+'   grep -Po \'id=\K\d+(?=.*slave\s*keyboard)\' '+'|'+'   xargs -P0 -n1 xinput test',shell=True,stdout=subprocess.PIPE)
        self.proc_started=True

        key_presssed_index=0;
        word_index=0;

        while self.proc_started:
            line = self.myProcess.stdout.readline()
            if line!='':
                word_index=line.find('press')
                if word_index>0:
                    key_presssed_index=int(line[5+word_index:].strip())
                    self.myQueue.put((key_presssed_index,1))
                else:
                    word_index=line.find('release')
                    key_presssed_index=int(line[7+word_index:].strip())
                    self.myQueue.put((key_presssed_index,0))

        self.myQueue.queue.clear()
        self.myProcess.terminate()
        if self.config.debug:
            print 'Killed keys determination process!'

    def begin_scan(self):
        newThread=threading.Thread(target=self.openReadingKeys)
        newThread.start()
        newThread2=threading.Thread(target=self.openReadingLang)
        newThread2.start()

    def stop_scan(self):
        self.proc_started=False
        self.lang_proc_started=False

