from tkinter import *
import time

def tick():
    time_string = time.strftime("%H:%M:%S")
    clock.config(text=time_string)
    clock.after(200, tick)

root = Tk()
clock = Label(root, font=("times", 50, "bold"), bg= "black", fg = "white")
clock.grid(row=0, column=0)
tick()

root.configure(background='black')
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen',True)

root.wm_attributes("-topmost", 1)
root.focus_set()

root.bind("<Escape>", lambda event:root.destroy())
root.after(10000, root.destroy)

root.mainloop()
