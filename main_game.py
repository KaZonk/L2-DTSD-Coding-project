"""The beginning of something beautiful or terrible"""

# Importing libraries
import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk



class Game(tk.Tk):
    """Initilising Main window as a class"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        """using the innit function create the necesserary
        widgets when the class 'Game' is called"""
        
        self.wm_title("Clicker game")
        self.wm_geometry("1200x800")
        self.resizable(False, False)

        # creating a container as a frame.
        container = tk.Frame(self, height=1200, width=800)

        container.pack(side="top", fill="both", expand=True)

        # configuring the location of container using grid.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of Frames.

        pg_class_list = [MainPage, SettingMenu, HelpMenu, 
                         AboutMenu, LeaderBoard
                         ]
        self.frames = {}

        for F in pg_class_list:
            """Using a for loop to call the classes as a frame
            and then assign to an object."""
            frame = F(container, self)

            # the Game class act as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.bind("<Button-1>", self.show_xy)

        
        
        # Calling a function to switch page
        # and also let the main page be first.
        self.show_frame(MainPage)


    def show_frame(self, controller):
        """This function find the frame in the dictionary 
        and raise it to the top"""
        frame = self.frames[controller]
        frame.tkraise()

    def show_xy(self,event):
                """Show x and y position when clicked
                just for designing purpose"""
                x, y = event.x, event.y
                print(f"Mouse position: x={x}, y={y}")
    




    def quit():
        pass




class MainPage(tk.Frame):
    """This is the MainPage, where the player will first be greeted
    this contain the title, and acess to Setting, Help, About and the play
    button"""
    def __init__(self, parent, controller):
        #intialise the class as a frame
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text= "Main Menu")
        label.pack(padx=10, pady=10)

        # Dictionary for the for loop to create switch_frame_button.
        pages = {
            "Setting Menu" : SettingMenu,
            "Help Menu" : HelpMenu,
            "About Menu" : AboutMenu,
            "LeaderBoard" : LeaderBoard
            }

        for page_name, page_class in pages.items():
            """This for loop uses the dictionary
            to create button to switch between each frames
            It switch frame by calling the show_frame method
            with a lambda function."""

            switch_frame_bt = tk.Button(
                self,
                text=f"Go to {page_name}",
                command= lambda p=page_class: controller.show_frame(p)
            )
            switch_frame_bt.pack(side="bottom", padx=10, pady=10)

        # This is the button that will start the game.
        play_bt = tk.Button(self,
                            text='Play', 
                            command= self.start_game
                            )
        play_bt.pack()

    def start_game(self):
        """This will start the game"""
        print('Game start')





    
    

class SettingMenu(tk.Frame):
    def __init__(self, parent, controller):
        """This is the setting menu, where the player can change
        sound and switch quality and also switch to main menu"""

        # Position for widgets and colours
        vls_pos = [690,235]
        vllb_pos = [400,235]
        vllb_pos2 = [900,235]
        MENU_BLUE = "#0cc0df"
        self.quality = ["Low", "Medium", "High", "Super-High"]


        tk.Frame.__init__(self, parent)

        # Load the background.
        self.setting_bg = Image.open("Sprites/setting_menu_bg.png")
        self.setting_menu_bg = ImageTk.PhotoImage(self.setting_bg)

        # Place background with label 
        self.image_lbl = tk.Label(self, image=self.setting_menu_bg)
        self.image_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.image_lbl.image = self.setting_menu_bg  
       

        # title of setting
        self.label = tk.Label(self, text="This is Setting menu")
        self.label.pack(padx=10, pady=10)
        
        # Volume label for right and left side of the slider
        self.volume_lbl = tk.Label(self, text="Sound Volume", 
                              font=("Microsoft Sans Serif",26), bg=MENU_BLUE)
        self.volume_lbl.place(in_=self.image_lbl, x=vllb_pos[0], 
                         y=vllb_pos[1], anchor="center")
        
        self.volume_lbl2 = tk.Label(self, text="70%",
                              font=("Microsoft Sans Serif",26), bg=MENU_BLUE)
        self.volume_lbl2.place(in_=self.image_lbl, x=vllb_pos2[0], 
                         y=vllb_pos2[1], anchor="center")

        # Volume Slider
        self.volume_sld = tk.Scale(self, from_=0, to=100, 
                              highlightbackground="black",sliderlength=10, 
                              orient="horizontal",bg="black", fg=MENU_BLUE, 
                              highlightthickness=1,troughcolor=MENU_BLUE, 
                              resolution=1, length=300, command=self.update_volume_lbl,
                              showvalue=False, activebackground="black")
        self.volume_sld.set(70)
        self.volume_sld.place(in_=self.image_lbl, x=vls_pos[0], 
                         y=vls_pos[1], anchor="center")
        
        # Quality label 
        self.quality_lbl = tk.Label(self, text="Quality",
                              font=("Microsoft Sans Serif",26), bg=MENU_BLUE)
        self.quality_lbl.place(in_=self.image_lbl, x=vllb_pos[0],
                         y=vllb_pos[1] + 100, anchor="center")
        
        self.quality_bt = tk.Button(self, text="Medium", width=10, command= self.update_quality,
                               font=("Microsoft Sans Serif",26), bg=MENU_BLUE)
        self.quality_bt.place(in_=self.image_lbl, x=vllb_pos[0]+200,
                         y=vllb_pos[1] + 100, anchor="center")
        

        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self,
            text="Go to back to Main Menu",
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.pack(side="bottom", fill=tk.X)

    def update_volume_lbl(self, value):
        """This function updates the volume label"""
        self.volume_lbl2.config(text=f"{value}%")
    
    def update_quality(self):
        """This function updates the quality value"""

        # Get the first element of the list
        text = self.quality.pop(0)
        # Put it at the end of the list
        self.quality.append(text)
        # Configure the button's text
        self.quality_bt.config(text=self.quality[0])




class HelpMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # title of setting
        label = tk.Label(self, text="This is Help menu")
        label.pack(padx=10, pady=10)

        # Button switch to main menu
        switch_window_button = tk.Button(
            self,
            text="Go to back to Main Menu",
            command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class AboutMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # title of setting
        label = tk.Label(self, text="This is About menu")
        label.pack(padx=10, pady=10)

        # Button switch to main menu
        switch_window_button = tk.Button(
            self,
            text="Go to back to Main Menu",
            command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

class LeaderBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # title of setting
        label = tk.Label(self, text="This is the LeaderBoard")
        label.pack(padx=10, pady=10)

        # Button switch to main menu
        switch_window_button = tk.Button(
            self,
            text="Go to back to Main Menu",
            command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

if __name__ == "__main__":
    root = Game()
    root.mainloop()