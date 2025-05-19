"""The beginning of something beautiful or terrible"""

# Importing libraries
import tkinter as tk
from tkinter import ttk
import random



class Game(tk.Tk):
    """Initilising Main window as a class"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        """using the innit function create the necesserary
        widgets when the class 'Game' is called"""
        
        self.wm_title("Clicker game")
        self.wm_geometry("1200x800")

        # creating a container as a frame
        container = tk.Frame(self, height=800, width=1200)

        container.pack(side="top", fill="both", expand=True)

        # configuring the location of container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of Frames
        self.frames = {}

        for F in (MainPage, SettingMenu):
            """So, I will use a for loop to initallise these
            class as frames so that they be raise and unraise
            like pages"""
            frame = F(container, self)

            # the Game class act as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        # Calling a function to switch page, and also let the main page be first
        self.show_frame(MainPage)

    def show_frame(self, cont):
        """This function find the frame in the dictionary 
        and raise it to the top"""
        frame = self.frames[cont]
        frame.tkraise()




class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        #intialise the class as a frame
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text= "Main Menu")
        label.pack(padx=10, pady=10)

        # button to switch frame, using lambda function to call show_frame()
        switch_window_button = tk.Button(
            self,
            text="Go to Setting",
            command=lambda: controller.show_frame(SettingMenu)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)



    def start():
        pass
    pass

class SettingMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # title of setting
        label = tk.Label(self, text="This is Setting menu")
        label.pack(padx=10, pady=10)

        # Button switch to main menu
        switch_window_button = tk.Button(
            self,
            text="Go to back to Main Menu",
            command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

    def quit():
        pass
    
    pass


class HelpMenu(tk.Frame):
    pass


class AboutMenu(tk.Frame):
    pass

if __name__ == "__main__":
    root = Game()
    root.mainloop()