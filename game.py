from library import *


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__()
        '''Fishing Minigame Init'''

        self.fishing_ticks = 0
        self.fishing_seconds = 0
        self.universal_ticks = 0
        self.indicator_seconds = 0
        self.indicator_change_speed = 0
        self.indicator_change_direction = 0
        self.indicator_change_speed_ticks = 0
        self.indicator_change_direction_ticks = 0
        self.mouse_hold = False
        self.choose_fish = True
        self.current_minigame = None

        self.sprite_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.current_fish_list = arcade.SpriteList()
        self.wall_block = arcade.SpriteList()
        self.progress_bar_height = 0

        self.background_texture = arcade.load_texture('assets/background.png')
        self.background_sprite = arcade.Sprite(self.background_texture)
        self.background_sprite.center_x = WINDOW_WIDTH / 2
        self.background_sprite.center_y = WINDOW_HEIGHT / 2
        self.background_list.append(self.background_sprite)

        self.background_bar_texture = arcade.load_texture("assets/blue.png")
        self.background_bar_sprite = arcade.Sprite(self.background_bar_texture)
        self.background_bar_sprite.center_x = FISHING_MINIGAME_X
        self.background_bar_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.background_bar_sprite)

        self.hooking_container_left_texture = arcade.load_texture("assets/left.png")
        self.hooking_container_left_sprite = arcade.Sprite(self.hooking_container_left_texture)
        self.hooking_container_left_sprite.center_x = FISHING_MINIGAME_X
        self.hooking_container_left_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.hooking_container_left_sprite)

        self.hooking_container_right_texture = arcade.load_texture("assets/right.png")
        self.hooking_container_right_sprite = arcade.Sprite(self.hooking_container_right_texture)
        self.hooking_container_right_sprite.center_x = FISHING_MINIGAME_X
        self.hooking_container_right_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.hooking_container_right_sprite)

        self.hooking_container_bot_texture = arcade.load_texture("assets/bot.png")
        self.hooking_container_bot_sprite = arcade.Sprite(self.hooking_container_bot_texture)
        self.hooking_container_bot_sprite.center_x = FISHING_MINIGAME_X
        self.hooking_container_bot_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.hooking_container_bot_sprite)
        self.wall_block.append(self.hooking_container_bot_sprite)

        self.hooking_container_top_texture = arcade.load_texture("assets/top.png")
        self.hooking_container_top_sprite = arcade.Sprite(self.hooking_container_top_texture)
        self.hooking_container_top_sprite.center_x = FISHING_MINIGAME_X
        self.hooking_container_top_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.hooking_container_top_sprite)
        self.wall_block.append(self.hooking_container_top_sprite)

        self.indicator_texture = arcade.load_texture("assets/bar.png")
        self.indicator_sprite = arcade.Sprite(self.indicator_texture)
        self.indicator_sprite.center_x = FISHING_MINIGAME_X
        self.indicator_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.indicator_sprite)

        self.hook_texture = arcade.load_texture("assets/hook.png")
        self.hook_sprite = arcade.Sprite(self.hook_texture)
        self.hook_sprite.center_x = FISHING_MINIGAME_X
        self.hook_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.hook_sprite)

        self.progress_bar_texture = arcade.load_texture("assets/progress_bar.png")
        self.progress_bar_sprite = arcade.Sprite(self.progress_bar_texture)
        self.progress_bar_sprite.center_x = FISHING_MINIGAME_X
        self.progress_bar_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.progress_bar_sprite)

        self.progress_bar_bar_texture = arcade.load_texture("assets/progress_bar_bar.png")
        self.progress_bar_bar_sprite = arcade.Sprite(self.progress_bar_bar_texture)
        self.progress_bar_bar_sprite.center_x = FISHING_MINIGAME_X
        self.progress_bar_bar_sprite.center_y = FISHING_MINIGAME_Y
        self.sprite_list.append(self.progress_bar_bar_sprite)

        self.physics_engine1 = arcade.PhysicsEnginePlatformer(self.hook_sprite, None,
                                                              GRAVITY, None, self.wall_block)
        self.physics_engine2 = arcade.PhysicsEnginePlatformer(self.indicator_sprite, None,
                                                              0, None, self.wall_block)

        self.collision = None

        self.current_value = None
        self.current_time_limit = None
        self.current_fish_sprite = None
        self.current_fish_texture = None
        self.current_difficulty_low = None
        self.current_difficulty_high = None
        self.init_fish_animate = True
        self.animate_fish = None
        self.current_column = None
        self.current_count = None

        '''Naval Bomb Minigame Init'''
        self.mineX = 500
        self.mineY = 530
        self.handX = 500
        self.handY = 340
        self.hand_vel = 5
        self.san_der = 0
        self.sanity = 459
        self.death = False
        self.san_accel = 0
        self.blackout = 0
        self.insanity_flag = False
        self.insanity_check_flag = True
        self.spont_combst_chance = 0
        self.water_leaked = 0
        self.should_init_mine = True
        self.jeep_texture = None
        self.jeep_list = arcade.SpriteList()
        self.jeep_flag = False
        self.anim_jeep = None
        self.jeep_animation = None
        self.jeep_anim_ticks = None
        self.jeep_secondary_flag = True
        self.jeep_tertiary_flag = 0

        # Setup mine sprites
        self.mine_list = arcade.SpriteList()
        self.defusal_list = arcade.SpriteList()

        self.detonator_texture = arcade.load_texture("assets/detonator.png")
        self.detonator_sprite = arcade.Sprite(self.detonator_texture, center_x=451, center_y=450)
        self.defusal_list.append(self.detonator_sprite)

        self.mine_texture = arcade.load_texture("assets/naval_bomb.png")
        self.mine_sprite = arcade.Sprite(self.mine_texture, center_x=self.mineX, center_y=self.mineY)
        self.mine_list.append(self.mine_sprite)
        self.defusal_list.append(self.mine_sprite)
        self.sanity_bar_texture = arcade.load_texture("assets/sanity_bar.png")
        self.sanity_bar_sprite = arcade.Sprite(self.sanity_bar_texture, center_x=FISHING_MINIGAME_X,
                                               center_y=FISHING_MINIGAME_Y)
        self.mine_list.append(self.sanity_bar_sprite)
        self.hand_texture = arcade.load_texture("assets/hand.png")
        self.hand_sprite = arcade.Sprite(self.hand_texture, center_x=self.handX, center_y=340)
        self.mine_list.append(self.hand_sprite)

        # Create camera that will follow the player sprite.
        self.camera_sprites = arcade.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.camera_sprites.view_data,
            max_amplitude=50.0,
            acceleration_duration=0.1,
            falloff_time=100,
            shake_frequency=50.0,
        )

        '''Main Game Loop Init''' 
        # Loads the texture to become sprites of the bob, and the background
        self.bob_texture = arcade.load_texture("assets/bobber.png")
        self.bob_sprite = arcade.Sprite(self.bob_texture, 0.70)
        self.background_texture = arcade.load_texture("assets/background.png")
        self.background_sprite = arcade.Sprite(self.background_texture)

        self.player_list = arcade.SpriteList()
        self.player_texture = None
        self.player_animation = None
        self.is_animate = False

        # Loop variables
        # Which day it is
        self.day = 0
        # TBD if this shows up all day or only when the day starts and between the days?
        self.day_text = arcade.Text(f"Day: {self.day}", WINDOW_WIDTH / 2 - 70, 50, font_name='Pixeled',
                                    font_size=20, color=arcade.color.WHITE)
        self.game_time_minutes = 6 * 60
        self.clock_speed = 4.8  # 1 real second = 4.8 in-game minute
        self.clock_text = arcade.Text('', x=100, y=600, font_size=20, font_name='Pixeled')
        self.balance = 0
        self.balance_text = arcade.Text(f'Money: {self.balance}', x=1000, y=700, font_name='Pixeled', font_size=20)
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

        # Sets the position of the bobber sprite
        self.bob_sprite.center_x = 1160
        self.bob_sprite.center_y = 0
        # The money quota for the first day
        self.money_quota = 250
        self.quota_text = arcade.Text(f"Quota: {self.money_quota}", WINDOW_WIDTH / 2 - 180, 700,
                                      font_name='Pixeled')
        # Lets us know when the bobber sprite should start bobbing
        self.fish_is_ready = False
        # Lets us know when the bobber gets thrown into the water
        self.bobber_animation = False
        # Lets us know when the person starts fishing, as soon as the mouse is clicked
        self.is_fishing = False
        # Once you successfully click when the bobber moves, the minigame shall activate
        self.minigame_activate = False
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
        texture_list = self.player_texture.get_texture_grid(size=(1350, 756), columns=40, count=40)
        frames = []
        for text in texture_list:
            frames.append(arcade.TextureKeyframe(text, duration=50))
        self.anim = arcade.TextureAnimation(frames)
        self.player_animation = arcade.TextureAnimationSprite(675, 375, animation=self.anim)
        self.player_list.append(self.player_animation)
        self.player_anim_ticks = 0

        # Lets us know when the main loop is going on and not any minigames
        self.main_loop = True

        self.start_animate = False
        self.fish_done = False
        self.fish_variable = 0

        
    def init_mine(self):
        self.spont_combst_chance = random.randint(0, 101)
        self.water_leaked = random.randint(1, 16)
        if self.water_leaked == 15:
            self.spont_combst_chance -= 50
        if self.spont_combst_chance == 100:
            self.death = True
        self.handY = 340
        self.jeep_secondary_flag = True
        self.jeep_tertiary_flag = 0

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


        self.background_list.draw()
        # Draws all the gui such as the button.
        self.manager.draw()

        # Drawing all the sprites
        self.player_list.draw(pixelated=True)
        self.clock_text.draw()
        self.balance_text.draw()
        self.current_fish_list.draw(pixelated=True)

        # Draws the missed fish text once we miss a fish
        if self.show_missed_label:
            arcade.draw_text(f"You missed the fish", WINDOW_WIDTH / 2 - 90, 350, arcade.color.GOLD)
        # Draws the quota
        self.quota_text.draw()
        # Shows what day it is at the bottom of the screen
        self.day_text.draw()
        # Once the fishing starts, draw the bobber and start counting the time before the bobber should start moving
        if self.is_fishing:
            self.bobber_animation = True
            arcade.draw_sprite(self.bob_sprite)
        
        if self.current_minigame == "Fishing Minigame" and self.minigame_activate is True:
            self.sprite_list.draw(pixelated=True)

        if self.current_minigame == "Naval Bomb Minigame" and self.minigame_activate is True:
            # when we integrate minigames draw minigame stuff here
            self.mine_list.draw(pixelated=True)
            arcade.draw_lrbt_rectangle_filled(103, 165.4, 219, 219 + self.sanity,
                                              arcade.color.AIR_SUPERIORITY_BLUE)
            # Draw insanity blackout
            arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, color=(0, 0, 0, self.blackout))

        self.camera_shake.readjust_camera()

        if self.current_minigame == "Disarmed":
            self.defusal_list.draw(pixelated=True)
            self.jeep_list.draw(pixelated=True)

    def choose_new_fish(self):
        current_fish = random.choices(FISH_LIST, weights=[0.20, 0.20, 0.15, 0.15, 0.05, 0.05,
                                                          0.025, 0.025, 0.02, 0.02, 0.11], k=1)[0]
        print("Caught:", current_fish)
        print("Minigame Type:", fish_data[current_fish][0])
        print("Worth:", fish_data[current_fish][1], "$")
        print("Lower-Bound Diff:", fish_data[current_fish][2])
        print("Upper-Bound Diff:", fish_data[current_fish][3])
        print("Time Limit:", fish_data[current_fish][4])
        print("Sprite Name:", fish_data[current_fish][5])
        self.current_minigame = fish_data[current_fish][0]
        self.current_value = fish_data[current_fish][1]
        self.current_difficulty_low = fish_data[current_fish][2]
        self.current_difficulty_high = fish_data[current_fish][3]
        self.current_time_limit = fish_data[current_fish][4]
        self.current_fish_sprite = fish_data[current_fish][5]
        self.current_column = fish_data[current_fish][6]
        self.current_count = fish_data[current_fish][7]
        self.choose_fish = False

        return (self.current_value,
                self.current_difficulty_low,
                self.current_difficulty_high,
                self.current_time_limit,
                self.current_fish_sprite)

    def init_new_fish_animate(self):
        self.current_fish_texture = arcade.load_spritesheet(self.current_fish_sprite)
        texture_list = self.current_fish_texture.get_texture_grid(size=(1350, 756),
                                                                  columns=self.current_column,
                                                                  count=self.current_count)
        frames = []
        for tex in texture_list:
            frames.append(arcade.TextureKeyframe(tex))
        anim = arcade.TextureAnimation(frames)
        self.animate_fish = arcade.TextureAnimationSprite(animation=anim)
        self.animate_fish.position = 1550, -105
        self.current_fish_list.append(self.animate_fish)
        self.init_fish_animate = False

    def on_update(self, delta_time):
        if self.choose_fish is True:
            self.choose_new_fish()
        if self.init_fish_animate is True:
            self.init_new_fish_animate()

        self.universal_ticks += 1
        self.sprite_list.update()
        self.physics_engine1.update()
        self.physics_engine2.update()
        self.current_fish_list.update_animation()

        # Physics engine will update if fish needs to move.
        if self.fish_animation:

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


        # Code for clock. Will fully comment later...
        self.game_time_minutes += delta_time * self.clock_speed
        self.game_time_minutes %= 1440
        hours = int(self.game_time_minutes) // 60
        minutes = int(self.game_time_minutes) % 60
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 or 12
        self.clock_text.text = f"Time: {display_hours:02}:{minutes:02} {am_pm}"
        if hours == 0:
            self.new_day()
            self.window.show_view(GameOverView(self.money_quota, self.balance))

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
            bobbing_offset = math.sin(self.universal_ticks * 0.25) * 2.5
            self.bob_sprite.center_y = 0 + bobbing_offset
            # Current amplitude (1px) and frequency (0.1 Hz)
            self.bob_sprite.angle = math.sin(self.universal_ticks * 0.1) * 1
            self.fish_ticks += 1
            self.button.visible = True

            self.fish_ticks += 1
            self.button.visible = True
            # Has three seconds to click button
            if self.fish_ticks < 240:
                # Button is clicked within time limit
                if self.clicked_button:
                    print("Minigame Activated")
                    self.choose_fish = True
                    self.minigame_activate = True
                    self.fish_animation = True
                    self.show_missed_label = False
                    # Resets all variables back to default.
                    self.clicked_button = False
                    self.fish_ticks = 0
                    self.fish_is_ready = False
                    self.is_fishing = False
                    self.button.visible = False
                    self.bobber_animation = False
                    self.main_loop = False
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
            self.animate_fish.change_x = -10

        if 950 > self.animate_fish.center_x > 720:
            if self.animate_fish.center_y >= 420:
                self.start_animate = True
                self.fish_animation = False
        # Currently this code is slightly broken and not optimized for all the fish... ex. rainbow trout 'stuck' on
        # player for unknown reason. Also need to make exception for naval mine because that won't be launched out.
        if self.start_animate:
            # Gently override position to simulate float
            self.animate_fish.center_y += math.sin(self.universal_ticks * 0.1) * 6
            self.fish_timer += 1
            if self.fish_timer == 180 and not self.fish_done:
                self.current_fish_list.clear()
                self.fish_timer = 0
                self.fish_done = True
                self.animate_fish.position = 1500, -60
            self.start_animate = False

        if self.jeep_flag:
            self.jeep_list.update_animation()
        self.camera_shake.update(delta_time)
        if self.minigame_activate is True:
            self.collision = arcade.check_for_collision(self.hook_sprite, self.indicator_sprite)
            if self.current_minigame == "Fishing Minigame":
                if self.collision is True:
                    self.fishing_ticks += 1
                    if self.progress_bar_bar_sprite.height < 1700:
                        self.progress_bar_bar_sprite.bottom = 235
                        self.progress_bar_bar_sprite.height += 3
                    if self.progress_bar_bar_sprite.height >= 1700:
                        self.balance += self.current_value
                        self.balance_text.text = f'Money: {self.balance}'
                        self.current_minigame = None
                        self.progress_bar_bar_sprite.height = 756
                        print("Mini Game Successful")
                        self.main_loop = True
                    if self.fishing_ticks % TICK_RATE == 0:
                        self.fishing_seconds += 1
                        print("Progress:", self.fishing_seconds)
                else:
                    if self.progress_bar_bar_sprite.height > 0:
                        self.progress_bar_bar_sprite.bottom = 235
                        self.progress_bar_bar_sprite.height -= 3
                        if self.universal_ticks % TICK_RATE == 0:
                            self.indicator_seconds += 1
                            print("Losing:", self.indicator_seconds)
                            if self.indicator_seconds == self.current_time_limit:
                                self.current_minigame = None
                                self.main_loop = True
                                self.progress_bar_bar_sprite.height = 756
                                print("Mini Game Failed")
                        if self.progress_bar_bar_sprite.height == 0:
                            self.current_minigame = None
                            self.main_loop = True
                            self.progress_bar_bar_sprite.height = 756
                            print('Mini Game Failed')
                self.indicator_change_direction = random.randint(0, 1)
                self.indicator_change_speed_ticks = random.randint(1, 2) * TICK_RATE
                self.indicator_change_direction_ticks = random.randint(1, 2) * TICK_RATE

                if self.universal_ticks % self.indicator_change_speed_ticks == 0:
                    self.indicator_sprite.change_y = random.randint(self.current_difficulty_low,
                                                                    self.current_difficulty_high)

                if self.universal_ticks % self.indicator_change_direction_ticks == 0:
                    if self.indicator_change_direction == 1:
                        self.indicator_sprite.change_y = -self.indicator_sprite.change_y

                if self.mouse_hold:
                    self.hook_sprite.change_y = HOOK_MOVEMENT_SPEED
                else:
                    self.hook_sprite.change_y = -HOOK_MOVEMENT_SPEED

            if self.current_minigame == "Naval Bomb Minigame":
                # this is where naval bomb minigame will go
                if self.should_init_mine:
                    self.should_init_mine = False
                    self.init_mine()
                # Oscillate hand
                if self.hand_sprite.center_x <= 300:
                    self.san_der = True
                    self.hand_vel = 0
                elif self.hand_sprite.center_x >= 700:
                    self.san_der = False
                    self.hand_vel = 0
                if self.san_der:
                    self.hand_vel += 1 + self.san_accel
                if not self.san_der:
                    self.hand_vel -= 1 + self.san_accel

                self.hand_sprite.center_x += self.hand_vel

                # Sanity
                if self.sanity != 218.5:
                    self.sanity -= 0.5
                self.san_accel += 0.005
                if self.blackout < 254:
                    self.blackout += 0.3

                if self.sanity <= 225 and self.insanity_check_flag:
                    self.insanity_check_flag = False
                    self.insanity_flag = True

                # Go crazy
                if self.insanity_flag:
                    self.insanity_flag = False
                    self.camera_shake.start()

            if self.current_minigame == "Disarmed":
                self.balance += self.current_value
                self.balance_text.text = f'Money: {self.balance}'
                if self.detonator_sprite.center_y > 250:
                    self.detonator_sprite.center_y -= 1
                else:
                    self.handY -= 1
                if self.handY == 300:
                    self.handY = 340
                    self.detonator_sprite.alpha = 0
                    if self.jeep_secondary_flag:
                        self.init_b_and_m()
                    self.jeep_flag = True
                    self.jeep_tertiary_flag += 1
                    if self.jeep_tertiary_flag == 3:
                        self.jeep_list.pop()
                        self.jeep_flag = False
                        self.current_minigame = "None"
                    if self.jeep_tertiary_flag == 2:
                        self.defusal_list.pop()
                self.main_loop = True

    # Function specifically for registering clicks from the button. Once the button is clicked, this function will run.
    def button_clicked(self, event):
        if self.fish_is_ready:
            self.clicked_button = True

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.SPACE:
            print(self.universal_ticks)
            print(self.fish)
            print(self.is_fishing)
            print(self.bobber_ticks)
            game_view = GameOverView(self.money_quota, self.balance)
            self.window.show_view(game_view)

    def init_b_and_m(self):
        self.jeep_texture = arcade.load_spritesheet("assets/b_and_m.png")
        texture_list = self.jeep_texture.get_texture_grid(size=(1350, 756), columns=40, count=40)
        frames = []
        for text in texture_list:
            frames.append(arcade.TextureKeyframe(text, duration=50))
        self.anim_jeep = arcade.TextureAnimation(frames)
        self.jeep_animation = arcade.TextureAnimationSprite(675, 375, animation=self.anim_jeep)
        self.jeep_list.append(self.jeep_animation)
        self.jeep_anim_ticks = 0
        self.jeep_secondary_flag = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.main_loop:
                self.main_loop = False
                self.is_fishing = True
                self.is_animate = True
            self.mouse_hold = True
            if self.current_minigame == "Naval Bomb Minigame":
                if 455 < self.hand_sprite.center_x < 500:
                    self.current_minigame = "Disarmed"
                    self.camera_shake.stop()
                elif (370 < self.hand_sprite.center_x < 400 or 600 < self.hand_sprite.center_x < 630 or 500 <
                      self.hand_sprite.center_x < 530):
                    self.death = True
                else:
                    self.spont_combst_chance += 30
                if self.spont_combst_chance == 100:
                    self.death = True
    def new_day(self):
        # Every new day the quota goes up by 10$ and the counter increases while the timer resets
        self.money_quota += 50
        self.day += 1
        self.universal_ticks = 0

    def on_mouse_release(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = False
            
            
class GameStartView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Start Screen", 100, 300, arcade.color.WHITE, 30)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pass

class GameOverView(arcade.View):
    def __init__(self, money_quota, balance):
        super().__init__()
        self.money_quota = money_quota
        self.balance = balance
        self.count = 0
        self.background_texture = arcade.load_texture('assets/end_day_bg.png')
        self.background = arcade.Sprite(self.background_texture)
        self.background.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.quota_text = arcade.Text(f'Quota: {self.count}', WINDOW_WIDTH//2, 300, arcade.color.GOLD,
                                      font_name='Pixeled')
        self.failed = False
        self.continue_day = False
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Make sure to add fonts and other things later...
        continue_button = arcade.gui.UIFlatButton(text="Next Day", width=200, x=WINDOW_WIDTH//2, y=200)
        self.manager.add(continue_button)
        @continue_button.event('on_click')
        def on_click_settings(event):
            game_view = GameView()
            self.window.show_view(game_view)

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_update(self, delta_time):
        # If quota is completed, then count up the quota... counting the entire balance normally takes too long.
        if self.balance >= self.money_quota > self.count:
            self.count += 1
            if self.count == self.money_quota:
                self.continue_day = True
        # If quota is not completed, count up the balance
        elif self.count < self.balance < self.money_quota:
            self.count += 1
            self.failed = True
        self.quota_text.text = f'Quota: {self.count}'



    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        self.quota_text.draw()
        if self.continue_day:
            self.manager.draw()

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
