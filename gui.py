import json
import tkinter
import winreg
from tkinter import messagebox

import script
import server


def back_to_homepage():
    root = tkinter.Tk()
    obj = Homepage(root)
    root.mainloop()


def size(root):
    # root setting
    window_width = 1280
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    return f'{window_width}x{window_height}+{center_x}+{center_y}'


class Signup:
    def __init__(self, root):
        self.root = root
        self.root.title('SignUp')
        self.root.geometry(size(self.root))

        # stylistic elements:
        title = tkinter.Label(text="Sign Up", font=("Impact", 35, "bold"), fg="#FC581F").place(x=100, y=80)
        usertext = tkinter.Label(text="Username", font=("Assistant", 20, 'bold'), fg="#FC581F").place(x=100, y=150)
        self.username = tkinter.Entry(bd=0)
        self.username.place(x=100, y=200)
        passtext = tkinter.Label(text="password", font=("Assistant", 20, 'bold'), fg="#FC581F").place(x=100, y=300)
        self.password = tkinter.Entry(bd=0)
        self.password.place(x=100, y=350)
        self.password.config(show='*')
        passtext2 = tkinter.Label(text="confirm password", font=("Assistant", 20, 'bold'), fg="#FC581F").place(x=100,
                                                                                                               y=370)
        self.password2 = tkinter.Entry(bd=0)
        self.password2.place(x=100, y=400)
        self.password2.config(show='*')

        send = tkinter.Button(text="sign me up", justify="center", font=("impact", 10, "bold"), bd=0,
                              command=self.register)
        send.place(x=400, y=100)

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


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry(size(self.root))

        title = tkinter.Label(text="Login", font=("Impact", 35, "bold"), fg="#FC581F").place(x=100, y=80)
        usertext = tkinter.Label(text="Username", font=("Assistant", 20, 'bold'), fg="#FC581F").place(x=100, y=150)
        self.username = tkinter.Entry(bd=0)
        self.username.place(x=100, y=200)
        passtext = tkinter.Label(text="password", font=("Assistant", 20, 'bold'), fg="#FC581F").place(x=100, y=300)
        self.password = tkinter.Entry(bd=0)
        self.password.place(x=100, y=350)
        self.password.config(show='*')
        next = tkinter.Button(text="connect", justify="center", font=("impact", 10, "bold"), bd=0,
                              command=self.validate)
        next.place(x=400, y=400)

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


class Send:
    def __init__(self, root):
        self.root = root
        self.root.title('wallet')
        self.root.geometry(size(self.root))

        text = tkinter.Label(text="destination").place(x=80, y=100)
        self.dest = tkinter.Entry()
        self.dest.place(x=80, y=120)

        text = tkinter.Label(text="amount").place(x=80, y=150)
        self.amount = tkinter.Entry()
        self.amount.place(x=80, y=170)

        send = tkinter.Button(text="send", command=self.make)
        send.place(x=80, y=200)

        back = tkinter.Button(text='back', command=self.back_to_homepage)
        back.place(x=80, y=230)

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

            text.insert('1.0',chars="the signed raw transaction is: " + signed)
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
        self.root.geometry(size(self.root))

        text = tkinter.Label(text="please copy the tx, make sure there isn't a mistake").place(x=80, y=100)
        self.src = tkinter.Entry()
        self.src.place(x=80, y=120)

        send = tkinter.Button(text="send", command=self.make)
        send.place(x=80, y=200)

        back = tkinter.Button(text="back", command=self.back_to_homepage)
        back.place(x=80, y=230)

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


class Homepage:
    def __init__(self, root):
        self.root = root
        self.root.title('wallet')
        self.root.geometry(size(self.root))

        amount = str(json.loads(server.rpc_call('-rpcwallet="wallet" getbalance')))  # get balance

        title = tkinter.Label(text="Hello", font=("Impact", 35, "bold"), fg="#FC581F").place(x=100, y=80)
        title = tkinter.Label(text="Balance:" + amount, font=("Impact", 35, "bold"), fg="#FC581F").place(x=100, y=130)

        addresses = server.rpc_call(r'-rpcwallet="wallet" getaddressesbylabel ""')
        add_list = json.loads(addresses)
        add_list = json.dumps(add_list)
        addresses = tkinter.Label(text="my addresses:").place(x=100, y=400)
        addresses = tkinter.Label(text=add_list).place(x=100, y=430)

        send = tkinter.Button(text="send bitcoin", command=self.send)
        send.place(x=100, y=200)

        sign = tkinter.Button(text="sign a transaction", command=self.sign)
        sign.place(x=400, y=200)

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