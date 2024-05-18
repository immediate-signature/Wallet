import json
import tkinter
import winreg
from tkinter import messagebox
from pathlib import Path

import scraping
import script
import server
import pyperclip

PATH = str(Path.home()) + r'\PycharmProjects\Wallet\UI'

def back_to_homepage():
    root = tkinter.Tk()
    obj = Homepage(root)
    root.mainloop()


def size(root, window_width=964, window_height=606):
    # root setting
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    return f'{window_width}x{window_height}+{center_x}+{center_y}'

class Phrase:
    def __init__(self, root, mnemonic_phrase):
        self.root = root
        self.root.title('wallet')
        self.root.geometry(size(self.root))

        title = tkinter.Label(text="your mnemonic phrase is: ", font=("Impact", 35, "bold"), fg="#FC581F").place(x=100,
                                                                                                                 y=80)
        title = tkinter.Label(text=mnemonic_phrase, font=("Impact", 35, "bold"), fg="#FC581F").place(x=100, y=120)
        title = tkinter.Label(text="please do not share this information", font=("Impact", 35, "bold"),
                              fg="#FC581F").place(x=100, y=500)

        next = tkinter.Button(text="next", justify="center", font=("impact", 10, "bold"), bd=0,
                              command=self.back_to_homepage)
        next.place(x=400, y=400)

        return

    def back_to_homepage(self):
        self.root.destroy()
        window = tkinter.Tk()
        obj = Homepage(window)
        window.mainloop()

class Popup:
    def __init__(self, root, text):
        self.root = root
        self.root.title('success')
        self.root.geometry('800x600')

        message =tkinter.Label(text=text).place(x=100, y=430)

class Homepage:
    def __init__(self, root):
        self.root = root
        self.root.title('wallet')
        self.root.geometry(size(self.root))

        self.bg = tkinter.PhotoImage(file=PATH +r'\pasted image edited.png')
        self.canvas1 = tkinter.Canvas(self.root,width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas1.pack(fill="both",expand=True)
        self.canvas1.create_image(0,0,image=self.bg, anchor="nw")

        amount = round(json.loads(server.rpc_call('-rpcwallet="wallet" getbalance')),2)
        self.canvas1.create_text(130, 150, text=str(amount) + ' BTC' ,font=("Roboto", 20, "bold"), fill="#FFFFFF")
        btc_amount = str(round(float(amount) * float(scraping.get_rate()),2))
        self.canvas1.create_text(370, 150, text=btc_amount + '$', font=("Roboto", 20, "bold"), fill="#444444", justify="center")

        send = tkinter.Button(text="send", font = ("Roboto",35, "bold"), command=self.send, fg="#FFFFFF",bg="#444444", bd=0)
        send.place(x=200, y=305)


        sign = tkinter.Button(text="recieve", font = ("Roboto",35, "bold"), command=self.sign, fg="#FFFFFF",bg="#444444", bd=0)
        sign.place(x=580, y=300)

        self.me = json.dumps(json.loads(server.rpc_call(r'-rpcwallet="wallet" getaddressesbylabel ""')))[2:36]
        button= tkinter.Button(text=self.me, font=("Roboto", 10, "bold"), fg="#444444", background="#FFFFFF", justify="center",command=self.copy,bd=0)
        button.place(x=350,y=500)

        return

    def send(self):
        self.root.destroy()
        window = tkinter.Tk()
        obj = Send(window)
        window.mainloop()

    def sign(self):
        self.root.destroy()
        window = tkinter.Tk()
        obj = Sign(window)
        window.mainloop()

    def copy(self):
        pyperclip.copy(self.me)
        return




class Login:
    def __init__(self,root):
        self.root = root
        self.root.title('Login')
        self.root.geometry(size(self.root,1200,650))

        self.bg = tkinter.PhotoImage(file= PATH+ r"\login.png")
        self.canvas1 = tkinter.Canvas(self.root, width=self.root.winfo_screenwidth(),
                                      height=self.root.winfo_screenheight())
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.username = tkinter.Entry(bd=0)
        self.username.place(x=270, y=280)

        self.password = tkinter.Entry(bd=0)
        self.password.place(x=270, y=360)
        self.password.config(show='*')
        next = tkinter.Button(text="log in", justify="center", font=("Roboto", 10, "bold"), bd=0, bg="#444444", fg="#FFFFFF",
                              command=self.validate)
        next.place(x=298, y=565)

        return

    def validate(self):
        h = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'bitWallet')
        username = winreg.QueryValueEx(h, "username")[0]
        password = winreg.QueryValueEx(h, "password")[0]
        h.Close()
        if (self.username.get() != username or self.password.get() != password):
            messagebox.showerror("Error", "Error: wrong credentials")
        else:
            self.root.destroy()
            back_to_homepage()

class Signup:
    def __init__(self,root):
        self.root = root
        self.root.title('Sign up')
        self.root.geometry(size(self.root,1200,650))

        self.bg = tkinter.PhotoImage(file=PATH+r"\signup.png")
        self.canvas1 = tkinter.Canvas(self.root, width=self.root.winfo_screenwidth(),
                                      height=self.root.winfo_screenheight())
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.username = tkinter.Entry(bd=0)
        self.username.place(x=270, y=280)

        self.password = tkinter.Entry(bd=0)
        self.password.place(x=270, y=360)
        self.password.config(show='*')

        self.password = tkinter.Entry(bd=0)
        self.password.place(x=270, y=430)
        self.password.config(show='*')
        next = tkinter.Button(text="sign up", justify="center", font=("Roboto", 10, "bold"), bd=0, bg="#444444", fg="#FFFFFF",
                              command=self.register)
        next.place(x=285, y=565)

        return

    def register(self):
        if (self.password2.get() == '' or self.password.get() == '' or self.username.get() == ''):
            return messagebox.showerror("Error", "Error: missing")
        if (self.password2.get() != self.password.get()):
            return messagebox.showerror("Error", "Error: mismatch")
        else:
            data = self.username.get() + '\n' + self.password.get()
            h = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'bitWallet')
            winreg.SetValueEx(h, 'username', 0, winreg.REG_SZ, self.username.get())
            winreg.SetValueEx(h, 'password', 0, winreg.REG_SZ, self.password.get())
            self.root.destory()


class Send:
    def __init__(self, root):
        self.root = root
        self.root.title('wallet')
        self.root.geometry(size(self.root,1210,650))

        self.bg = tkinter.PhotoImage(file=PATH+r"\transfer.png")
        self.canvas1 = tkinter.Canvas(self.root, width=self.root.winfo_screenwidth(),
                                      height=self.root.winfo_screenheight())
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.dest = tkinter.Entry(bd=0)
        self.dest.place(x=260, y=280)

        self.amount = tkinter.Entry(bd=0)
        self.amount.place(x=260, y=360)

        send = tkinter.Button(text="transfer", command=self.make, bd=0, bg="#444444",fg="#FFFFFF", font=("Roboto",12,"bold"))
        send.place(x=284, y=566)

        back = tkinter.Button(text='cancel', command=self.back_to_homepage, bg="#EBEBEB", fg="#444444", font=("Roboto",12,"bold"), bd=0)
        back.place(x=430, y=566)

        return

    def make(self):
        if self.amount.get() == '' or self.dest.get() == '':
            return messagebox.showerror("Error", "please fill out all of the fields")
        amount = self.amount.get()
        dest = self.dest.get()
        tx = script.transaction(int(amount), dest)
        if tx == 'error':
            return messagebox.showerror("Error", "You don't have enough BTC to make this transaction")
        else:
            tx = str(tx)[2:-5]
            signed = script.sign(tx)
            signed = json.loads(signed)["hex"]

            window2 = tkinter.Toplevel()
            window2.title("success")
            window2.geometry("600x400")
            text = tkinter.Text(window2)

            text.insert('1.0', chars="the signed raw transaction is: " + signed)
            text['state'] = 'disabled'
            text.pack()
            window2.mainloop()

            self.root.destroy()
            window = tkinter.Tk()
            obj = Homepage(window)
            window.mainloop()

    def back_to_homepage(self):
        self.root.destroy()
        window = tkinter.Tk()
        obj = Homepage(window)
        window.mainloop()

class Sign:
    def __init__(self, root):
        self.root = root
        self.root.title('wallet')
        self.root.geometry(size(self.root,1000,650))

        self.bg = tkinter.PhotoImage(file=PATH+r"\sign.png")
        self.canvas1 = tkinter.Canvas(self.root, width=self.root.winfo_screenwidth(),
                                      height=self.root.winfo_screenheight())
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.src = tkinter.Entry(bd=0)
        self.src.place(x=260, y=350)


        send = tkinter.Button(text="transfer", command=self.make, bd=0, bg="#444444",fg="#FFFFFF", font=("Roboto",12,"bold"))
        send.place(x=270, y=540)

        back = tkinter.Button(text='cancel', command=self.back_to_homepage, bg="#EBEBEB", fg="#444444", font=("Roboto",12,"bold"), bd=0)
        back.place(x=410, y=540)

        return

    def make(self):
        src = self.src.get()
        tx = script.sign(src)
        tx = str(json.loads(tx)["hex"])
        print(tx)
        signed = script.sign(tx)
        signed = json.loads(signed)["hex"]
        print(signed)
        num = script.send(signed)
        print(num)


        self.root.destroy()
        window = tkinter.Tk()
        obj = Homepage(window)
        window.mainloop()

    def back_to_homepage(self):
        self.root.destroy()
        window = tkinter.Tk()
        obj = Homepage(window)
        window.mainloop()
