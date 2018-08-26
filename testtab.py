# 工具箱, 包含rmq解析
import base64
import hashlib
import json
import os, sys
from tkinter import *

from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
# import tkinter.filedialog as tkFileDialog
# import tkinter.simpledialog as tkSimpleDialog    #askstring()
from aes_utils import Aesutils as aesutils
from const.const import Const;


class ApplicationUi(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        rer = Const.topIcon
        ico = bytes(rer, 'utf-8')
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(ico))
        tmp.close()
        self.master.iconbitmap("tmp.ico")
        os.remove("tmp.ico")

        self.master.title('my box')

        # 得到屏幕宽度
        sw = self.master.winfo_screenwidth()
        # 得到屏幕高度
        sh = self.master.winfo_screenheight()

        ww = 1120
        wh = 710
        # 窗口宽高为100
        x = (sw - ww)/2
        y = (sh - wh)/2

        self.master.deiconify()  # now window size was calculated
        self.master.withdraw()  # hide window again
        dfd = '%dx%d+%d+%d' % (ww, wh, x, y)
        self.master.geometry(dfd)
        self.master.deiconify()
        self.create_widgets()

    def create_widgets(self):
        box_menu = Menu(self)
        box_menu.add_command(label="关于", command=hello)

        self.top = self.winfo_toplevel()
        self.style = Style()
        self.top.config(menu=box_menu)
        self.TabStrip1 = Notebook(self.top)
        self.TabStrip1.place(relx=0.032, rely=0.045, relwidth=0.937, relheight=0.899)

        # rmq 解析
        self.TabStrip1__Tab1 = Frame(self.TabStrip1)
        self.TabStrip1__Tab1Lbl = Label(self.TabStrip1__Tab1)
        self.TabStrip1__Tab1Lbl.place(relx=0.1,rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab1, text='bz rmq 解析')

        self.a = Label(self.TabStrip1__Tab1, text='输入topic: ')
        self.a.place(x=18, y=20, anchor='nw')

        e = StringVar()
        self.b = Entry(self.TabStrip1__Tab1, width=30, textvariable=e, font=('Calibri', '11'))
        self.b.place(x=100, y=20, anchor='nw')

        self.c = Label(self.TabStrip1__Tab1, text='输入密文: ')
        self.c.place(x=20, y=55, anchor='nw')

        self.d = Text(self.TabStrip1__Tab1, height=40, width=30)
        self.d.place(x=100, y=55, anchor='nw')

        self.e = Label(self.TabStrip1__Tab1, text='明文: ').place(x=390, y=45, anchor='nw')

        self.f = Text(self.TabStrip1__Tab1, height=40)
        self.f.place(x=450, y=55, anchor='nw')

        self.e = Button(self.TabStrip1__Tab1, text='解密', width=15, command=self.parse)
        self.e.place(x=390, y=17, anchor='nw')

        # zk manager
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1__Tab2Lbl = Label(self.TabStrip1__Tab2, text='敬请期待')
        self.TabStrip1__Tab2Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='zk manager')

        # 隧道
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1__Tab2Lbl = Label(self.TabStrip1__Tab2, text='敬请期待')
        self.TabStrip1__Tab2Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='隧道')

        # 其他
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1__Tab2Lbl = Label(self.TabStrip1__Tab2, text='敬请期待')
        self.TabStrip1__Tab2Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='其他')


    def parse(self):
        key = self.b.get()
        hexdigest_ = hashlib.md5(key.encode('utf-8')).hexdigest()[8:-8]
        print(hexdigest_)
        context = self.d.get("0.0", "end")
        decode = base64.b64decode(context)
        rs = aesutils.aes_ecb_decrypt(decode, hexdigest_)
        rs_decode = rs.decode('utf-8')
        print(rs_decode)
        loads = json.loads(rs_decode)
        msgBody = loads['msgBody']
        if msgBody.strip() == '':
            print('msg body is null')
        else:
            try:
                decdsdsode = base64.b64decode(msgBody)
            except  Exception:
                print("msg body 非密文")
            else:
                print("msg body 密文")
                decryptss = aesutils.aes_ecb_decrypt(decdsdsode,
                                                     hashlib.md5(loads['msgType'].encode('utf-8')).hexdigest()[8:-8])
                json_loadsss = json.loads(decryptss.decode('utf-8'))
                loads['msgBody'] = json_loadsss

        self.f.delete(1.0, END)
        dumpsss = json.dumps(loads, sort_keys=True, indent=2, separators=(',', ': '))

        self.f.insert(END, dumpsss)




class Application(ApplicationUi):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        ApplicationUi.__init__(self, master)


def hello():
    showinfo("关于", " 袁大师的工具箱\n qq:173171486 \n 接受bug 拒绝需求")
    print("hhh")



if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
