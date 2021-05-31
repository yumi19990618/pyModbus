import tkinter as tk  # 使用Tkinter前需要先匯入
import tkinter.messagebox
import pickle
import matplotlib.pyplot as plt
import time
from pyModbusTCP.client import ModbusClient

# 第1步，例項化object，建立視窗window
window = tk.Toplevel()

# 第2步，給視窗的視覺化起名字
window.title('Wellcome to MODBUS TCP test')

# 第3步，設定視窗的大小(長 * 寬)
window.geometry('800x600')  # 這裡的乘是小x

# 第4步，載入 wellcome image
canvas = tk.Canvas(window, width=450, height=300, bg='white') #
image_file = tk.PhotoImage(file='pic.gif')
image = canvas.create_image(200, 0, anchor='n', image=image_file)
canvas.pack(side='top')
tk.Label(window, text='Wellcome',font=('Comic Sans MS', 20)).pack()

# 第5步，使用者資訊
tk.Label(window, text='User name:', font=('Comic Sans MS', 14)).place(x=220, y=345)
tk.Label(window, text='Password:', font=('Comic Sans MS', 14)).place(x=220, y=380)

# 第6步，使用者登入輸入框entry
# 使用者名稱
var_usr_name = tk.StringVar()
#var_usr_name.set('graph@test.com')
var_usr_name.set('123321')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name, font=('Comic Sans MS', 14))
entry_usr_name.place(x=340,y=350)
# 使用者密碼
var_usr_pwd = tk.StringVar()
var_usr_pwd.set('456654')
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, font=('Comic Sans MS', 14), show='·')
entry_usr_pwd.place(x=340,y=385)

# 第8步，定義使用者登入功能
def usr_login():
    # 這兩行程式碼就是獲取使用者輸入的usr_name和usr_pwd
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    # 這裡設定異常捕獲，當我們第一次訪問使用者資訊檔案時是不存在的，所以這裡設定異常捕獲。
    # 中間的兩行就是我們的匹配，即程式將輸入的資訊和檔案中的資訊匹配。
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        # 這裡就是我們在沒有讀取到`usr_file`的時候，程式會建立一個`usr_file`這個檔案，並將管理員
        # 的使用者和密碼寫入，即使用者名稱為`admin`密碼為`admin`。
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            usr_file.close()    # 必須先關閉，否則pickle.load()會出現EOFError: Ran out of input

    # 如果使用者名稱和密碼與檔案中的匹配成功，則會登入成功，並跳出彈窗how are you? 加上你的使用者名稱。
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            HOST = "140.123.92.109"
            PORT = 502
            
            client=ModbusClient()
            
            client.host(HOST)
            client.port(PORT)
            x=[]
            y=[]
            n=1
            while True:
                 if not (client.is_open() or client.open() )  :
                     print("can't connect to " +HOST+ ":" +str(PORT))
                 
                 if client.is_open():
                    print("connect is ok")
                    regs = client.read_input_registers(0x2100,1)
                    if regs:
                        for a in regs:
                            x.append(n)
                            y.append(a/10) 
                            plt.plot(x,y,color="#a73dd1")
                            plt.xlabel("Time(s)")
                            plt.ylabel("Volt")
                            plt.title("PA3000 MODBUS")
                 n=n+1
                 plt.show()
                 time.sleep(1)
                 if n==61:
                     break
                
        # 如果使用者名稱匹配成功，而密碼輸入錯誤，則會彈出'Error, your password is wrong, try again.'
        else:
            tkinter.messagebox.showerror(message='Error, your password is wrong, try again.')
            
    else:  # 如果發現使用者名稱不存在
        is_sign_up = tkinter.messagebox.askyesno('Welcome！ ', 'You have not Register yet. Register now?')
        # 提示需不需要註冊新使用者
        if is_sign_up:
            usr_register()

# 第9步，定義使用者註冊功能
def usr_register():
    def sign_to_Hongwei_Website():
        # 以下三行就是獲取我們註冊時所輸入的資訊
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        # 這裡是開啟我們記錄資料的檔案，將註冊資訊讀出
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        # 這裡就是判斷，如果兩次密碼輸入不一致，則提示Error, Password and confirm password must be the same!
        if np != npf:
            tkinter.messagebox.showerror('Error', 'Password and confirm password must be the same!')

        # 如果使用者名稱已經在我們的資料檔案中，則提示Error, The user has already signed up!
        elif nn in exist_usr_info:
            tkinter.messagebox.showerror('Error', 'The user has already signed up!')

        # 最後如果輸入無以上錯誤，則將註冊輸入的資訊記錄到檔案當中，並提示註冊成功Welcome！,You have successfully signed up!，然後銷燬視窗。
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            # 然後銷燬視窗。
            window_sign_up.destroy()

    # 定義長在視窗上的視窗
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('600x500')
    window_sign_up.title('Register window')

    new_name = tk.StringVar()  # 將輸入的註冊名賦值給變數
    new_name.set('graph@test.com')  # 將最初顯示定為'graph@test.com'
   # entry_usr_name = tk.Entry(window, textvariable=new_name, font=('Comic Sans MS', 14))
    tk.Label(window_sign_up, text='User name: ',font=('Comic Sans MS', 12)).place(x=160, y=10)  # 將`User name:`放置在座標（10,10）。
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name,font=('Comic Sans MS', 12))  # 建立一個註冊名的`entry`，變數為`new_name`
    entry_new_name.place(x=310,y=15)  # `entry`放置在座標（150,10）.

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ',font=('Comic Sans MS', 12)).place(x=160, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd,font=('Comic Sans MS', 12))#, show='*'
    entry_usr_pwd.place(x=310,y=55)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ', font=('Comic Sans MS', 12)).place(x=160, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm,font=('Comic Sans MS', 12))#, show='*'
    entry_usr_pwd_confirm.place(x=310,y=95)

    # 下面的 sign_to_Hongwei_Website
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Register', command=sign_to_Hongwei_Website, font=('Comic Sans MS', 12))
    btn_comfirm_sign_up.place(x=250,y=140)

# 第7步，login and Register 按鈕
btn_login = tk.Button(window, text='Login', command=usr_login,font=('Comic Sans MS', 14))
btn_login.place(x=320, y=425)
btn_sign_up = tk.Button(window, text='Register', command=usr_register,font=('Comic Sans MS', 14))
btn_sign_up.place(x=420, y=425)

# 第10步，主視窗迴圈顯示
window.mainloop()