# Main game loop goes here
import arcade
import arcade.gui
from arcade.gui import UIManager, UITextureButton
from arcade import uicolor

# from constants import *
from library import *
import math


class GameView(arcade.View):
    """
    Main application class.
    """
    def __init__(self):
        # Call the parent class to set up the window
        super().__init__()
        # Loads the texture to become sprites of the bob, and the background
        self.bob_texture = arcade.load_texture("assets/bobber.png")
        self.bob_sprite = arcade.Sprite(self.bob_texture, 0.70)
        self.background_texture = arcade.load_texture("assets/background.png")
        self.background_sprite = arcade.Sprite(self.background_texture)

        self.player_list = arcade.SpriteList()
        self.player_texture = None
        self.player_animation = None
        self.is_animate = False

        self.fish_list = arcade.SpriteList()

        # Loop variables
        # The time in a day
        self.timer = 0
        # Which day it is
        self.day = 0
        # TBD if this shows up all day or only when the day starts and between the days?
        self.day_text = arcade.Text(f"Day: {self.day}", WINDOW_WIDTH/2-70, 50, font_name='Pixeled',
                                    color=arcade.color.WHITE)
        self.game_time_minutes = 6 * 60
        self.clock_speed = 4.8 # 1 real second = 4.8 in-game minute
        self.clock_text = arcade.Text('', x=1100, y=700, font_name='Pixeled')
        self.balance = 0
        self.balance_text = arcade.Text(f'Money: {self.balance}', x=1100, y=600, font_name='Pixeled')
        # How much money we have
        self.money = 0
        # All the mini timers that are needed to keep track of certain variables
        # This timer counts how long a label should last on the screen for
        self.label_timer_ticks = 0
        # This timer counts how long it should take before the bobber starts to move
        self.bobber_ticks = 0
        # This timer gives us how long we have after the bobber bobs and we have to fish
        self.fish_ticks = 0
        # This timer counts how long we should keep the missed fish label for
        self.missed_ticks = 0
        # This timer is for the bobbing animation to happen
        self.change_ticks = 0
        # This shows how many seconds are needed before a fish pops up
        self.fish = random.randint(180, 300)
        # Sets the position of the background image
        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2
        # Sets the position of the bobber sprite
        self.bob_sprite.center_x = 1160
        self.bob_sprite.center_y = 0
        # The money quota for the first day
        self.money_quota = 250
        self.quota_text = arcade.Text(f"Quota: {self.money_quota}", 1100, 650,
                                      font_name='Pixeled')
        # Lets us know when the bobber sprite should start bobbing
        self.fish_is_ready = False
        # Lets us know when the bobber gets thrown into the water
        self.bobber_animation = False
        # Lets us know when the person starts fishing, as soon as the mouse is clicked
        self.is_fishing = False
        # Once you successfully click when the bobber moves, the minigame shall activate
        self.fishing_minigame_activate = False
        # Lets us know once we lose the game, not enough money to meet the daily quota
        self.lose = False
        # Variable that lets us show a missed fish label for a few seconds
        self.show_missed_label = False
        # Variable to see when fish should fly towards the player
        self.fish_animation = False
        self.fish_timer = 0
        # Creates and enables the manager for the gui package
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Creates two buttons from textures
        default_button = arcade.load_texture('assets/default_button.png')
        press_button = arcade.load_texture('assets/pressed_button.png')
        # The function from the gui manager to create a button, uses a custom texture.
        self.button = UITextureButton(x=50, y=50, texture=default_button, texture_pressed=press_button, scale=0.6)
        self.clicked_button = False
        self.button.visible = False
        # Specifically used to register and track clicks on the button. The way this works is slightly unknown.
        self.button.on_click = self.button_clicked
        self.manager.add(self.button)

        # Player texture
        self.player_texture = arcade.load_spritesheet("assets/fisherman.png")
        # Block of code that creates an animation (for player). Creates a texture list and adds all the frames to this
        # list. Then creates the sprite using a function.
        texture_list = self.player_texture.get_texture_grid(size=(1350, 756), columns=8, count=8)
        frames = []
        for text in texture_list:
            frames.append(arcade.TextureKeyframe(text, duration=200))
        self.anim = arcade.TextureAnimation(frames)
        self.player_animation = arcade.TextureAnimationSprite(675, 375, animation=self.anim)
        self.player_list.append(self.player_animation)
        self.player_anim_ticks = 0

        # Lets us know when the main loop is going on and not any minigames
        self.main_loop = True
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        # Chooses a random fish from the FISH_LIST with specific weights/chances. Then creates the specific fish sprite.
        current_fish = random.choices(FISH_LIST, weights=[0.20, 0.20, 0.15, 0.15, 0.05, 0.05,
                                                          0.025, 0.025, 0.02, 0.02, 0.11], k=1)[0]
        self.current_fish = fish_data[current_fish][5]
        self.current_fish_price = fish_data[current_fish][1]
        self.current_fish_texture = arcade.load_texture(self.current_fish)
        self.current_fish_sprite = arcade.Sprite(self.current_fish_texture)
        print(self.current_fish)
        self.current_fish_sprite.position = 1550, -105

        self.fish_list.append(self.current_fish_sprite)
        # Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.current_fish_sprite, None, GRAVITY-1, None,
                                                             self.player_list)

        self.start_animate = False
        self.fish_done = False
        self.fish_variable = 0

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""
        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()
        # Draw the background
        arcade.draw_sprite(self.background_sprite)
        # Draws all the gui such as the button.
        self.manager.draw()

        # Drawing all the sprites
        self.fish_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.clock_text.draw()
        self.balance_text.draw()
        self.current_fish_sprite.draw_hit_box()
        self.player_animation.draw_hit_box()

        # Draws the missed fish text once we miss a fish
        if self.show_missed_label:
            arcade.draw_text(f"You missed the fish", WINDOW_WIDTH/2-90, 350, arcade.color.GOLD)
        # Draws the quota
        self.quota_text.draw()
        # Shows what day it is at the bottom of the screen
        self.day_text.draw()
        # Once the fishing starts, draw the bobber and start counting the time before the bobber should start moving
        if self.is_fishing:
            self.bobber_animation = True
            arcade.draw_sprite(self.bob_sprite)

    def on_update(self, delta_time):
        # Physics engine will update if fish needs to move.
        if self.fish_animation:
            self.physics_engine.update()
        # If player is needed to be animated from mouse button left click, then the frames will start looping.
        if self.is_animate:
            # Loops through all the frames
            self.player_anim_ticks += delta_time
            if self.player_anim_ticks <= self.anim.duration_seconds:
                self.player_list.update_animation(delta_time)
            else:
                # Stops when all frames are looped through.
                self.player_anim_ticks = 0
                self.is_animate = False
                # Reset to first frame so it starts fresh next time
                self.player_animation.current_keyframe_index = 0
                self.player_animation.texture = self.anim.keyframes[0].texture

        # Tick timer, every tick add one there are 60 ticks in a second
        self.timer += 1
        # Code for clock. Will fully comment later...
        self.game_time_minutes += delta_time * self.clock_speed
        self.game_time_minutes %= 1440
        hours = int(self.game_time_minutes) // 60
        minutes = int(self.game_time_minutes) % 60
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 or 12
        self.clock_text.text = f"Time: {display_hours:02}:{minutes:02} {am_pm}"
        if hours == 0:
            self.window.show_view(BetweenDayView(self.money_quota, self.balance, self.day))

        # If you miss a fish, this will allow a label to be drawn for only 1 second
        if self.show_missed_label:
            self.missed_ticks += 1
            if self.missed_ticks == 60:
                self.missed_ticks = 0
                self.show_missed_label = False
        # Counts how many ticks the bobber has been in the water for, if it matches self.fish,
        # Start the bobbing animation as a fish is on the line and start a counter for
        # how many seconds you have to catch the fish
        if self.bobber_animation:
            self.bobber_ticks += 1
            if self.bobber_ticks == 250:
                self.fish_is_ready = True
                self.bobber_animation = False
                self.bobber_ticks = 0
        # Once the fish is on the line, start a timer so the bobber can move, after 3 seconds
        if self.fish_is_ready:
            # Animation of bobber by changing angles and y by using math.
            # Current amplitude (2.5px) and frequency (0.25 Hz).
            bobbing_offset = math.sin(self.timer * 0.25) * 2.5
            self.bob_sprite.center_y = 0 + bobbing_offset
            # Current amplitude (1px) and frequency (0.1 Hz)
            self.bob_sprite.angle = math.sin(self.timer * 0.1) * 1
            self.fish_ticks += 1
            self.button.visible = True
            if self.fish_is_ready:
                self.fish_ticks += 1
                self.button.visible = True
                # Has three seconds to click button
                if self.fish_ticks < 240:
                    # Button is clicked within time limit
                    if self.clicked_button:
                        print("minigame activated")
                        self.fishing_minigame_activate = True
                        self.fish_animation = True
                        self.show_missed_label = False
                        # Resets all variables back to default.
                        self.clicked_button = False
                        self.fish_ticks = 0
                        self.fish_is_ready = False
                        self.is_fishing = False
                        self.button.visible = False
                        self.bobber_animation = False
                        self.main_loop = True
                # Button is not clicked within time limit.
                else:
                    self.clicked_button = False
                    self.fish_ticks = 0
                    self.fish_is_ready = False
                    self.is_fishing = False
                    self.button.visible = False
                    self.bobber_animation = False
                    self.main_loop = True
                    self.show_missed_label = True

        # Fish animation (changes y and x)
        if self.fish_animation and self.fish_variable == 0:
            self.fish_variable = 1
            self.physics_engine.jump(42)
            self.current_fish_sprite.change_x = -9.5

        if 969 > self.current_fish_sprite.center_x > 784:
            if self.current_fish_sprite.center_y >= 430:
                self.start_animate = True
                self.fish_animation = False
        # Currently this code is slightly broken and not optimized for all the fish... ex. rainbow trout 'stuck' on
        # player for unknown reason. Also need to make exception for naval mine because that won't be launched out.
        if self.start_animate:
            # Gently override position to simulate float
            self.current_fish_sprite.center_y += math.sin(self.timer * 0.1) * 6
            self.fish_timer += 1
            if self.fish_timer == 150 and not self.fish_done:
                self.fish_list.clear()
                self.fish_timer = 0
                self.balance += self.current_fish_price
                self.balance_text.text = f'Money: {self.balance}'
                self.fish_done = True
                self.current_fish_sprite.position = 1500, -60
            self.start_animate = False
            self.fish_variable = 0

    # Function specifically for registering clicks from the button. Once the button is clicked, this function will run.
    def button_clicked(self, event):
        if self.fish_is_ready:
            self.clicked_button = True

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.SPACE:
            game_view = BetweenDayView(self.money_quota, self.balance, self.day)
            self.window.show_view(game_view)

    def on_mouse_press(self, x, y, button, modifiers):
            # Calls the actual fishing mechanic through left click.
            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.main_loop:
                    self.main_loop = False
                    self.is_fishing = True
                    self.is_animate = True
            print(x,y)

    def new_day(self):
        # Every new day the quota goes up by 10$ and the counter increases while the timer resets
        self.money_quota += 50
        self.quota_text.text = f"Quota: {self.money_quota}"
        self.day += 1
        self.day_text.text = f'Day: {self.day}'
        self.balance = 0
        self.balance_text.text = f'Money: {self.balance}'
        self.timer = 0

class GameStartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_texture = arcade.load_texture('assets/start_screen.png')
        self.background = arcade.Sprite(self.background_texture)
        self.background.position = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        button_style = {
            "normal": {
                'font_name': 'Pixeled',
                'font_color': arcade.color.WHITE,
                'bg': uicolor.DARK_BLUE_MIDNIGHT_BLUE
            },
            'hover': {
                'font_name': 'Pixeled',
                'font_color': uicolor.DARK_BLUE_MIDNIGHT_BLUE,
                'bg': uicolor.WHITE_CLOUDS
            },
            'press': {
                'font_name': 'Pixeled',
                'font_color': arcade.color.WHITE,
                'bg': uicolor.DARK_BLUE_MIDNIGHT_BLUE
            }
        }
        start_button = arcade.gui.UIFlatButton(text="Start", width=200, x=WINDOW_WIDTH // 2-70,
                                                  y=WINDOW_HEIGHT // 2-65,
                                                  style=button_style)
        self.manager.add(start_button)

        @start_button.event('on_click')
        def on_click_settings(event):
            self.window.show_view(GameView())

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        self.manager.draw()


class BetweenDayView(arcade.View):
    def __init__(self, money_quota, balance, day):
        super().__init__()
        self.money_quota = money_quota
        self.balance = balance
        self.day = day
        self.count = 0
        self.background_texture = arcade.load_texture('assets/end_day_bg.png')
        self.background = arcade.Sprite(self.background_texture)
        self.background.position = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.quota_text = arcade.Text(f'Quota: {self.count}', WINDOW_WIDTH//2-75, 300, arcade.color.GOLD,
                                      font_name='Pixeled')
        self.day_text = arcade.Text(f'Day: {self.day}', WINDOW_WIDTH//2-50, 700, arcade.color.WHITE,
                                    font_name='Pixeled', font_size=20)
        self.failed = False
        self.continue_day = False
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.main_window = GameView()
        # Make sure to add fonts and other things later...
        # Define styles for different button states
        button_style = {
            "normal": {
                'font_name': 'Pixeled',
                'font_color': arcade.color.WHITE,
                'bg': uicolor.DARK_BLUE_MIDNIGHT_BLUE
            },
            'hover': {
                'font_name' : 'Pixeled',
                'font_color': uicolor.DARK_BLUE_MIDNIGHT_BLUE,
                'bg': uicolor.WHITE_CLOUDS
            },
            'press': {
                'font_name': 'Pixeled',
                'font_color': arcade.color.WHITE,
                'bg': uicolor.DARK_BLUE_MIDNIGHT_BLUE
            }
        }
        self.continue_button = arcade.gui.UIFlatButton(text="Next Day", width=200, x=WINDOW_WIDTH//2-100, y=WINDOW_HEIGHT//2,
                                                  style=button_style)
        self.failed_button = arcade.gui.UIFlatButton(text="Back to Menu", width=200, x=WINDOW_WIDTH//2-100,
                                                                  y=WINDOW_HEIGHT//2, style=button_style)

        self.failed_button.on_click = self.clicked_failed_button
        self.continue_button.on_click = self.clicked_continue_button

    def clicked_failed_button(self, event):
        self.window.show_view(GameStartView())
        self.manager.remove(self.failed_button)
        self.failed = False
    def clicked_continue_button(self, event):
        self.main_window.new_day()
        self.window.show_view(self.main_window)
        self.manager.remove(self.continue_button)
        self.continue_day = False

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # If quota is completed, then count up the quota... counting the entire balance normally takes too long.
        if self.balance >= self.money_quota > self.count:
            self.count += 1
            if self.count == self.money_quota:
                self.continue_day = True
        # If quota is not completed, count up the balance
        elif self.count < self.balance < self.money_quota:
            self.count += 1
            if self.count == self.balance:
                self.failed = True
        self.quota_text.text = f'Quota: {self.count}'
        if self.continue_day:
            self.manager.add(self.continue_button)
        elif self.failed:
            self.manager.add(self.failed_button)

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        self.quota_text.draw()
        self.day_text.draw()
        if self.continue_day or self.failed:
            self.manager.draw()

def main():
   """Main function"""
   window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
   start_view = GameStartView()
   window.show_view(start_view)
   start_view.setup()
   arcade.run()

if __name__ == "__main__":
   main()
