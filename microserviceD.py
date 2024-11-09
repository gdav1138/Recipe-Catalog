import time

import zmq

from tkinter import *
from tkinter import messagebox

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1138")

while True:
    timeRequest = socket.recv()
    timeRequest = timeRequest.decode("utf-8")
    if timeRequest.isdigit():
        root = Tk()
        root.geometry("300x250")
        root.title("Timer")

        hour = StringVar()
        minute = StringVar()
        second = StringVar()

        hour.set("00")
        minute.set(timeRequest)
        second.set("00")

        minuteLabel = Label(root, text="Minutes")
        minuteLabel.place(x=80, y=10)
        minuteEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=minute)
        minuteEntry.place(x=80, y=40)
        secondLabel = Label(root, text="Seconds")
        secondLabel.place(x=130, y=10)
        secondEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=second)
        secondEntry.place(x=130, y=40)

        temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
        while temp > -1:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)

            hour.set("{0:2d}".format(hours))
            minute.set("{0:2d}".format(mins))
            second.set("{0:2d}".format(secs))

            root.update()
            time.sleep(1)

            if (temp == 0):
                messagebox.showinfo("Timer", "Time's up!")
            temp -= 1
        root.mainloop()
    else:
        pass