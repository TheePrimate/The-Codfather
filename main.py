# Main game loop goes here
import arcade
import arcade.gui
from arcade.gui import UIManager, UITextureButton, UIDropdown, UISlider

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
        self.fish_texture = arcade.load_texture("assets/cod.png")
        self.fish_sprite = arcade.Sprite(self.fish_texture)

        self.player_list = arcade.SpriteList()
        self.player_texture = None
        self.player_animation = None
        self.is_animate = False
        self.mouse_button_clicked = False

        # Loop variables
        # The time in a day
        self.timer = 0
        # Which day it is
        self.day = 0
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
        self.fish = random.randint(0, 100)
        # Sets the position of the background image
        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2

        self.fish_sprite.center_x = 1150
        self.fish_sprite.center_y = 300

        # Sets the position of the bobber sprite
        self.bob_sprite.center_x = 1160
        self.bob_sprite.center_y = 0
        # The money quota for the first day
        self.money_quota = 100
        # Lets us know when the bobber sprite should start bobbing
        self.fish_is_ready = False
        # Lets us know when the bobber gets thrown into the water
        self.bobber_animation = False
        # Lets us show the days quota for only a certain amount of time
        self.show_quota_label = False
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

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        ''''
        self.slider = UISlider(x=500, y=250)
        self.dropdown = UIDropdown(x=500, y=500, options=['1', '2', '3'])
        self.manager.add(self.dropdown)
        self.manager.add(self.slider)
        '''
        texture = arcade.load_texture('assets/arbitrary_asset.png')
        texture_hover = arcade.load_texture('assets/albatross.png')
        self.button = UITextureButton(x=random.randint(100, 1250), y=random.randint(50, 700), texture=texture,
                                      texture_pressed=texture_hover)
        self.clicked_button = None
        self.button.on_click = self.button_clicked
        self.button.visible = False
        self.manager.add(self.button)

        self.player_texture = arcade.load_spritesheet("assets/fisherman.png")
        texture_list = self.player_texture.get_texture_grid(size=(1350, 756), columns=40, count=40)
        frames = []
        for text in texture_list:
            frames.append(arcade.TextureKeyframe(text))
        anim = arcade.TextureAnimation(frames)
        self.player_animation = arcade.TextureAnimationSprite(675, 375, animation=anim)
        self.player_list.append(self.player_animation)
        self.player_anim_ticks = 0


        # Lets us know when the main loop is going on and not any minigames
        self.main_loop = True
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        current_fish = random.choices(FISH_LIST, weights=[0.20, 0.20, 0.15, 0.15, 0.05, 0.05,
                                                          0.025, 0.025, 0.02, 0.02, 0.11], k=1)[0]
        self.current_fish = fish_data[current_fish][4]
        self.current_fish_texture = arcade.load_texture(self.current_fish)
        self.current_fish_sprite = arcade.Sprite(self.current_fish_texture)
        self.current_fish_sprite.position = self.bob_sprite.center_x-300, 200

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.current_fish_sprite, None, GRAVITY-1, None,
                                                             self.player_list)
        self.physics_engine1 = arcade.PhysicsEnginePlatformer(self.fish_sprite, None, GRAVITY-1.5, None,)
        self.fish_variable = 0

    def button_clicked(self, event):
        self.clicked_button = 'pressed'
        self.fishing_minigame_activate = True
        print('minigame activated')
        self.fish_is_ready = False
        self.is_fishing = False
        self.bobber_animation = False
        self.main_loop = True
        self.button.x, self.button.y = random.randint(100, 1250), random.randint(50, 700)
        self.button.visible = False
        self.fish_ticks = 0
        self.mouse_button_clicked = False


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
        self.manager.draw()

        arcade.draw_sprite(self.current_fish_sprite)
        self.player_list.draw(pixelated=True)
        self.current_fish_sprite.draw_hit_box()

        # Draws the missed fish text once we miss a fish
        if self.show_missed_label:
            arcade.draw_text(f"You missed the fish", WINDOW_WIDTH/2-90, 350, arcade.color.GOLD)
        # Draws the quota every new day
        if self.show_quota_label:
            arcade.draw_text(f"Today's Quota: ${self.money_quota}",WINDOW_WIDTH/2-180, 700, arcade.color.YELLOW,24)
        # Shows what day it is at the bottom of the screen
        arcade.draw_text(f"Day: {self.day}", WINDOW_WIDTH/2-70, 50, arcade.color.GREEN, 30)
        # Once the fishing starts, draw the bobber and start counting the time before the bobber should start moving
        if self.is_fishing:
            self.bobber_animation = True
            arcade.draw_sprite(self.bob_sprite)
<<<<<<< HEAD
=======
        if self.button_appear:
            arcade.draw_circle_filled(self.buttonX, self.buttonY, radius=50,
                                      color=(30, 30, 30, 200))
            self.button_message.draw()
        if self.fish_animation:
            arcade.draw_sprite(self.fish_sprite)
>>>>>>> 97743f9e6847f726233d124e071ff8e4812f029c

    def on_update(self, delta_time):
        self.physics_engine.update()
        if self.fish_animation:

            self.physics_engine1.update()

        if self.is_animate:
            self.player_anim_ticks += 1
            self.player_list.update_animation()
            if self.player_anim_ticks == 250:
                self.is_animate = False
                self.player_anim_ticks = 0


        # Tick timer, every tick add one there are 60 ticks in a second
        self.timer += 1
        # Every 5 minutes or 18000 ticks trigger a new day with the trigger mob function
        if self.timer % 400 == 0:
            self.trigger_mob()
        # If you miss a fish, this will allow a label to be drawn for only 1 second
        if self.show_missed_label:
            self.missed_ticks += 1
            if self.missed_ticks == 60:
                self.missed_ticks = 0
                self.show_missed_label = False
        # Shows a quota at the start of a new day for 4 seconds
        if self.show_quota_label:
            self.label_timer_ticks += 1
            if self.label_timer_ticks >= 240:
                self.show_quota_label = False
                self.label_timer_ticks = 0
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
            # Current amplitude (2.5px) and frequency (0.25 Hz)
            bobbing_offset = math.sin(self.timer * 0.25) * 2.5
            self.bob_sprite.center_y = 0 + bobbing_offset
            # Current amplitude (1px) and frequency (0.1 Hz)
            self.bob_sprite.angle = math.sin(self.timer * 0.1) * 1
            self.fish_ticks += 1
            self.button.visible = True
            if self.fish_ticks < 180:
                if self.mouse_button_clicked:
                    self.show_missed_label = True
                    self.fish_is_ready = False
                    self.is_fishing = False
                    self.bobber_animation = False
                    self.main_loop = True
                    self.button.x, self.button.y = random.randint(100, 1250), random.randint(50, 700)
                    self.button.visible = False
                    self.fish_ticks = 0
                self.mouse_button_clicked = False
            else:
                self.fish_ticks = 0
                self.is_fishing = False
                self.button.visible = False
                self.bobber_animation = False
                self.button.x, self.button.y = random.randint(100, 1250), random.randint(50, 700)
                self.show_missed_label = True
                self.fish_is_ready = False
                self.main_loop = True
                self.mouse_button_clicked = False


        if self.fish_animation and self.fish_variable == 0:
            self.fish_variable = 1
            self.fish_sprite.change_x = -5
            self.fish_sprite.change_y = 15

        if self.fish_sprite.center_x == 900:
            self.fish_animation = False
            self.fish_sprite.center_x = 1150
            self.fish_sprite.center_y = 300
            self.fish_sprite.change_y = 15





    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.SPACE:
            print(self.timer)
            print(self.fish)
            print(self.is_fishing)
            print(self.bobber_ticks)

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.main_loop:
                self.main_loop = False
                self.is_fishing = True
                self.is_animate = True
            if self.fish_is_ready:
<<<<<<< HEAD
                self.mouse_button_clicked = True

=======
                if self.fish_ticks < 180 and distance_squared <= 50**2:
                    self.fish_animation = True
                    self.fishing_minigame_activate = True
                    print('minigame activated')
                    self.fish_is_ready = False
                    self.is_fishing = False
                    self.bobber_animation = False
                    self.main_loop = True
                    self.buttonX, self.buttonY = random.randint(100, 1250), random.randint(50, 700)
                    self.button_message.x, self.button_message.y = self.buttonX, self.buttonY
                    self.button_appear = False
                    self.fish_ticks = 0
                else:
                    self.show_missed_label = True
                    self.fish_is_ready = False
                    self.is_fishing = False
                    self.bobber_animation = False
                    self.main_loop = True
                    self.buttonX, self.buttonY = random.randint(100, 1250), random.randint(50, 700)
                    self.button_message.x, self.button_message.y = self.buttonX, self.buttonY
                    self.fish_ticks = 0
                    self.button_appear = False
>>>>>>> 97743f9e6847f726233d124e071ff8e4812f029c

    def trigger_mob(self):
        # Every new day the quota goes up by 10$ and the counter increases while the timer resets
        self.money_quota += 10
        self.day += 1
        self.show_quota_label = True
        self.timer = 0



class GameStartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("assets/arbitrary_asset.png")

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        arcade.draw_text("Start Screen", 100, 300, arcade.color.WHITE, 30)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            game_view = RulesView()
            self.window.show_view(game_view)


class RulesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("assets/arbitrary_asset.png")

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        arcade.draw_text("Rules Screen", 100, 300, arcade.color.WHITE, 30)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            game_view = GameStartView()
            self.window.show_view(game_view)

def main():
   """Main function"""
   window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
   start_view = GameStartView()
   window.show_view(start_view)
   start_view.setup()
   arcade.run()

if __name__ == "__main__":
   main()
