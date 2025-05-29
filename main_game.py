"""The beginning of something beautiful or terrible"""

# Importing libraries
import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk



class Game(tk.Tk):
    """Initilising Main window as a class"""

    # colours
    MENU_BLUE = "#0cc0df" 
    TEXT_GOLD = "#dbae3c"
    BT_BLUE = "#004aad"
    # font
    BT_FONT = ('Times', 24)
    text_font = ("Microsoft Sans Serif",30)
    # position for widgets
    vl_sl_pos = [690,200]
    vllb_pos = [380,200]
    vllb_pos2 = [900,200]
    qual_lbl_pos = [380,280]
    qual_bt_pos = [690,280]

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
                         AboutMenu, GameMain
                         ]
        self.frames = {}

        for F in pg_class_list:
            """Using a for loop to call the classes as a frame
            and then assign to an object."""
            frame = F(container, self)

            # the Game class act as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        
        
        # Calling a function to switch page
        # and also let the main page be first.
        self.show_frame(MainPage)


    def show_frame(self, controller):
        """This function find the frame in the dictionary 
        and raise it to the top"""
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(tk.Frame):
    """This is the MainPage, where the player will first be greeted
    this contain the title, and acess to Setting, Help, About and the play
    button"""
    def __init__(self, parent, controller):
        #intialise the class as a frame
        tk.Frame.__init__(self, parent)

        # Load the background.
        self.main_bg= Image.open("Sprites/main_menu_bg.png")
        self.main_menu_bg = ImageTk.PhotoImage(self.main_bg)

        # Place background with label 
        self.main_bg_lbl = tk.Label(self, image=self.main_menu_bg)
        self.main_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.main_bg_lbl.image = self.main_menu_bg  

        label = tk.Label(self, text= "Ocean Clicker", font = ('Forte', 100),
                         background=controller.MENU_BLUE, 
                         fg=controller.TEXT_GOLD)
        label.pack(padx=10, pady=10)

        # Dictionary for the for loop to create switch_frame_button.
        pages = {
            "About Menu" : AboutMenu,
            "Help Menu" : HelpMenu,
            "Setting Menu" : SettingMenu,
            "Play Game" : GameMain
            }

        for page_name, page_class in pages.items():
            """This for loop uses the dictionary to create button,
            It switch frame by calling the show_frame method
            with a lambda function."""

            switch_frame_bt = tk.Button(
                self, fg=controller.TEXT_GOLD, bg=controller.BT_BLUE, 
                font=controller.BT_FONT, text=f"{page_name}", 
                width=10, height=2, 
                activebackground=controller.MENU_BLUE,
                command= lambda p=page_class: controller.show_frame(p)
            )
            switch_frame_bt.pack(side="bottom", padx=10, pady=10)


class GameMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # title of setting
        label = tk.Label(self, text="This is the Game Main")
        label.pack(padx=10, pady=10)

        # Load the background.
        self.game_main = Image.open("Sprites/game_bg.png")
        self.game_bg = ImageTk.PhotoImage(self.game_main)

        # Place background with label 
        self.game_bg_lbl = tk.Label(self, image=self.game_bg)
        self.game_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.game_bg_lbl.image = self.game_bg

        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.pack(side="top", anchor="ne")


class SettingMenu(tk.Frame):
    """This is the setting menu, where the player can change
        sound and switch quality and also switch to main menu"""
    
    def __init__(self, parent, controller):
        """The setting menu have the following:
        background, volume slider and buttons to switch quality
        button to return to main menu."""




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
                              font=controller.text_font, 
                              bg=controller.MENU_BLUE)
        self.volume_lbl.place(in_=self.image_lbl, x=controller.vllb_pos[0], 
                         y=controller.vllb_pos[1], anchor="center")
        
        self.volume_lbl2 = tk.Label(self, text="70%", font=controller.text_font, 
                              bg=controller.MENU_BLUE
                              )
        self.volume_lbl2.place(in_=self.image_lbl, x=controller.vllb_pos2[0], 
                         y=controller.vllb_pos2[1], anchor="center"
                         )

        # Volume Slider
        self.volume_sld = tk.Scale(self, from_=0, to=100, 
                              highlightbackground="black",sliderlength=10, 
                              orient="horizontal",bg="black", 
                              fg=controller.MENU_BLUE, highlightthickness=1, 
                              troughcolor=controller.MENU_BLUE, 
                              length=300, command=self.update_volume_lbl,
                              showvalue=False, activebackground="black")
        
        self.volume_sld.set(70)
        self.volume_sld.place(in_=self.image_lbl, x=controller.vl_sl_pos[0], 
                         y=controller.vl_sl_pos[1], anchor="center")
        
        # Quality label 
        self.quality_lbl = tk.Label(self, text="Quality",
                                font=controller.text_font, 
                                bg=controller.MENU_BLUE
                                    )
        self.quality_lbl.place(in_=self.image_lbl, x=controller.qual_lbl_pos[0],
                                y=controller.qual_lbl_pos[1], anchor="center"
                                )
        
        # Quality Button
        self.quality = ["Low", "Medium", "High", "Super-High"]

        self.quality_bt = tk.Button(self, text="Low",
                                    command= self.update_quality, width=10,
                                    activebackground="gray",
                                    font=controller.text_font, 
                                    bg=controller.MENU_BLUE
                                    )
        self.quality_bt.place(in_=self.image_lbl, x=controller.qual_bt_pos[0],
                                y=controller.qual_bt_pos[1], anchor="center"
                                )
        

        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.pack(side="top", anchor="ne")


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

        # Load the background.
        self.help_bg = Image.open("Sprites\help_page_bg.png")
        self.help_menu_bg = ImageTk.PhotoImage(self.help_bg)

        # Place background with label 
        self.help_img_lbl = tk.Label(self, image=self.help_menu_bg)
        self.help_img_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.help_img_lbl.image = self.help_menu_bg


        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.pack(side="top", anchor="ne")


class AboutMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # title of setting
        label = tk.Label(self, text="This is About menu")
        label.pack(padx=10, pady=10)

        # Load the background.
        self.about_bg = Image.open("Sprites\About_Page_bg.png")
        self.about_menu_bg = ImageTk.PhotoImage(self.about_bg)

        # Place background with label 
        self.about_img_lbl = tk.Label(self, image=self.about_menu_bg)
        self.about_img_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.about_img_lbl.image = self.about_menu_bg

        # Really long text
        self.long_text = """Lorem ipsum dolor sit 
        amet consectetur adipiscing elit.
          Quisque faucibus ex sapien vitae pellentesque sem placerat.
            In id cursus mi pretium tellus duis convallis. 
            Tempus leo eu aenean sed diam urna tempor. 
            Pulvinar vivamus fringilla lacus nec metus bibendum egestas. 
            Iaculis massa nisl malesuada lacinia integer nunc posuere. 
            Ut hendrerit semper vel class aptent taciti sociosqu. 
            Ad litora torquent per conubia nostra inceptos himenaeos."""

        self.long_paragraph = tk.Text(self, height = 10, width = 52)
        self.long_paragraph.insert(tk.END, self.long_text)
        self.long_paragraph.pack(padx=10, pady=10, anchor='center')

        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.pack(side="top", anchor="ne")



if __name__ == "__main__":
    root = Game()
    root.mainloop()