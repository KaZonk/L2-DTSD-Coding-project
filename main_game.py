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
    place_holder_font = ("Helvetica", 16)
    # position for widgets
    vl_sl_pos = [690,200]
    vllb_pos = [380,200]
    vllb_pos2 = [900,200]
    qual_lbl_pos = [380,280]
    qual_bt_pos = [690,280]
    txt_box_height = 12
    txt_box_width = 125


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        """using the innit function create the necesserary
        widgets when the class 'Game' is called"""

        
        self.wm_title("Clicker game")
        self.wm_geometry("1200x800")
        self.resizable(False, False)
        
        # In-game varible.
        self.money = 0
        self.money_per_click = 1
        self.sanitary = 0
        self.sanitary_per_click = 1
        self.bad_ending_points = -1000
        self.good_ending_points = 1000
        # just so it doesn't have any name at the start.
        self.current_frame_name = None

        # creating a container as a frame.
        container = tk.Frame(self, height=1200, width=800)

        container.pack(side="top", fill="both", expand=True)

        # configuring the location of container using grid.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of Frames.
        pg_class_list = [MainPage, SettingMenu, HelpMenu, 
                         AboutMenu, GameMain, UpgradeMenu,
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
        """This function finds the frame in the dictionary 
        and raises it to the top."""
        frame = self.frames[controller]
        frame.tkraise()

        self.current_frame = frame
        self.current_frame_name = controller  # Track name of current page

        # Pause the game if the current frame is not GameMain
        if isinstance(self.frames[GameMain], GameMain):
            if self.current_frame_name == GameMain:
                self.frames[GameMain].resume_game()
            else:
                self.frames[GameMain].pause_game()


class MainPage(tk.Frame):
    """This is the MainPage, where the player will first be greeted
    this contain the title, and acess to Setting, Help, About and the play
    button"""
    def __init__(self, parent, controller):
        #intialise the class as a frame
        tk.Frame.__init__(self, parent) 
        # this also be super().__init__(parent) 
        # but it can be considered in the future.
        """The MainPage have the following:"""

        # Store the controller as an instance attribute, so that it can be used
        # in the MainGame class method.
        self.controller = controller  

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
        self.controller = controller
        self.parent = parent
        self.running = False
        
        # Load the background.
        self.game_main = Image.open("Sprites/game_bg.png")
        self.game_bg = ImageTk.PhotoImage(self.game_main)

        # create a subframe to hold canvas
        sub_frame = tk.Frame(self)
        sub_frame.pack(side="top", fill="both", expand=True)
        sub_frame.grid_rowconfigure(0, weight=1)  # For the canvas
        sub_frame.grid_columnconfigure(0, weight=1)

        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        # Use place for precise positioning at the top-right corner
        self.switch_window_button.place(relx=1.0, rely=0.0, anchor="ne", 
                                        x=-10, y=10
        )

        # Button switch to Upgrademenu
        self.upgrade_menu_bt = tk.Button(
            self, text="Shop", bg="gray", 
            fg="black", activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(UpgradeMenu)
        )
        # Use place for precise positioning at the right
        self.upgrade_menu_bt.place(relx=1.0, rely=0.5, anchor="ne", x=-10, y=0
        )

        # Create canvas for image and Keep a reference 
        self.canvas = tk.Canvas(sub_frame, width=1200, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.game_bg, anchor='nw') 
        self.canvas.image = self.game_bg

        # Money label
        self.money_lbl = tk.Label(self, text="Money: $0", 
                                    font=controller.place_holder_font)
        self.money_lbl.place(anchor="n", x=459, y=50)

        self.sanitary_lbl = tk.Label(self, text="Sanitary: 0", 
                                    font=controller.place_holder_font)
        self.sanitary_lbl.place(anchor="n", x=700, y=50)

        # Falling button (ball)
        self.falling_button = self.canvas.create_oval(
        180, 0, 220, 40, fill="red"
        )
        self.canvas.tag_bind(self.falling_button, "<Button-1>", self.hit_button)

        self.rubbish_sprites = []  # List to hold rubbish sprites

        self.fall_speed = 10
        self.update_game()
        

    def update_game(self):
        if self.running:
            # Move Rubbish down
            for sprite, image in self.rubbish_sprites:
                coords = self.canvas.coords(sprite)
                if coords[1] < 500:  #move if y < 500
                    self.canvas.move(sprite, 0, self.fall_speed)
                elif coords[1] >= 500 and coords[1] < 510:  # Stop at y=500
                    self.after(8000, lambda s=sprite: self.remove_rubbish(s))
                    self.canvas.coords(sprite, coords[0], 500)  # Ensure it stays at y=500
                    
        self.after(50, self.update_game)

    def hit_button(self, event):
        self.controller.money += self.controller.money_per_click
        self.money_lbl.config(text=f"Points: ${self.controller.money}")
        x = random.randint(50, 350)
        self.canvas.coords(self.falling_button, x, 0, x + 40, 40)

    def spawn_rubbish(self):
        x = random.randint(20, 1160) # Random x position for ruppish entities
        rubbish_image = ImageTk.PhotoImage(Image.open("Sprites/rubbish_e3.png"))
        sprite = self.canvas.create_image(x, 0, 
                                          image=rubbish_image, anchor='nw'
    )
        # Ensure the sprite is not garbage collected by keeping a reference
        rubbish_image.image = rubbish_image
        # Store the sprite and image reference
        self.rubbish_sprites.append((sprite, rubbish_image))  
    
    def start_spawning_rubbish(self):
        """This function starts spawning rubbish sprites at regular 
        intervals."""
        self.spawn_rubbish()  # Spawn the first rubbish sprite
        self.after(3000, self.start_spawning_rubbish)  # Spawn every 3s
    
    def remove_rubbish(self, sprite):
        """This function removes the rubbish sprite from the canvas"""
        if sprite in [s[0] for s in self.rubbish_sprites]:
            self.canvas.delete(sprite)  # Remove sprite from canvas
            self.rubbish_sprites = [s for s in self.rubbish_sprites if 
                                    s[0] != sprite]
            self.controller.sanitary -= 10  # Deduct sanitary points
            self.sanitary_lbl.config(text=f"Sanitary: {self.controller.sanitary}")
    
    def give_money(self, amount):
        pass
        

    def pause_game(self):
        self.running = False # Pause the game.

    def resume_game(self):
        self.running = True # Resume the game.
        self.start_spawning_rubbish()


class UpgradeMenu(tk.Frame):
    def __init__(self, parent, controller):
        """This is the UpgradeMenu, where the player can upgrade"""
        tk.Frame.__init__(self, parent)

        # Title
        label = tk.Label(self, text="Upgrade Menu")
        label.pack(padx=10, pady=10)

        # Load the background.
        self.shop_bg = Image.open("Sprites\Shop_rf.png")
        self.shop_bg_bg = ImageTk.PhotoImage(self.shop_bg)

        # Place background with label 
        self.shop_bg_bg_lbl = tk.Label(self, image=self.shop_bg_bg)
        self.shop_bg_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.shop_bg_bg_lbl.image = self.shop_bg_bg


        # Button switch to GameMain
        self.switch_window_button = tk.Button(
            self, text="Back to Game", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(GameMain)
        )
        # Use place for precise positioning at the top-right corner
        self.switch_window_button.place(relx=1.0, rely=0.0, anchor="ne", 
                                        x=-10, y=10
        )


    def upgrade(self):
        pass

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

        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.pack(side="top", anchor="ne")


        # First Paragraph
        self.long_text = """Lorem ipsum dolor sit 
                amet consectetur adipiscing elit.
          Quisque faucibus ex sapien vitae pellentesque sem placerat.
            In id cursus mi pretium tellus duis convallis. 
            Tempus leo eu aenean sed diam urna tempor. 
            Pulvinar vivamus fringilla lacus nec metus bibendum egestas. 
            Iaculis massa nisl malesuada lacinia integer nunc posuere. 
            Ut hendrerit semper vel class aptent taciti sociosqu. 
            Ad litora torquent per conubia nostra inceptos himenaeos."""

        self.long_paragraph = tk.Text(self, height = controller.txt_box_height, 
                                      width = controller.txt_box_width, 
                                        bg='#cfb792'
                                        )
        self.long_paragraph.insert(tk.END, self.long_text)
        self.long_paragraph.pack(padx=10, pady=50, side='top')

        # Second Paragraph
        self.long_text2 = """Lorem ipsum dolor sit 
                amet consectetur adipiscing elit.
          Quisque faucibus ex sapien vitae pellentesque sem placerat.
            In id cursus mi pretium tellus duis convallis. 
            Tempus leo eu aenean sed diam urna tempor. 
            Pulvinar vivamus fringilla lacus nec metus bibendum egestas. 
            Iaculis massa nisl malesuada lacinia integer nunc posuere. 
            Ut hendrerit semper vel class aptent taciti sociosqu. 
            Ad litora torquent per conubia nostra inceptos himenaeos."""

        self.long_paragraph2 = tk.Text(self, height = controller.txt_box_height, 
                                      width = controller.txt_box_width, 
                                      bg='#ae8f60'
                                    )
        self.long_paragraph2.insert(tk.END, self.long_text2)
        self.long_paragraph2.pack(padx=10, pady=50, side='top')




if __name__ == "__main__":
    root = Game()
    root.mainloop()