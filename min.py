import win32api, win32gui
import win32con, winerror
import sys, os
from tkinter import *
import threading
from traceback import *
from win32com.client import Dispatch
import time, eyed3
from tkinter import filedialog


total = 100
name = []
index = [1]
filenames = []
root = Tk()


def openfile(index=[1]):
    global total, name
    filenames = []


    filenames = filedialog.askopenfilenames(title="音乐播放器",
                                            filetypes=[("mp3文件", "*.mp3"), ("WMA文件", "*.wma"), ("WAV文件", "*.wav")])
    if filenames:
        save = open("info.txt", "a+")

        for i in range(len(filenames)):
            media = wmp.newMedia(filenames[i])
            wmp.currentPlaylist.appendItem(media)
            save.write("%s\n" % filenames[i])
            print(filenames)
            coco = eyed3.load(filenames[i])  # eyed3模块读取mp3信息
            total = int(coco.info.time_secs)
            minute = int(coco.info.time_secs) // 60
            sec = int(coco.info.time_secs) % 60
            length = int(coco.info.time_secs)

            name = filenames[i].split("/")

            k = index[-1]
            itemsong = str(k) + "." + name[-1] + " " * 6 + "0%d:%d" % (minute, sec) + "\n"

            if sec >= 10:
                list_name.insert(END, itemsong)
            else:
                list_name.insert(END, itemsong)
            k = k + 1
            index.append(k)

        save.close()


def play(event=None):
    # root.title("%s" % name[-1]),使用wmp.currentMedia.name更好,在per函数中
    per_thread = threading.Thread(target=per)
    per_thread.daemon = True
    wmp.controls.play()
    per_thread.start()
    # print(wmp.currentMedia.duration)#放到暂停那里居然可以用,而这里不行


def per():
    global total
    while wmp.playState != 1:
        global progress_scal
        progress_scal.set(int(wmp.controls.currentPosition))
        progress_scal.config(label=wmp.controls.currentPositionString)
        progress_scal.config(to=total, tickinterval=50)
        time.sleep(1)
        root.title("%s" % wmp.currentMedia.name)


def stop():
    wmp.controls.stop()


def pause(event=None):
    wmp.controls.pause()


def uselist():
    pass


def fullscr():
    pass


def exitit():
    root.destroy()


def Previous_it():
    wmp.controls.previous()


def Next_it():
    wmp.controls.next()


def Volume_ctr(none):
    global vio_scale
    wmp.settings.Volume = vio_scale.get()


def Volume_add(i=[0]):
    global vio_scale
    wmp.settings.Volume = wmp.settings.Volume + 5
    i.append(wmp.settings.Volume)
    vio_scale.set(wmp.settings.Volume)


def Volume_minus(i=[0]):
    global vio_scale
    wmp.settings.Volume = wmp.settings.Volume - 5
    i.append(wmp.settings.Volume)
    vio_scale.set(wmp.settings.Volume)


def Scale_ctr(none):
    global var_scale
    wmp.controls.currentPosition = var_scale.get()
    print(wmp.currentMedia.duration)


def Clear_list():
    stop()
    wmp.currentPlaylist.clear()
    list_name.delete(1.0, END)
    name = []
    index = []


def List_random():
    wmp.settings.setMode("shuffle", True)
    play()


def List_loop():
    wmp.settings.setMode("loop", True)
    play()


def list_new(index=[1]):
    str1 = simpledialog.askstring("新建歌曲列表", "请输入列表名称")
    new_list = open("%s.txt" % str1, "w+")
    global total, name
    filenames = []

    filenames = filedialog.askopenfilenames(title="音乐播放器",
                                            filetypes=[("mp3文件", "*.mp3"), ("WMA文件", "*.wma"), ("WAV文件", "*.wav")])
    if filenames:

        for i in range(len(filenames)):
            media = wmp.newMedia(filenames[i])
            wmp.currentPlaylist.appendItem(media)
            new_list.write("%s\n" % filenames[i])
            print(filenames)
            coco = eyed3.load(filenames[i])  # eyed3模块读取mp3信息
            total = int(coco.info.time_secs)
            minute = int(coco.info.time_secs) // 60
            sec = int(coco.info.time_secs) % 60
            length = int(coco.info.time_secs)

            name = filenames[i].split("/")

            k = index[-1]
            itemsong = str(k) + "." + name[-1] + " " * 6 + "0%d:%d" % (minute, sec) + "\n"

            if sec >= 10:
                list_name.insert(END, itemsong)
            else:
                list_name.insert(END, itemsong)
            k = k + 1
            index.append(k)


class MainWindow:
    def __init__(self):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated");  # 定义一个新的窗口消息
        message_map = {  # 建立函数命令字典，用于窗口回调函数的四个参数
            msg_TaskbarRestart: self.OnRestart,
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER + 20: self.OnTaskbarNotify,
        }
        # Register the Window class.
        self.wc = win32gui.WNDCLASS()  # 局部变量wc改成窗口类的实例
        hinst = self.wc.hInstance = win32api.GetModuleHandle(None)  # 获得程序模块句柄
        self.wc.lpszClassName = ("PythonTaskbarDemo")  # 窗口类的类名
        self.wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;  # 窗口类的style特征，水平重画和竖直重画
        self.wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        self.wc.hbrBackground = win32con.COLOR_WINDOW
        self.wc.lpfnWndProc = message_map  # could also specify a wndproc，给窗口回调函数赋值
        '''这里传进去的其实是函数指针，它里面保存的是我们定义的windowproc的入口地址'''
        # Don't blow up if class already registered to make testing easier
        try:
            classAtom = win32gui.RegisterClass(self.wc)  # 用wc将classatom注册为一个窗口类
        except win32gui.error and err_info:
            if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.wc.lpszClassName, "Taskbar Demo", style,  # 创建一个窗口
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)  # 更新窗口
        self._DoCreateIcons()
        win32gui.PumpMessages()

    def _DoCreateIcons(self):
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)

        iconPathName = os.path.abspath(
            os.path.join(os.path.split(sys.executable)[0], "pyc.ico"))  # sys.executalbe为python解释程序路径
        # if not os.path.isfile(iconPathName):#如果系统ico文件不存在
        # Look in DLLs dir, a-la py 2.5
        # iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "DLLs", "pyc.ico" ))
        # if not os.path.isfile(iconPathName):
        # Look in the source tree.
        # iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "..\\PC\\pyc.ico" ))
        # if os.path.isfile(iconPathName):
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE  # ico标识，从文件载入和默认大小
        hicon = win32gui.LoadImage(hinst, "classic.ico", win32con.IMAGE_ICON, 0, 0, icon_flags)  # 载入.ico文件
        '''handle = LoadImage(hinst,name,type,cx,cy,fuload)'''
        # else:
        # print ("Can't find a Python icon file - using default")
        # hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO  # 定义托盘图标的样式
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "酷酷东东mp3播放器", "猪已经跑到系统托盘了")
        # 最后一个选项猪已经跑。。”是气泡提示内容
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)  # 增加系统托盘图标
        except win32gui.error:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print("Failed to add the taskbar icon - is explorer running?")
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            root.deiconify()
            print("有种你单击死我呀.")
            win32gui.DestroyWindow(self.hwnd)
            win32gui.UnregisterClass(self.wc.lpszClassName, None)

        elif lparam == win32con.WM_LBUTTONDBLCLK:
            root.deiconify()
            print("你居然双击，我爱死你了")
            win32gui.DestroyWindow(self.hwnd)
            win32gui.UnregisterClass(self.wc.lpszClassName, None)
        elif lparam == win32con.WM_RBUTTONUP:
            print("右击有美女哟.")
            menu = win32gui.CreatePopupMenu()  # 产生一个菜单句柄menu
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "出来吧，对话框")  # 给菜单添加子项，1027可以一直下去
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "你好，猪")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "退出程序")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1026, "神猪大军")
            win32gui.EnableMenuItem(menu, 1023, win32con.MF_GRAYED)  # 是用菜单句柄，对菜单进行操作

            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)

            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)  # 显示并获取选中的菜单
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)  # 忽略当前事件消息
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == 1023:
            # import win32gui_dialog
            win32api.MessageBox(0, "你个猪", "你真的是猪么", win32con.MB_OK)
        elif id == 1024:
            print("你好，乌克兰大白猪")
        elif id == 1025:
            print("退出程序")
            win32gui.DestroyWindow(self.hwnd)
        elif id == 1026:
            print("我好怕怕")
        else:
            print("Unknown command -", id)


def play_ico():
    root.withdraw()
    cio_thread = threading.Thread(target=god)
    cio_thread.daemon = True
    cio_thread.start()


def god():
    app = MainWindow()


def main():
    root.title("我靠")
    btn = Button(root, command=play_ico)
    btn.grid()
    global wmp
    wmp = Dispatch("WMPlayer.OCX")

    canvas = Canvas(root, width=150, height=100, bg="blue")
    filename = PhotoImage(file="girl.gif")
    image = canvas.create_image((0, 0), image=filename)
    canvas.place(x=0, y=0)
    canvas.coords(image, 79, 50)
    canvas.grid(row=0, column=0, sticky="nw", rowspan=2)

    progress_lab = LabelFrame(root, text="播放进度")
    progress_lab.grid(row=2, column=0, sticky="we", rowspan=2)
    var_scale = DoubleVar()
    global progress_scal
    progress_scal = Scale(progress_lab, orient=HORIZONTAL, showvalue=0, length=180, variable=var_scale)
    # progress_scal.bind("<Button-1>",pause)
    # progress_scal.bind("")
    # progress_scal.bind("<ButtonRelease-1>",play)
    progress_scal.grid(row=3, column=0)

    modee_lab = LabelFrame(root, text="播放模式")
    modee_lab.grid(row=4, column=0, rowspan=4, sticky="ws")
    var_mode = IntVar()
    randomradio = Radiobutton(modee_lab, variable=var_mode, value=1, text="随机播放", command=List_random)
    randomradio.grid(row=4, column=2)
    inturnradio = Radiobutton(modee_lab, variable=var_mode, value=2, text="顺序播放", command=play)
    inturnradio.grid(row=4, column=3)
    alloop = Radiobutton(modee_lab, variable=var_mode, value=2, text="全部循环播放", command=List_loop)
    alloop.grid(row=5, column=2)
    sinloop = Radiobutton(modee_lab, variable=var_mode, value=3, text="单曲循环播放")
    sinloop.grid(row=5, column=3)
    previous_play = Button(modee_lab, text="上一曲", height=1, command=Previous_it)
    previous_play.grid(row=6, column=2, rowspan=2, pady=5)
    next_play = Button(modee_lab, text="下一曲", height=1, command=Next_it)
    next_play.grid(row=6, column=3, rowspan=2, pady=5)

    var_volume = IntVar()
    vioce_lab = LabelFrame(root, text="音量控制")
    vioce_lab.grid(row=8, column=0, sticky="wes")
    global vio_scale
    vio_scale = Scale(vioce_lab, orient=HORIZONTAL, length=170, variable=var_volume, command=Volume_ctr)
    vio_scale.set(30)
    vio_scale.grid(row=8, column=0)
    vio_plus = Button(vioce_lab, width=8, text="增加音量+", command=Volume_add)
    vio_plus.grid(row=9, column=0, sticky="w")
    vio_minus = Button(vioce_lab, width=8, text="减少音量-", command=Volume_minus)
    vio_minus.grid(row=9, column=0, sticky="e")

    ctr_lab = LabelFrame(root, text="播放控制", height=130)
    ctr_lab.grid(row=0, column=1, rowspan=12, sticky="ns")
    btn_open = Button(ctr_lab, text="打开音乐文件", width=10, command=openfile)
    btn_open.grid(row=0, column=1)
    btn_play = Button(ctr_lab, text="播放", width=10, command=play)
    btn_play.grid(row=1, column=1, pady=5)
    btn_stop = Button(ctr_lab, text="停止", width=10, command=stop)
    btn_stop.grid(row=2, column=1, pady=5)
    btn_pause = Button(ctr_lab, text="暂停", width=10, command=pause)
    btn_pause.grid(row=3, column=1, pady=5)

    btn_playlist = Button(ctr_lab, text="新建播放列表", width=10, command=list_new)
    btn_playlist.grid(row=4, column=1, pady=5)

    listimport = Button(ctr_lab, width=10, text="我的列表", height=3)
    listimport.grid(row=6, column=1, sticky="nw", pady=5, rowspan=2)

    listdel_all = Button(ctr_lab, width=10, text="清空列表", command=Clear_list)
    listdel_all.grid(row=8, column=1, sticky="nw", pady=5)
    listdel_sel = Button(ctr_lab, width=10, text="删除歌曲")
    listdel_sel.grid(row=12, column=1, sticky="nw", pady=5)
    savelist_btn = Button(ctr_lab, text="保存为列表")
    savelist_btn.grid(row=9, column=1)
    min_btn = Button(ctr_lab, text="最小化窗口", command=play_ico)
    min_btn.grid(row=13, column=1)

    time_lab = Label(root, width=20, height=2, text="现在时间为:")
    time_lab.grid(row=12, column=0, sticky="nw", pady=5)
    time_text = Text(root, width=30, height=3, foreground="green")
    time_text.grid(row=10, column=0, sticky="nw", pady=5)
    global list_name
    list_name = Text(root, height=18, width=110)
    list_name.grid(row=0, column=2, sticky="n", rowspan=6)
    out_file = open("info.txt", "a+")
    for line in out_file.readlines():
        line = line.strip()
        filenames.append(line)

    # filenames = tuple(filenames)
    print(filenames)
    out_file.close()
    for i in range(len(filenames)):
        media = wmp.newMedia(filenames[i])
        wmp.currentPlaylist.appendItem(media)

        # print(filenames[i])
        coco = eyed3.load((filenames[i].strip()))  # eyed3模块读取mp3信息
        total = int(coco.info.time_secs)
        minute = int(coco.info.time_secs) // 60
        sec = int(coco.info.time_secs) % 60
        length = int(coco.info.time_secs)

        name = filenames[i].split("/")

        k = index[-1]
        itemsong = str(k) + "." + name[-1] + " " * 6 + "0%s:%d" % (minute, sec) + "\n"
        if sec >= 10:
            list_name.insert(END, itemsong)
        else:
            list_name.insert(END, str(k) + "." + name[-1] + " " * 6 + "0%s:0%d" % (minute, sec) + "\n")

        k = k + 1
        index.append(k)

    root.mainloop()

    # Runs a message loop until a WM_QUIT message is received.


if __name__ == '__main__':
    main()