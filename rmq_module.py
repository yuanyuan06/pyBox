# 构造mq解析ui
from tkinter import *

from tkinter.ttk import *


# import tkinter.filedialog as tkFileDialog
# import tkinter.simpledialog as tkSimpleDialog    #askstring()


class RmqUIPack:

    @staticmethod
    def pack_rmq_ui(top):

        top.a = Label(top.TabStrip1__Tab1, text='输入topic: ')
        top.a.place(x=18, y=20, anchor='nw')

        e = StringVar()
        top.b = Entry(top.TabStrip1__Tab1, width=30, textvariable=e, font=('Calibri', '11'))
        top.b.place(x=100, y=20, anchor='nw')

        top.c = Label(top.TabStrip1__Tab1, text='输入密文: ')
        top.c.place(x=20, y=55, anchor='nw')

        top.d = Text(top.TabStrip1__Tab1, height=40, width=30, wrap='none')
        top.d.place(x=100, y=55, anchor='nw')

        top.e = Label(top.TabStrip1__Tab1, text='明文: ').place(x=390, y=45, anchor='nw')

        top.f = Text(top.TabStrip1__Tab1, height=40)
        top.f.place(x=450, y=55, anchor='nw')

        top.e = Button(top.TabStrip1__Tab1, text='解密', width=15, command=top.parse)
        top.e.place(x=390, y=17, anchor='nw')

        top.e.pack
        top.b.pack
        top.c.pack
        top.d.pack
        top.e.pack
        top.f.pack