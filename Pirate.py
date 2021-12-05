import os
from tkinter import *

fen = Tk()
can = Canvas(fen,width=300,height=168)
photo = PhotoImage("/Users/Shared/programmes/William/Python/piratage/windowsLogin.jpg")
background = can.create_image(300,168,image=photo)
can.pack()
ip=os.popen("ifconfig |grep inet").readlines()
ip=ip[4][6:17]
print(ip)

mainloop()
fen.destroy()
