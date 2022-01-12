import os, sys, time
import tkinter as tk
from tkinter import StringVar, ttk, filedialog

import webbrowser
import pyaudio
import wave
import shutil

class Application(tk.Frame):

    #メインウィンドウ生成コンストラクタ
    def __init__(self, master = None):
        super().__init__(master)

        self.audio = pyaudio.PyAudio()

        #クラス内で使う共有変数宣言
        self.empty_namelist = []
        self.empty_namelist2 = []
        self.device_num = 0
        self.entry1 = StringVar()
        self.entry2 = StringVar()
        self.stop = False
        
        #windowの設定
        master.title(u"Pythonサウンドレコーダ")
        master.iconbitmap('images/favicon.ico')
        master.geometry("550x320")

        self.ScanInputMonitor()

        self.pack()
        self.create_menu()
        self.create_upperUI()
        self.create_DownnerUI()

    
    #=====================================UI設計=====================================
    #左上メニュー生成関数
    def create_menu(self):
        #Menuバーの作成
        menubar = tk.Menu(self)
        window.config(menu=menubar)

        menu_file = tk.Menu(menubar, tearoff = False)
        menu_file.add_command(label = "バージョン情報", command = self.show_version)
        menu_file.add_command(label = "開発者情報", command = self.show_inventer)
        menu_file.add_separator()
        menu_file.add_command(label = "終了", command = window.destroy)

        menubar.add_cascade(label="設定", menu = menu_file)

    #上部UIの生成関数
    def create_upperUI(self):
        # 保存ファイルフレーム内定義
        frame1 = tk.LabelFrame(self,text="保存ファイル",foreground="Green")

        f0 = tk.Frame(frame1)

        label_1 = tk.Label(f0, text='フォルダー')
        label_1.pack(fill = 'x', padx=10, pady= 5,  side = 'left')

        
        folder_name = tk.Entry(f0,textvariable=self.entry1, width=40)
        folder_name.insert(0, os.path.abspath(os.path.dirname(__file__)+ "/output"))
        folder_name.pack(fill = 'x', padx=10, pady= 5, side = 'left')

        Button1 = tk.Button(f0, text="参照", width=5,  command=self.searchfolder)
        Button1.pack(fill = 'x', padx=10, side = 'left')

        f1 = tk.Frame(frame1)
        label_2 = tk.Label(f1, text='ファイル名')
        label_2.pack(fill = 'x', padx=10, pady= 5, side = 'left')

        file_name = tk.Entry(f1, textvariable=self.entry2, width=40)
        file_name.insert(0, "Sample")
        file_name.pack(fill = 'x', padx=10, pady= 5, side = 'left')

        f2 = tk.Frame(frame1)
        label_3 = tk.Label(f2, text='　　　')
        label_3.pack(fill = 'x', padx=10, pady= 5, side = 'left')

        f0.pack()
        f1.pack()
        f2.pack()
        frame1.pack()

    #下部UIの生成関数
    def create_DownnerUI(self):
        #inputMonitorや録音・停止ボタンのフレーム内定義
        frame2 = tk.Frame(self)

        f3 = tk.Frame(frame2)

        #ラベル1の作成
        label_4 = tk.Label(f3, text='InputMonitor')
        label_4.grid(row=0, column=0, pady=10)

        #コンボボックスの作成と配置
        global v
        v = tk.StringVar() #inputMonitorの読み込み用

        pulldown_list = self.empty_namelist2
        combobox = ttk.Combobox(f3, width=50, values=pulldown_list,textvariable=v, state="readonly")  

        combobox.set(pulldown_list[0])
        combobox.bind('<<ComboboxSelected>>', self.select_device())
        combobox.grid(row=0, column=1)

        f4 = tk.Frame(frame2)

        self.Button2 = tk.Button(f4,text="録音",width=20, height=5, bg="gray", fg="white", command=self.recording)
        self.Button2.pack(fill = 'x', padx=10, side = 'left') 

        self.Button3 = tk.Button(f4,text="停止",width=20, height=5, bg="gray", fg="red", state="disable", command=self.stop_rec)
        self.Button3.pack(fill = 'x', padx=10, side = 'left') 

        f3.pack()
        f4.pack()
        frame2.pack()

    #バージョン情報表示関数
    def show_version(self):
        self.construct_subwindow("バージョン情報", "1.0.1", "None", 0)

    #開発者表示関数
    def show_inventer(self):
        self.construct_subwindow("開発者", "teslasand0987", "https://github.com/teslasand0987", 1)

    #サブウィンドウ生成関数
    def construct_subwindow(self, title, info, url, flag):
        sub_win = tk.Toplevel()
        sub_win.geometry("300x80")
        label_sub = tk.Label(sub_win, text=title)
        label_sub2 = tk.Label(sub_win, text=info)

        if flag == 1:
            Button1 = tk.Button(sub_win,text=url,command=self.subclicked)

        label_sub.pack()
        label_sub2.pack()

        if flag == 1:
            Button1.pack()

    #==========================機能処理=============================================================
    #サブウィンドウ用クリック処理
    def subclicked(self):
        webbrowser.open('https://github.com/teslasand0987')

    #inputMonitorを選ぶ関数
    def select_device(self):
        name = v.get()

        for i in range(len(self.empty_namelist)):
            if name == self.empty_namelist[i]:
                self.device_num = i
                #print(device_num)
                break

    #入力可能なデバイスを調査し配列に格納する関数
    def ScanInputMonitor(self):
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            #print(dev['name'], end=':')
            #print(dev['hostApi'], end=':')
            #print(dev['index'])
            
            if dev['hostApi'] == 0:
                self.empty_namelist.append(dev['name'])
                
                if dev['maxInputChannels'] > 0:
                    self.empty_namelist2.append(dev['name'])

    #フォルダー設定関数
    def searchfolder(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        iDirPath = filedialog.askdirectory(initialdir = iDir)
        self.entry1.set(iDirPath)

    # 録音開始関数
    def recording(self):
        self.Button2["state"] = "disable"
        self.Button3["state"] = "normal"

        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        
        self.stop = False

        frames = []

        # 音の取込開始
        stream = self.audio.open(format=FORMAT,
                            channels=CHANNELS,
                            input_device_index=self.device_num,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        
        while self.stop == False:
            data = stream.read(CHUNK)
            frames.append(data)
            #print("* recording")
            self.update()


        stream.close()

        fname = self.entry2.get()
        dname = self.entry1.get()
        wf = wave.open(fname + '.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        shutil.move(fname + '.wav', dname)
        #print(dname + fname + '.wav')

    #録音停止関数
    def stop_rec(self):
        self.Button2["state"] = "normal"
        self.Button3["state"] = "disable"

        self.stop = True



#メイン処理
def main(window):
    app = Application(master=window)
    app.mainloop()


#メイン関数実行
if __name__ == "__main__":
    window = tk.Tk()
    main(window)
