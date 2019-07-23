from Tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.button = Button(frame, 
                         text = "START",
                         fg = "red",
                         command = frame.quit)
        self.button.pack(side=LEFT)
        self.slogan = Button(frame,
                         text = "STOP",
                         fg = "green",
                         command=self.write_slogan)
        self.slogan.pack(side=LEFT)
    

root = Tk()
app = App(root)
root.mainloop()
