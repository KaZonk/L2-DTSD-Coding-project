"""This is a Clicker game, 
where the player will click on rubbish to collect money and sanitary points.
When the player collects enough points, they can upgrade their tools
and hire cleaners to help them collect rubbish. Moreover, the player can
achieve the good and bad endings by reaching a certain sanitary value.
Made by Kane Dao
Made with Python, mainly with the Tkinter library
Date finished 8/8/25
Honourable mention: Ms Marnette Strauss, Matthew, Noah, GitHub Copilot, 
Stack Overflow.
Dishonourable mention: Campbell Robert.
--------------------------------------------------------------------------
Purpose of program:
To raise awareness among children about ocean pollution through a game
Functionality:
A clicker game, click on rubbish, get money, buy an upgrade, repeat
--------------------------------------------------------------------------
Main Menu Music by: Royalty Free Music: https://www.bensound.com\
License code: Z4B0MZ7L27NBZYQA}I
--------------------------------------------------------------------------
Transaction sound effect: Buy or Sell Item 1 by Sabacky 
-- https://freesound.org/s/766069/ -- License: Attribution 4.0
"""

# Importing libraries
import tkinter as tk
import random
import math
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import pygame


class Game(tk.Tk):
    """Initialising Main window as a class"""
    #These variables are used to define the colours, fonts and other constants
    # colours
    MENU_BLUE = "#0cc0df" 
    TEXT_GOLD = "#dbae3c"
    BT_BLUE = "#004aad"
    TITLE_PURPLE = "#4e2a84"
    # font
    BT_FONT = ('Calibri', 22)
    text_font = ("Microsoft Sans Serif", 30)
    place_holder_font = ("Helvetica", 16)
    description_font = ("Helvetica", 18)

    def __init__(self, *args, **kwargs):
        """This function initializes the main window, sets the title, 
        geometry, and sets the protocol for closing the window and
        define ingame varibles."""
        tk.Tk.__init__(self, *args, **kwargs)
        

        # Setting the title, geometry and resizable properties for window
        self.wm_title("Clicker game")
        self.wm_geometry("1200x800")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Initialize the pygame mixer to play music.
        pygame.mixer.init()
        
        # These are in-game varible, they can change and
        # are often used in function within class.
        self.money = 0
        self.sanitary = 0
        self.money_per_click = 5
        self.sanitary_per_click = 8
        self.sanitary_per_lost = -15
        self.bad_ending_points = -300
        self.good_ending_points = 1000
        self.fall_speed = 10
        self.current_frame_name = None

        # Creating a container as a frame.
        container = tk.Frame(self, height=1200, width=800)
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of container using grid.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of Frames.
        frame_classes = [MainPage, SettingMenu, HelpMenu, 
                         AboutMenu, GameMain, UpgradeMenu,
                        ]
        self.frames = {}

        for F in frame_classes:
            """This for loop creates a frame for each class in the list,
            and store it in the frames dictionary with the class as the key."""

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # Show the Mainpage and play music
        self.show_frame(MainPage)
        self.start_music()
    
    def start_music(self):
        """This function starts the background music."""
        pygame.mixer.music.load("music/hey_gamemain/hey.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)  # Set volume to 30%

    def show_frame(self, controller):
        """This function open the frame, by finding the frame in the dictionary 
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

    def on_close(self):
        """Handle window close event with confirmation."""
        if mb.askyesno("Exit Game", 
                       "Are you sure you want to exit the game? (Your" \
                       " progress will not be saved.)"):
            self.destroy()


class MainPage(tk.Frame):
    """This is the MainPage, where the player will first be greeted
    this contain the title, and acess to Setting, Help, About and the play
    button"""
    def __init__(self, parent, controller):
        """This function initializes the MainPage, sets the background,
        title, exit button and buttons to switch frames."""
        tk.Frame.__init__(self, parent) 

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

        label = tk.Label(self, text= "Ocean Clicker", 
                         font = ('Courier', 80),
                         background=controller.MENU_BLUE, 
                         fg=controller.TITLE_PURPLE)
        label.place(x=200, y=50)  

        # Button to exit the game
        exit_button = tk.Button(
            self, fg="black", bg="red", 
                font=controller.BT_FONT, text=f"Exit Game", 
                width=8, height=1, 
                activebackground="gray",
                command= lambda: controller.on_close()
            )
        exit_button.place(x=1000, y=725)

        # Dictionary for the for loop to create switch_frame_button.
        pages = {
                "Play Game": GameMain,
                "Setting Menu": SettingMenu,
                "Help Menu": HelpMenu,
                "About Menu": AboutMenu
                }

        # Starting position for buttons
        start_x = 500
        start_y = 300
        button_spacing = 125 

        for i, (page_name, page_class) in enumerate(pages.items()):
            """This for loop creates a button for each page in the 
            pages dictionary, and places it at the specified 
            position with a spacing.""" 
            button = tk.Button(
                self, text=page_name, font=controller.BT_FONT, 
                bg=controller.BT_BLUE, activebackground=controller.MENU_BLUE,
                fg=controller.TEXT_GOLD, width=10, height=2,
                command=lambda page=page_class: controller.show_frame(page)
            )
            button.place(x=start_x, y=start_y + i * button_spacing)
    
    
class GameMain(tk.Frame):
    """This is the GameMain, where the player will play the game."""

    def __init__(self, parent, controller):
        """In this GameMain, there are sub frame, button
        and to the shop menu and the label for each points system"""
        tk.Frame.__init__(self, parent)

        # Define the attributes, flags and load the images.
        self.controller = controller
        self.parent = parent
        self.running = False
        self.spawning_rubbish = False 
        self.spawning_rubbish_id = None  
        self.bubble_animation_running = False
        self.canvas = None 
        self.game_over = False
        self.load_background_images()  

        # define the starting sanitary and money per click.
        self.start_spc = 8
        self.start_mpc = 5

        # create a subframe to hold canvas
        sub_frame = tk.Frame(self)
        sub_frame.pack(side="top", fill="both", expand=True)
        sub_frame.grid_rowconfigure(0, weight=1) 
        sub_frame.grid_columnconfigure(0, weight=1)

        # Button switch to main menu at the top-right corner.
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=self.controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.place(relx=1.0, rely=0.0, anchor="ne", 
                                        x=-10, y=10
        )

        # Button to Upgrademenu, positioning at the right.
        self.upgrade_menu_bt = tk.Button(
            self, text="Shop", bg="gray", 
            fg="black", activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(UpgradeMenu)
        )
        self.upgrade_menu_bt.place(relx=1.0, rely=0.5, anchor="ne", x=-10, y=0
        )

        # Create canvas for image and Keep a reference .
        self.canvas = tk.Canvas(sub_frame, width=1200, height=800)
        self.canvas.pack(fill="both", expand=True)

        # Money label.
        self.money_lbl = tk.Label(self, text= f"Money: ${self.controller.money}", 
                                    font=controller.place_holder_font)
        self.money_lbl.place(anchor="n", x=459, y=50)
        
        # Sanitary label.
        self.sanitary_lbl = tk.Label(self, text="Sanitary: 0", 
                                    font=controller.place_holder_font)
        self.sanitary_lbl.place(anchor="n", x=700, y=50)

        # list to store rubbish sprites and bubble sprite
        self.rubbish_sprites = [] 
        self.bubbles = []  
        self.bubbles_images = [] 

        # Control the bubble spawning.
        self.check_quality_change_bubble()
        
        self.update_background()  
        self.update_game()


    def load_background_images(self):
        """Load all background images."""
        self.regular_game_main = ImageTk.PhotoImage(
                                            Image.open("Sprites/game_bg.png"))
        self.bad_ending_bg = ImageTk.PhotoImage(
                                        Image.open("Sprites/bad_ending.png"))
        self.good_ending_bg = ImageTk.PhotoImage(
                                        Image.open("Sprites/good_ending.png"))

    def update_background(self):
        """Update the canvas background based on sanitary points."""
        if self.canvas and self.game_over is False: 
            if self.controller.sanitary >= self.controller.good_ending_points:
                self.canvas.create_image(0, 0, image=self.good_ending_bg, 
                                         anchor='nw', tags="background")
 
                message = "You have achieved a Good ending!" \
                            " Do you want to play again?"
                self.reset_or_not(message)
                
            elif self.controller.sanitary <= self.controller.bad_ending_points:
                self.canvas.create_image(0, 0, image=self.bad_ending_bg,
                                        anchor='nw', tags="background")
                message = "You have achieved a bad ending!" \
                            " Do you want to play again?"
                self.reset_or_not(message)
                
            else:
                self.canvas.create_image(0, 0, image=self.regular_game_main,
                                        anchor='nw', tags="background")
            self.canvas.tag_lower("background") 

    def update_game(self):
        """This function updates the game by moving
        the rubbish until it reaches a random y coordinate assigned
        then after 5 seconds it removes the rubbish sprite"""
        if self.running and self.game_over is False:
            # Move Rubbish down
            for sprite, image in self.rubbish_sprites:
                coords = self.canvas.coords(sprite)
                y_collision = random.randint(499, 510)  
                if coords[1] <= y_collision:
                    self.canvas.move(sprite, 0, self.controller.fall_speed)
                elif coords[1] >= y_collision and coords[1] < y_collision+10: 
                    self.after(5000, lambda s=sprite: self.remove_rubbish(s))
                    self.canvas.coords(sprite, coords[0], y_collision+10) 
        self.after(50, self.update_game)

    def spawn_rubbish(self):
        """This function spawn rubbish sprite at random x coordinates
        at top of the canvas. Then it bind it to a click event so that 
        it can be interacted with by the player."""

        x = random.randint(20, 1100)  # Random x position for rubbish entities
        rubbish_image1 = ImageTk.PhotoImage(
                                           Image.open("Sprites/rubbish_e1.png"))
        rubbish_image2 = ImageTk.PhotoImage(
                                           Image.open("Sprites/rubbish_e2.png"))
        rubbish_image3 = ImageTk.PhotoImage(
                                           Image.open("Sprites/rubbish_e3.png"))
        rubbish_image4 = ImageTk.PhotoImage(
                                           Image.open("Sprites/rubbish_e4.png"))
        rubbish_image5 = ImageTk.PhotoImage(
                                           Image.open("Sprites/rubbish_e5.png"))

        # Randomly choose one of the rubbish images
        rubbish_image = random.choice([rubbish_image1, rubbish_image2, 
                                        rubbish_image3, rubbish_image4,
                                        rubbish_image5])
        sprite = self.canvas.create_image(x, 0, image=rubbish_image, 
                                        anchor='nw')

        # Ensure the sprite is not garbage collected by keeping a reference
        rubbish_image.image = rubbish_image
        # Store the sprite and image reference
        self.rubbish_sprites.append((sprite, rubbish_image))

        # Bind click event to the rubbish sprite 
        self.canvas.tag_bind(sprite, "<Button-1>",
                             lambda e, s=sprite: self.hit_rubbish(s))

    def hit_rubbish(self, sprite):
        """This function check if the sprite is in the rubbish_sprites list,
        if it is then remove it and give money and sanitary points."""
        if sprite in [s[0] for s in self.rubbish_sprites]:
            """This if statement check if the sprite exist in the list
            then remove it, play the sound once and give the money."""
            hit_sound = pygame.mixer.Sound(
                                        "music/sound_effect/collecting_se.wav")
            hit_sound.play(loops=0)  
            self.canvas.delete(sprite)  # Remove sprite from canvas
            self.rubbish_sprites = [s for s in self.rubbish_sprites 
                                    if s[0] != sprite]
            self.give_money(self.controller.money_per_click, 
                            self.controller.sanitary_per_click)  

    def give_money(self, money_increment, sanitary_increment):
        """Increment player's money, sanitary and update the labels."""
        self.controller.money += money_increment
        self.controller.sanitary += sanitary_increment
        self.controller.frames[UpgradeMenu].update_money() 
        self.sanitary_lbl.config(text=f"Sanitary: {self.controller.sanitary}")
        self.update_background()  # Update background after sanitary changes

    def start_spawning_rubbish(self):
        """This function starts spawning 
        rubbish sprites at 3 seconds intervals."""  
        if self.game_over is False:
            self.running = True  # Start the game      
            self.spawn_rubbish()
            self.spawning_rubbish_id = self.after(3000, 
                                                  self.start_spawning_rubbish)

    def remove_rubbish(self, sprite):
        """This function removes the rubbish sprite from the canvas"""
        if sprite in [s[0] for s in self.rubbish_sprites]:
            self.canvas.delete(sprite)  # Remove sprite from canvas
            self.rubbish_sprites = [s for s in self.rubbish_sprites if 
                                    s[0] != sprite]
            self.controller.sanitary += self.controller.sanitary_per_lost
            self.sanitary_lbl.config(text=
                                    f"Sanitary: {self.controller.sanitary}")
            self.update_background() 

    def pause_game(self):
        """Pause the game and stop spawning rubbish."""        
        self.running = False  
        if self.spawning_rubbish_id: 
            self.after_cancel(self.spawning_rubbish_id)
            self.spawning_rubbish_id = None
        self.spawning_rubbish = False

    def resume_game(self):
        """Resume the game and start spawning rubbish if not already running."""        
        if not self.running:  # Only resume if the game is not already running
            self.running = True
            if not self.spawning_rubbish: 
                self.start_spawning_rubbish()
    
    def wipe_all_rubbish(self):
        """This function removes all rubbish sprites from the canvas by
        deleting each sprite and clearing the list."""
        for sprite, image in self.rubbish_sprites:
            self.canvas.delete(sprite)
        self.rubbish_sprites.clear()
    
    def reset_game(self):
        """This function resets the game by clearing all rubbish, resetting
        money and sanitary points, and updating the labels."""
        self.game_over = False
        self.wipe_all_rubbish()
        self.controller.money = 0
        self.controller.sanitary = 0
        self.controller.money_per_click = self.start_mpc
        self.controller.sanitary_per_click = self.start_spc
        self.controller.frames[UpgradeMenu].update_money()
        self.sanitary_lbl.config(text="Sanitary: 0")
        self.controller.frames[UpgradeMenu].reset_shop()
        self.update_background()

    def reset_or_not(self,message):
        """This function ask the player if they want to reset or not.
        If they click yes, it resets the game and switch to GameMain."""
        self.wipe_all_rubbish()
        self.pause_game()
        self.game_over = True
        answer = mb.askyesno("Game Over", message, icon='info')
        if answer:
            self.reset_game() 
            self.controller.show_frame(MainPage)
        else:
            self.controller.show_frame(MainPage)
    
    def generate_bubbles(self):
        """Generates bubbles at random positions on the canvas with the maximum
        of 6 bubbles at a time. The bubbles will be animated to move upwards."""
        max_bubbles = 6
        if len(self.bubbles) >= max_bubbles:
            return
        # Pick from two ranges: 20-200 and 700-1100 for x, and 500-700 for y.
        if random.choice([True, False]):
            x = random.randint(20, 200)
        else:
            x = random.randint(700, 1100)
        y = random.randint(500, 700)
        bubble_image = ImageTk.PhotoImage(Image.open("Sprites/p_bubble.png"))
        bubble_sprite = self.canvas.create_image(x, y, 
                                                 image=bubble_image, anchor='nw')
        bubble_image.image = bubble_image  # Prevent garbage collection
        self.bubbles.append(bubble_sprite)
        self.bubbles_images.append(bubble_image)
    
    def generate_bubble_periodically(self):
        """Spawns a bubble every few seconds if particle quality is enabled."""
        if (self.game_over or not self.running or 
            self.controller.frames[SettingMenu].quality[0] == "Disabled"):
            return
        self.generate_bubbles()
        self.after(10000, self.generate_bubble_periodically)
    
    def animate_bubbles(self):
        """This function animates the bubbles by moving them upwards and handle
        them if they move off screen."""
        for bubble in self.bubbles:
            coords = self.canvas.coords(bubble)
            if coords[1] > 200:
                self.canvas.move(bubble, 0, -1)
            else:
                # If bubble goes off screen, reset its position
                new_x = random.randint(20, 1100)
                self.canvas.coords(bubble, new_x, 700)
        # Schedule the next bubble animation
        self.after(100, self.animate_bubbles) 
    
    def wipe_all_bubbles(self):
        """This function removes all bubble sprites by clearing
        the list and deleting each bubble sprite."""
        for bubble in self.bubbles:
            self.canvas.delete(bubble)
        self.bubbles.clear()
    
    def check_quality_change_bubble(self):
        """Checks the quality setting and updates the bubble animation,
        generating bubbles if enabled, or stopping the animation if disabled."""
        current_quality = self.controller.frames[SettingMenu].quality[0]
        if (self.game_over or not self.running or current_quality == "Disabled"):
            self.wipe_all_bubbles()
            self.bubble_animation_running = False
        elif current_quality == "Enabled":
            self.generate_bubble_periodically()
            if not self.bubble_animation_running:
                self.bubble_animation_running = True
                self.animate_bubbles()
        self.after(1000, self.check_quality_change_bubble)


class UpgradeMenu(tk.Frame):
    """UpgradeMenu is the menu where the player can buy upgrades in order
    to complete task faster and more efficiently."""
    def __init__(self, parent, controller):
        """This function initializes the UpgradeMenu, sets the background,
        creates labels and buttons for hiring cleaners, upgrading rubbish
        disposer, and better tools. It also includes a button to switch back"""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Starting cost for each upgrade.
        self.hc_start_cost = 105
        self.rbd_start_cost = 30
        self.tool_start_cost = 30

        # Load the background.
        self.shop_bg = Image.open("Sprites/shop_menu_bg.png")
        self.shop_bg_bg = ImageTk.PhotoImage(self.shop_bg)

        # Place background with label 
        self.shop_bg_bg_lbl = tk.Label(self, image=self.shop_bg_bg)
        self.shop_bg_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.shop_bg_bg_lbl.image = self.shop_bg_bg

        self.money_lbl = tk.Label(self, 
                                  text= f"Money: ${self.controller.money}",
                             font=controller.place_holder_font,
                             bg=controller.MENU_BLUE)
        self.money_lbl.place(in_=self.shop_bg_bg_lbl, x=100, y=50)

        # Hire Cleaner money label and button
        self.hire_cleaner_lbl = tk.Label(self, text=f"Cost: {self.hc_start_cost}",
                                        font=controller.place_holder_font, 
                                        bg=controller.MENU_BLUE)
        self.hire_cleaner_lbl.place(in_=self.shop_bg_bg_lbl, x=125, y=325)

        self.hc_lvl = 0
        self.hc_lvl_lbl = tk.Label(self, text="Cleaner Level: 0",
                                        font=controller.place_holder_font, 
                                        bg=controller.MENU_BLUE)
        self.hc_lvl_lbl.place(in_=self.shop_bg_bg_lbl, x=105, y=375)

        self.hire_cleaner_bt = tk.Button(self, text="Hire Cleaner",
                                        font=controller.place_holder_font, 
                                        bg="#00bf63",
                                        fg="black",
                                        activebackground="gray",
                                        borderwidth=0,
                                        command=lambda: 
                                        self.upgrade_hire_cleaner(),
                                        width=12, height=2)
        self.hire_cleaner_bt.place(in_=self.shop_bg_bg_lbl, x=105, y=425)

        # Load cleaner sprites
        cleaner_1 = ImageTk.PhotoImage(
                                        Image.open("Sprites/fish_friend_1.png"))
        cleaner_2 = ImageTk.PhotoImage(
                                        Image.open("Sprites/fish_friend_2.png"))
        cleaner_3 = ImageTk.PhotoImage(
                                        Image.open("Sprites/fish_friend_3.png"))
        cleaner_4 = ImageTk.PhotoImage(
                                        Image.open("Sprites/fish_friend_4.png"))
        cleaner_5 = ImageTk.PhotoImage(
                                        Image.open("Sprites/fish_friend_5.png"))
        cleaner_6 = ImageTk.PhotoImage(
                                        Image.open("Sprites/fish_friend_6.png"))
        self.cleaner_sprites = [cleaner_1, cleaner_2, cleaner_3,
                                cleaner_4, cleaner_5, cleaner_6]

        # Rubbish Disposer(money per click) label and upgrade button
        self.rbd_lbl = tk.Label(self, text=(f"Cost: ${self.rbd_start_cost}"),
                                        font=controller.place_holder_font, 
                                        bg=controller.MENU_BLUE)
        self.rbd_lbl.place(in_=self.shop_bg_bg_lbl, x=430, y=325)

        self.rbd_lvl = 0
        self.rbd_lvl_lbl = tk.Label(self, text="Disposer Level: 0",
                                        font=controller.place_holder_font, 
                                        bg=controller.MENU_BLUE)
        self.rbd_lvl_lbl.place(in_=self.shop_bg_bg_lbl, x=415, y=375)

        self.rbd_bt = tk.Button(self, text="Trash Disposer",
                                        font=controller.place_holder_font, 
                                        bg="#00bf63",
                                        fg="black",
                                        activebackground="gray",
                                        borderwidth=0,
                                        command=lambda: 
                                        self.upgrade_rubbish_delivery(),
                                        width=12, height=2)
        self.rbd_bt.place(in_=self.shop_bg_bg_lbl, x=415, y=425)

        # better tool money label and button       
        self.better_tool_lbl = tk.Label(self, 
                                        text=f"Cost: ${self.tool_start_cost}",
                                        font=controller.place_holder_font, 
                                        bg=controller.MENU_BLUE)
        self.better_tool_lbl.place(in_=self.shop_bg_bg_lbl, x=735, y=325)

        
        self.tool_lvl = 0
        self.tool_lvl_lbl = tk.Label(self, text="Tool Level: 0",
                                        font=controller.place_holder_font, 
                                        bg=controller.MENU_BLUE)
        self.tool_lvl_lbl.place(in_=self.shop_bg_bg_lbl, x=720, y=375)

        self.better_tool_bt = tk.Button(self, text="Better Tool",
                                        font=controller.place_holder_font, 
                                        bg="#00bf63",
                                        fg="black",
                                        activebackground="gray",
                                        borderwidth=0,  
                                        command=lambda: 
                                        self.upgrade_better_tool(),
                                        width=12, height=2)
        self.better_tool_bt.place(in_=self.shop_bg_bg_lbl, x=720, y=425)

        self.buy_sound = pygame.mixer.Sound("music\sound_effect\purchase.wav")


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
    
    def reset_shop(self):
        """Reset the shop state, including costs and labels.
        And delete every cleaner sprite."""
        self.rbd_lbl.config(text=f"Cost: ${self.rbd_start_cost}")  
        self.better_tool_lbl.config(text=f"Cost: ${self.tool_start_cost}")  
        self.hire_cleaner_lbl.config(text=f"Cost: ${self.hc_start_cost}")
        self.hc_lvl = 0
        self.hc_lvl_lbl.config(text="Cleaner Level: 0")
        self.rbd_lvl = 0
        self.rbd_lvl_lbl.config(text="Disposer Level: 0")
        self.tool_lvl = 0
        self.tool_lvl_lbl.config(text="Tool Level: 0")
        # Clear all cleaner sprites from the canvas
        game_main_frame = self.controller.frames[GameMain]
        for cleaner_sprite in game_main_frame.canvas.find_withtag("cleaner"):
            game_main_frame.canvas.delete(cleaner_sprite)
        # Clear the cleaner sprites list
        self.cleaner_sprites.clear()
        self.update_money() 
        
    def update_money(self):
        """Update the money label in the UpgradeMenu and Gamemain."""
        self.controller.frames[GameMain].money_lbl.config(
                                        text=f"Money: ${self.controller.money}")
        self.controller.frames[UpgradeMenu].money_lbl.config(
                                        text=f"Money: ${self.controller.money}")

    def upgrade_hire_cleaner(self):
        """This function inserts a cleaner sprite into the game, 
        which move around randomly and automatically give the player
        sanitary and money."""
        # cost and check player's money.
        cost = self.cost_calc(self.hc_lvl, 'cleaner')
        if self.controller.money >= cost:
            self.buy_sound.play(loops=0) 
            self.controller.money -= cost
            self.controller.money_per_click += 5
            self.hc_lvl += 1
            text = f"Cost: ${self.cost_calc(self.hc_lvl, 'cleaner')}"
            self.hire_cleaner_lbl.config(text=text)
            self.hc_lvl_lbl.config(text=f"Cleaner Level: {self.hc_lvl}")
            self.update_money()

            # Create cleaner sprite
            cleaner_image = random.choice(self.cleaner_sprites)
            cleaner_sprite = self.controller.frames[GameMain].canvas.create_image(
                random.randint(20, 1100), 500,
                image=cleaner_image, anchor='nw'
            )
            cleaner_image.image = cleaner_image  # Prevent garbage collection.
            self.controller.frames[GameMain].canvas.addtag_withtag(
                "cleaner", cleaner_sprite)

            # Start moving and giving bonuses
            self.move_cleaner(cleaner_sprite)
            self.action_cleaner(cleaner_sprite)
        else:
            mb.showerror("Error", 
                        "You don't have enough money to hire a cleaner!")

    def move_cleaner(self, cleaner_sprite):
        """This function moves the cleaner sprite randomly around the canvas."""
        if not self.controller.frames[GameMain].game_over:
            x_move = random.choice([-10, 10])
            y_move = random.choice([-10, 10])
            self.controller.frames[GameMain].canvas.move(
                                                 cleaner_sprite, x_move, y_move)

            # Keep the cleaner within bounds
            coords = self.controller.frames[GameMain].canvas.coords(
                                                                cleaner_sprite)
            if (coords[0] < 0 or coords[0] > 1100 
                or coords[1] < 0 or coords[1] > 700):
                self.controller.frames[GameMain].canvas.move(
                                                cleaner_sprite, -x_move, -y_move)

                
            self.after(500, lambda: self.move_cleaner(cleaner_sprite))

    def action_cleaner(self, cleaner_sprite):
        """Cleaner will randomly 'clean' for player. Update the money
        and sanitary while doing it."""
        if not self.controller.frames[GameMain].game_over:
            money_bonus = random.randint(5, 10)
            sanitary_bonus = random.randint(2, 10)
            self.controller.money += money_bonus
            self.controller.sanitary += sanitary_bonus
            self.update_money()
            self.controller.frames[GameMain].sanitary_lbl.config(
                text=f"Sanitary: {self.controller.sanitary}"
            )
            self.controller.frames[GameMain].update_background()

            # Schedule the next bonus
            random_delay = random.randint(5000, 15000)
            self.after(random_delay, lambda: self.action_cleaner(cleaner_sprite))

    def upgrade_rubbish_delivery(self):
        """This function upgrades the rubbish disposer, which increases the money
        per click and update the cost for the next upgrade level."""
        cost = self.cost_calc(self.rbd_lvl, 'rbd')
        if self.controller.money >= cost:
            self.buy_sound.play(loops=0) 
            self.controller.money -= cost
            self.controller.money_per_click += 5
            self.rbd_lvl += 1
            text = f"Cost: ${self.cost_calc(self.rbd_lvl, 'rbd')}"
            self.rbd_lbl.config(text=text)
            self.rbd_lvl_lbl.config(text=f"Disposer Level: {self.rbd_lvl}")
            self.update_money()
        else:
            mb.showerror("Error", "You don't have enough money to upgrade!")

    def upgrade_better_tool(self):
        """This function upgrades the better tool, it increases the money per 
        click and also increase the cost of the upgrade"""
        cost = self.cost_calc(self.tool_lvl, 'tool')
        if self.controller.money >= cost:
            self.buy_sound.play(loops=0) 
            self.controller.money -= cost
            self.controller.sanitary_per_click += 5
            self.tool_lvl += 1
            text = f"Cost: ${self.cost_calc(self.tool_lvl, 'tool')}"
            self.better_tool_lbl.config(text=text)
            self.tool_lvl_lbl.config(text=f"Tool Level: {self.tool_lvl}")
            self.update_money()
        else:
            mb.showerror("Error", "You don't have enough money to upgrade!")

    def cost_calc(self, level, upgrade_type):
        """Calculate the cost based on the level using quadractic equations."""
        if upgrade_type == 'tool' or upgrade_type == 'rbd':
            cost = 4 * (level)**2 + 34 * level + 30
        else:
            cost = 5 * (level)**2 + 45 * level + 105
        return cost


class SettingMenu(tk.Frame):
    """The setting menu have the following:
        background, volume slider and particle quality and
        button to return to main menu."""
    
    def __init__(self, parent, controller):
        """Intialise the Setting menu"""
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
        self.volume_lbl.place(in_=self.image_lbl, x=380, 
                         y=200, anchor="center")
        
        self.volume_lbl2 = tk.Label(self, text="30%", font=controller.text_font, 
                              bg=controller.MENU_BLUE
                              )
        self.volume_lbl2.place(in_=self.image_lbl, x=900, 
                         y=200, anchor="center"
                         )

        # Volume Slider
        self.volume_sld = tk.Scale(self, from_=0, to=100, 
                              highlightbackground="black",sliderlength=10, 
                              orient="horizontal",bg="black", 
                              fg=controller.MENU_BLUE, highlightthickness=1, 
                              troughcolor=controller.MENU_BLUE, 
                              length=300, command=self.update_volume_lbl,
                              showvalue=False, activebackground="black")
        self.volume_sld.set(30)
        self.volume_sld.place(in_=self.image_lbl, x=690, 
                         y=200, anchor="center")
        
        # Particle label 
        self.quality_lbl = tk.Label(self, text="Particle",
                                font=controller.text_font, 
                                bg=controller.MENU_BLUE
                                    )
        self.quality_lbl.place(in_=self.image_lbl, x=380,
                                y=280, anchor="center"
                                )
        
        # Quality Button
        self.quality = ["Enabled", "Disabled"]

        self.quality_bt = tk.Button(self, text=self.quality[0],
                                    command= self.update_quality, width=10,
                                    activebackground="gray",
                                    font=controller.text_font, 
                                    bg=controller.MENU_BLUE
                                    )
        self.quality_bt.place(in_=self.image_lbl, x=690,
                                y=280, anchor="center"
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
        """This function updates the volume label and change the volume of the 
        music in Pygame."""
        self.volume_lbl2.config(text=f"{value}%")
        self.pygame_volume = int(value) / 100  # Convert to float between 0 - 1
        pygame.mixer.music.set_volume(self.pygame_volume)  
    

    def update_quality(self):
        """This function updates the quality value, by getting the first
        element of the list, popping it and appending it to the end of the list.
        Then update the button text."""
        text = self.quality.pop(0)
        self.quality.append(text)
        self.quality_bt.config(text=self.quality[0])


class HelpMenu(tk.Frame):
    """This is the Help menu, where the player can read about the game, if 
    they're stuck on what to do."""
    def __init__(self, parent, controller):
        """This function initializes the HelpMenu, sets the background,
        creates labels for instructions, and includes a button to switch back
        to the main menu."""
        tk.Frame.__init__(self, parent)

        # Load the background.
        self.help_bg = Image.open("Sprites/help_page_bg.png")
        self.help_menu_bg = ImageTk.PhotoImage(self.help_bg)

        # Place background with label 
        self.help_img_lbl = tk.Label(self, image=self.help_menu_bg)
        self.help_img_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        self.help_img_lbl.image = self.help_menu_bg

        self.instruction_text = (
        "In Ocean Clicker, you're the cleaner of The Fish Civilization's "
        "in the ocean. Your task is to keep the Coral Reef clean by "
        "clicking on rubbishes. You are paid for the amount of rubbish "
        "you pick up. Get the Coral Reef to 1000 Sanitation and the fish lives "
        "happily over after! "
        "However, leaving the Reef dirty will result in serious consequences "
        )

        self.instruction1 = tk.Text(self, height = 12, width = 125, 
                                      font=controller.description_font,
                                      bg=controller.MENU_BLUE, wrap='word',
                                      state='normal', 
                                      highlightthickness=0, borderwidth=0
                                        )
        self.instruction1.insert(tk.END, self.instruction_text)
        self.instruction1.place(x=75, y=200, width=750, height=150)

        self.instruction2_text = (
        "Click on falling rubbish to collect them, giving you money and sanitary "
        "When you have enough money, click on the 'Shop' button to buy upgrades. "
        "Upgrade tools, disposer system and even hire cleaners "
        "and clean the Reef more thoroughly. "
        "When you're ready, you can start the game by clicking on "
        "the 'Play Game' button on the main menu. "
        )
        self.instruction2 = tk.Text(self, height = 12, width = 125, 
                                        font=controller.description_font,
                                        bg='#b1b6a8', wrap='word', 
                                        state='normal', highlightthickness=0,
                                        borderwidth=0
                                    )
        self.instruction2.insert(tk.END, self.instruction2_text)
        self.instruction2.place(x=350, y=560, width=700, height=200)
        
        # Disable the text widgets to prevent editing
        self.instruction1.config(state=tk.DISABLED)
        self.instruction2.config(state=tk.DISABLED)


        # Button switch to main menu
        self.switch_window_button = tk.Button(
            self, text="Back to Main Menu", bg=controller.BT_BLUE, 
            fg=controller.TEXT_GOLD, activebackground="gray",
            font=controller.text_font,
            command=lambda: controller.show_frame(MainPage)
        )
        self.switch_window_button.place(relx=1.0, rely=0.0, anchor="ne", 
                                        x=-10, y=10
        )


class AboutMenu(tk.Frame):
    """This is the About menu, where the player can read about the game,"""
    def __init__(self, parent, controller):
        """This function initializes the AboutMenu, sets the background,"""
        tk.Frame.__init__(self, parent)

        # Load the background.
        self.about_bg = Image.open("Sprites/About_Page_bg.png")
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
        # Use place for precise positioning at the top-right corner
        self.switch_window_button.place(relx=1.0, rely=0.0, anchor="ne", 
                                        x=-10, y=10
        )

        # First Paragraph
        self.long_text = (
        "This game was created by K. "
        "The art was created by me on Canva, music was basic stock sound effect "
        "from www.freesound.org. The coding was done by me but I'd like "
        "to thank my teacher, Mrs S. and many forum on Stack Overflow, "
        "and Co Pilot for helping me fix errors and bugs. "
        )

        self.long_paragraph = tk.Text(self, height = 12, width = 125, 
                                      font=controller.description_font,
                                      bg='#cfb792', wrap='word', 
                                      state='normal', highlightthickness=0,
                                    borderwidth=0
                                    )
        self.long_paragraph.insert(tk.END, self.long_text)
        self.long_paragraph.place(x=100, y=200, width=1000, height=200)

        # Second Paragraph
        self.long_text2 = (
        "This game is a simple clicker game where you play as a cleaner "
        "of the ocean, your task is to clean up the ocean by clicking on "
        "rubbish and collecting money. The game is a fun way to learn about "
        "the importance of keeping our oceans clean and the impact "
        "of pollution on marine life. I hope you'll enjoy playing this game "
        )

        self.long_paragraph2 = tk.Text(self, height = 12, width = 125, 
                                      font=controller.description_font,
                                      bg='#ae8f60', wrap='word', 
                                      state='normal', highlightthickness=0, 
                                      borderwidth=0
                                    )
        self.long_paragraph2.insert(tk.END, self.long_text2)
        self.long_paragraph2.place(x=100, y=500, width=1000, height=200)
        
        # Disable the text widgets to prevent editing
        self.long_paragraph.config(state=tk.DISABLED)
        self.long_paragraph2.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = Game()
    root.mainloop()
