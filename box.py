# 工具箱, 包含rmq解析
import base64
import hashlib
import json
import os, sys
import time, datetime
from tkinter import *

from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
# import tkinter.filedialog as tkFileDialog
# import tkinter.simpledialog as tkSimpleDialog    #askstring()
from aes_utils import Aesutils as aesutils
from const.const import Const;
from rmq_module import RmqUIPack;


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

        self.master.title('my box(version 1.1)')

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
        self.TabStrip1 =  Notebook(self.top)
        self.TabStrip1.place(relx=0.032, rely=0.045, relwidth=0.937, relheight=0.899)

        # rmq 解析
        self.TabStrip1__Tab1 = Frame(self.TabStrip1)
        self.TabStrip1__Tab1Lbl = Label(self.TabStrip1__Tab1)
        self.TabStrip1__Tab1Lbl.place(relx=0.1,rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab1, text='bz rmq 解析')
        RmqUIPack.pack_rmq_ui(self)

        # zk manager
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1__Tab2Lbl = Label(self.TabStrip1__Tab2, text='敬请期待')
        self.TabStrip1__Tab2Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='zk manager')

        # 隧道
        self.TabStrip1__Tab3 = Frame(self.TabStrip1)
        self.TabStrip1__Tab3Lbl = Label(self.TabStrip1__Tab3, text='敬请期待')
        self.TabStrip1__Tab3Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab3, text='ssh 隧道')

        # 时间戳转换
        self.TabStrip1__Tab4 = Frame(self.TabStrip1)
        self.TabStrip1__Tab4Lbl = Label(self.TabStrip1__Tab4)
        self.TabStrip1__Tab4Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab4, text='速查')

        Label(self.TabStrip1__Tab4, text="%Y-%m-%d %H:%M:%S", font=('Calibri', '9')).place(x=130, y=40, anchor='nw')
        Button(self.TabStrip1__Tab4, text='时间戳\n 转 换', command=self.qt).place(x=20, y=25, anchor='nw')
        self.qt1 = Entry(self.TabStrip1__Tab4, width=20, textvariable=Variable(), font=('Calibri', '11'))
        self.qt1.place(x=130, y=20, anchor='nw')
        self.qt2 = Entry(self.TabStrip1__Tab4, width=20, textvariable=Variable(), font=('Calibri', '11'))
        self.qt2.place(x=130, y=55, anchor='nw')

        # 其他
        self.TabStrip1__Tab5 = Frame(self.TabStrip1)
        self.TabStrip1__Tab5Lbl = Label(self.TabStrip1__Tab5, text='敬请期待')
        self.TabStrip1__Tab5Lbl.place(relx=0.1, rely=0.5)
        self.TabStrip1.add(self.TabStrip1__Tab5, text='其他')

    def qt(self):

        if(self.qt1.get().isdigit()):
            print(int(self.qt1.get()))
            localtime = time.localtime(int(self.qt1.get()))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            self.qt2.delete(0, END)
            self.qt2.insert(END, otherStyleTime)
        elif(len(self.qt1.get().strip()) <=0):
            return
        else:
            # 2013-10-10 23:40:00
            self.qt2.insert(END, self.qt1.get())
            timeArray = time.strptime(self.qt1.get(), "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            self.qt2.delete(0, END)
            self.qt2.insert(END,timeStamp)

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
        dumpsss = json.dumps(loads, sort_keys=True, ensure_ascii=False, indent=2, separators=(',', ': '))

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
