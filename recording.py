from Tkinter import *

import pyaudio as pa
from pyaudio import PyAudio

import pandas as pd
import threading
import wave as wv
import math
from time import sleep
import random
import struct
import numpy as np
import matplotlib.pyplot as plt


class play_sound:
    def __init__(self,BITRATE=16000,CHANNELS = 2):
        self.BITRATE = BITRATE
        self.CHANNELS = CHANNELS
        self.WAVE_DATA = ''
        
    def play_wave_data(self):
        p = PyAudio()
    
        stream = p.open(format=p.get_format_from_width(1),
                        channels=self.CHANNELS,
                        rate=self.BITRATE,
                        output=True,)
    
        stream.write(self.WAVE_DATA)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def generate_sin_wave(self, freq = 440, SECONDS = 2):
        self.WAVE_DATA = ''
        self.FREQ = freq
        self.NUMBEROFFRAMES = int(SECONDS * self.BITRATE)
        self.RESTFRAMES = self.NUMBEROFFRAMES % self.BITRATE
        for x in xrange(self.NUMBEROFFRAMES):
            self.WAVE_DATA += chr(int(math.sin(x / ((self.BITRATE / float(self.FREQ)) / math.pi)) * 127 + 128))
        for x in xrange(self.RESTFRAMES):
            self.WAVE_DATA += chr(128)
        
class record_sound:
    def __init__(self, FORMAT =  pa.paInt16 ,CHANNELS = 2, RATE = 44100, CHUNK = 1024):
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.CHUNK = CHUNK
        
    def recording(self):
        p = PyAudio()
        stream = p.open(format = self.FORMAT,
                        channels = self.CHANNELS,
                        rate = self.RATE,
                        input = True)
        frames = []
        for i in range(0, int(self.RATE / self.CHUNK)):
            data = stream.read(self.CHUNK)
            data_converted = struct.unpack(str(4 * self.CHUNK) + 'B',data)
            data_np = np.array(data_converted, dtype='b')[::2] + 128
            frames.append(data_np)
        stream.stop_stream()
        stream.close()
        p.terminate()
        return frames
    
class App:
    def __init__(self, master):
        #instance to play a wave after the wavedata was generated with generate_sin_wave
        #make sure speaker is on
        self.audio = play_sound()
        
        #instance to record data from microphone
        self.recording = record_sound()
        
        #tkinter setup
        self.frame = Frame(master)
        self.frame.pack()
        
        self.start = Button(self.frame, 
                         text = "START",
                         fg = "green",
                         command = self.start_recording)
        self.start.pack(side=LEFT)
        
        self.stop = Button(self.frame,
                         text = "STOP",
                         fg = "red",
                         command=self.stop_recording)
        self.stop.pack(side=LEFT)

    def stop_recording(self):
        self.frame.quit()
        
        
    def start_recording(self):
        df = pd.DataFrame({"sound_data":[], "frequency":[]})
        number_of_frequnces = 30
        number_of_data_per_frequence = 15
        for _ in range(number_of_frequnces):
            freq = random.uniform(80,1200)
            self.audio.generate_sin_wave(freq = freq, SECONDS = 4)
            self.audio_thread = threading.Thread(target = self.audio.play_wave_data)
            self.audio_thread.start()
            #time makes sure that audio is playing
            sleep(0.1)
            for frame in self.recording.recording()[:number_of_data_per_frequence]:                
                datapoint = pd.DataFrame({"sound_data":[frame], "frequency":[freq]}) 
                df = df.append(datapoint,ignore_index=True)
            
            self.audio_thread.join()
        df.to_csv(r'./data/data_26_Juli.csv', index = None, header=True)
                

root = Tk()
app = App(root)
root.mainloop()