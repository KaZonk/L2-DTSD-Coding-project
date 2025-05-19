"""The beginning of something beautiful or terrible"""

# Importing libraries
import tkinter as tk
from tkinter import ttk
import random

# Temporary useful link: https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes

class Game(tk.Tk):
    """Initilising Main window as a class"""
    def __init__(self, *args, **kwargs):
        """using the innit function create the necesserary
        widgets when Game is called"""
        
        self.wm_title("Click ball game")

        # creating a container as a frame
        container = tk.Frame(self, height=400, width=600)

        container.pack(side="top", fill="both", expand=True)

        # configuring the location of container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of Frames
        self.frames = {}

        for F in (MainPage, SettingMenu, HelpMenu, AboutMenu):
            """So, I will use a for loop to initallise these
            class as frames so that they be raise and unraise
            like pages"""
            pass




class MainPage():
    def __init__(self):
        pass

    def start():
        pass
    pass

class SettingMenu():
    def __init__(self):
        pass

    def quit():
        pass
    
    pass

class HelpMenu():
    pass

class AboutMenu():
    pass

if __name__ == "__main__":
    pass