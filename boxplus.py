import atexit
import base64
import cProfile
import gc
import os
from compent.compent import Application
from const.const import Const
import tkinter as tk

if __name__ == '__main__':
    rer = Const.topIcon
    ico = bytes(rer, 'utf-8')
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(ico))
    tmp.close()
    root = tk.Tk()
    Application(root).mainloop()
