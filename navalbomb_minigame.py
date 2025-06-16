from library import *

WINDOW_TITLE = "Starting Template"


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK
        self.fish = "mine"
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
        # If you have sprite lists, you should create them here,
        # and set them to None

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

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        self.camera_shake.update_camera()
        self.camera_sprites.use()

        # Call draw() on all your sprite lists below
        if self.fish == "mine":
            self.mine_list.draw(pixelated=True)
            arcade.draw_lrbt_rectangle_filled(103, 165.4, 219, 219+self.sanity,
                                              arcade.color.AIR_SUPERIORITY_BLUE)
            # Draw insanity blackout
            arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, color=(0, 0, 0, self.blackout))

        self.camera_shake.readjust_camera()

        if self.fish == "disarmed":
            self.defusal_list.draw(pixelated=True)
            self.jeep_list.draw(pixelated=True)

    def on_update(self, delta_time):
        if self.jeep_flag:
            self.jeep_list.update_animation()
        self.camera_shake.update(delta_time)
        # If the naval mine mini-game is engaged execute the following
        if self.fish == "mine":
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

        if self.fish == "disarmed":
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
                    self.fish = "None"
                if self.jeep_tertiary_flag == 2:
                    self.defusal_list.pop()

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
        if self.fish == "mine":
            if 455 < self.hand_sprite.center_x < 500:
                self.fish = "disarmed"
                self.camera_shake.stop()
            elif (370 < self.hand_sprite.center_x < 400 or 600 < self.hand_sprite.center_x < 630 or 500 <
                  self.hand_sprite.center_x < 530):
                self.death = True
            else:
                self.spont_combst_chance += 30
            if self.spont_combst_chance == 100:
                self.death = True

                
def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and set up the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
