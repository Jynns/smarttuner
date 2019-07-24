from Tkinter import *
import pyaudio as pa


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.start = Button(frame, 
                         text = "START",
                         fg = "green",
                         command = self.start_recording)
        self.start.pack(side=LEFT)
        
        self.stop = Button(frame,
                         text = "STOP",
                         fg = "red",
                         command=self.stop_recording)
        self.stop.pack(side=LEFT)

    def stop_recording(self):
        print("stop")

    def start_recording(self):
        print("start")
    

root = Tk()
app = App(root)
root.mainloop()
