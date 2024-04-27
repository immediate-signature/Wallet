import main
import tkinter

# functionality
def get_data():
    box.get()
    p=password.get()

    print(p)

class Login:
    def __init__(self, root):
        self.window = root
        root.title('Log-in')

root = tkinter.Tk()
#root setting
window_width = 1280
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
title = tkinter.Label(text="Log in ", font=("Impact",35, "bold"), fg="#FC581F").place(x=100,y=80) #make it cventer 3can make it any font I want
box = tkinter.Entry(root,width=25, font=('Assisstant',11, 'bold'),bd=0,)
box.place(x=580, y=200)

password = tkinter.Entry(root,width=25, font=('Assisstant',11, 'bold'),bd=0)
password.place(x=580, y=240)
password.config(show='*')

send = tkinter.Button(text="next",justify="center",font=("impact",10,"bold"),bd=0, command=get_data)
send.place(x=580, y=300)
obj = Login(root)
root.mainloop()


