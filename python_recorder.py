import os, sys
import tkinter
from tkinter import StringVar, ttk, filedialog
import webbrowser

import pyaudio
import wave
import shutil

audio = pyaudio.PyAudio()

#===============global変数宣言======================
empty_namelist = []
empty_namelist2 = []
stop = False

#フォルダー設定関数
def searchfolder():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    entry1.set(iDirPath)

def ScanInputMonitor():

    for i in range(audio.get_device_count()):
        dev = audio.get_device_info_by_index(i)
        print(dev['name'], end=':')
        print(dev['hostApi'], end=':')
        print(dev['index'])
        
        if dev['hostApi'] == 0:
            empty_namelist.append(dev['name'])
            
            if dev['maxInputChannels'] > 0:
                empty_namelist2.append(dev['name'])

def select_device(self):
        name = v.get()
        global device_num

        for i in range(len(empty_namelist)):
            if name == empty_namelist[i]:
                device_num = i
                #print(device_num)
                break

# 録音開始関数
def recording():
    Button2["state"] = "disable"
    Button3["state"] = "normal"

    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    
    global stop
    stop = False

    frames = []

    # 音の取込開始
    stream = audio.open(format=FORMAT,
                         channels=CHANNELS,
                         input_device_index=device_num,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)
    
    while stop == False:
        data = stream.read(CHUNK)
        frames.append(data)
        #print("* recording")
        root.update()


    stream.close()

    fname = entry2.get()
    dname = entry1.get()
    wf = wave.open(fname + '.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    shutil.move(fname + '.wav', dname)
    #print(dname + fname + '.wav')


#録音停止関数
def stop_rec():
    Button2["state"] = "normal"
    Button3["state"] = "disable"

    global stop
    stop = True

#==================Window作成関数====================
#Main Windowの作成
def construct_mainwindow():
    # メインウィンドウ
    global root
    root = tkinter.Tk()
    root.title(u"Pythonサウンドレコーダ")
    root.iconbitmap('images/favicon.ico')
    root.geometry("550x300")

    #Menuバーの作成
    menubar = tkinter.Menu(root)

    root.config(menu=menubar)

    menu_file = tkinter.Menu(menubar, tearoff = False)
    menu_file.add_command(label = "バージョン情報",  command = show_version)
    menu_file.add_command(label = "開発者情報", command = show_inventer)
    menu_file.add_separator()
    menu_file.add_command(label = "終了", command = root.destroy)

    menubar.add_cascade(label="設定", menu = menu_file)

    # 保存ファイルフレーム内定義
    frame1 = tkinter.LabelFrame(root,text="保存ファイル",foreground="Green")

    f0 = tkinter.Frame(frame1)

    label_1 = tkinter.Label(f0, text='フォルダー')
    label_1.pack(fill = 'x', padx=10, pady= 5,  side = 'left')

    
    global entry1 #フォルダ名グローバル変数
    entry1 = StringVar()
    folder_name = tkinter.Entry(f0,textvariable=entry1, width=40)
    folder_name.insert(0, os.path.abspath(os.path.dirname(__file__)+ "/output"))
    folder_name.pack(fill = 'x', padx=10, pady= 5, side = 'left')

    Button1 = tkinter.Button(f0, text="参照", width=5, command=searchfolder)
    Button1.pack(fill = 'x', padx=10, side = 'left')

    f1 = tkinter.Frame(frame1)
    label_2 = tkinter.Label(f1, text='ファイル名')
    label_2.pack(fill = 'x', padx=10, pady= 5, side = 'left')

    global entry2 #ファイル名グローバル変数
    entry2 = StringVar()
    file_name = tkinter.Entry(f1, textvariable=entry2, width=40)
    file_name.insert(0, "Sample")
    file_name.pack(fill = 'x', padx=10, pady= 5, side = 'left')

    f2 = tkinter.Frame(frame1)
    label_3 = tkinter.Label(f2, text='　　　')
    label_3.pack(fill = 'x', padx=10, pady= 5, side = 'left')

    f0.pack()
    f1.pack()
    f2.pack()
    frame1.pack()

    #inputMonitorや録音・停止ボタンのフレーム内定義
    frame2 = tkinter.Frame(root)

    f3 = tkinter.Frame(frame2)

    #ラベル1の作成
    label_4 = tkinter.Label(f3, text='InputMonitor').grid(row=0, column=0, pady=10)

    global device_num #録音デバイスのナンバーのグローバル変数
    device_num = 0
    global v

    #コンボボックスの作成と配置
    v = StringVar()
    pulldown_list = empty_namelist2
    combobox = ttk.Combobox(f3, width=50, values=pulldown_list,textvariable=v, state="readonly")  

    combobox.set(pulldown_list[0])
    combobox.bind('<<ComboboxSelected>>', select_device)
    combobox.grid(row=0, column=1)

    f4 = tkinter.Frame(frame2)

    global Button2
    Button2 = tkinter.Button(f4,text="録音",width=20, height=5, bg="gray", fg="white", command=recording)
    Button2.pack(fill = 'x', padx=10, side = 'left') 

    global Button3
    Button3 = tkinter.Button(f4,text="停止",width=20, height=5, bg="gray", fg="red", state="disable", command=stop_rec)
    Button3.pack(fill = 'x', padx=10, side = 'left') 

    f3.pack()
    f4.pack()
    frame2.pack()

    # アプリの待機
    root.mainloop()

#バージョン情報表示関数
def show_version():
    construct_subwindow("バージョン情報", "1.0.0", "None", 0)

#開発者表示関数
def show_inventer():
    construct_subwindow("開発者", "teslasand0987", "https://github.com/teslasand0987", 1)

#サブウィンドウ用クリック処理
def subclicked():
    webbrowser.open('https://github.com/teslasand0987')

#サブウィンドウ生成関数
def construct_subwindow(title, info, url, flag):
    sub_win = tkinter.Toplevel()
    sub_win.geometry("300x80")
    label_sub = tkinter.Label(sub_win, text=title)
    label_sub2 = tkinter.Label(sub_win, text=info)

    if flag == 1:
        Button1 = tkinter.Button(sub_win,text=url,command=subclicked)

    label_sub.pack()
    label_sub2.pack()

    if flag == 1:
        Button1.pack()


#==================Main処理==========================
def main():

    ScanInputMonitor()
    construct_mainwindow()



if __name__ == "__main__":
    main()
