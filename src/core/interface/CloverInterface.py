# -*- coding: utf8 -*-
from Tkinter import *
import tkMessageBox
import locale
import json
import winshell
#import gettext

class CloverInterface:
    def __init__(self, name, cfile, setup_path):
        self.name = name
        root = Tk()
        root.title(self.name)
        root.attributes("-topmost", True)
        root.iconbitmap(setup_path+'\\clover.ico')
        root.withdraw()
        self.cfile = cfile
        self.root = root
        #gettext.install('general', setup_path()+'\\locale')

    def changed_key(self, block):
        key_path = block['key'][0]+"\\"+block['key'][1]+"\\"+block['changed_value'][0]
        result = tkMessageBox.askyesno(self.name, "Detected Windows registry changes:"+"\n"+key_path+": "+block['changed_value'][1]+"\n"+"Do you want to rollback?", icon=tkMessageBox.WARNING)
        if result == True:
            logs = open(self.cfile, 'a')
            logs.write(json.dumps(block)+"\n")
            logs.close()

    @staticmethod
    def clear(pipes):
        """ Clears communication file """
        for pipe in pipes:
            logs = open(pipe, 'w')
            logs.close()

class CloverServiceInterface:
    def __init__(self, pipe_path):
        """ Simulates pipe communication """
        self.file = pipe_path
        #self.clear()

    def changed_key(self, changed_value, key, keys_old):
        logs = open(self.file, 'a')
        logs.write(json.dumps({'changed_value': changed_value, 'key': key, 'keys_old': keys_old, 'type': 1})+"\n")
        logs.close()
