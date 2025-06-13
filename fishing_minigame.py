from library import *


class FishingMiniGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.fishing_ticks = 0
        self.fishing_seconds = 0
        self.indicator_ticks = 0
        self.indicator_seconds = 0
        self.indicator_change_speed = 0
        self.indicator_change_direction = 0
        self.indicator_change_speed_ticks = 0
        self.indicator_change_direction_ticks = 0
        self.mouse_hold = False
        self.draw_fish = True
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
        self.current_sprite = None
        self.current_fish_texture = None
        self.current_fish_sprite = None
        self.current_difficulty_low = None
        self.current_difficulty_high = None
        self.init_fish_animate = True
        self.animate_fish = None
        self.current_column = None
        self.current_count = None

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
        if self.current_minigame == "Fishing Minigame":
            self.sprite_list.draw(pixelated=True)
            self.current_fish_list.draw(pixelated=True)

        if self.current_minigame == "Naval Bomb Minigame":
            # when we integrate minigames draw minigame stuff here
            self.current_fish_list.draw(pixelated=True)

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
        self.current_sprite = fish_data[current_fish][5]
        self.current_column = fish_data[current_fish][6]
        self.current_count = fish_data[current_fish][7]
        self.choose_fish = False

        return (self.current_value,
                self.current_difficulty_low,
                self.current_difficulty_high,
                self.current_time_limit,
                self.current_sprite)

    def init_new_fish_animate(self):
        self.current_fish_texture = arcade.load_spritesheet(self.current_sprite)
        texture_list = self.current_fish_texture.get_texture_grid(size=(1350, 756),
                                                                  columns=self.current_column,
                                                                  count=self.current_count)
        frames = []
        for tex in texture_list:
            frames.append(arcade.TextureKeyframe(tex))
        anim = arcade.TextureAnimation(frames)
        self.animate_fish = arcade.TextureAnimationSprite(animation=anim)
        self.animate_fish.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.current_fish_list.append(self.animate_fish)
        self.init_fish_animate = False

    def on_update(self, delta_time):
        self.indicator_ticks += 1
        self.sprite_list.update()
        self.physics_engine1.update()
        self.physics_engine2.update()
        self.sprite_list.update_animation()

        self.collision = arcade.check_for_collision(self.hook_sprite, self.indicator_sprite)
        if self.choose_fish is True:
            self.choose_new_fish()
        if self.current_minigame == "Fishing Minigame":
            if self.init_fish_animate is True:
                self.init_new_fish_animate()
            if self.collision is True:
                self.fishing_ticks += 1
                if self.progress_bar_bar_sprite.height < 1700:
                    self.progress_bar_bar_sprite.bottom = 235
                    self.progress_bar_bar_sprite.height += 3
                if self.progress_bar_bar_sprite.height >= 1700:
                    self.current_minigame = None
                    print("Mini Game Successful")
                if self.fishing_ticks % TICK_RATE == 0:
                    self.fishing_seconds += 1
                    print("Progress:", self.fishing_seconds)
            else:
                if self.progress_bar_bar_sprite.height > 0:
                    self.progress_bar_bar_sprite.bottom = 235
                    self.progress_bar_bar_sprite.height -= 3
                    if self.indicator_ticks % TICK_RATE == 0:
                        self.indicator_seconds += 1
                        print("Losing:", self.indicator_seconds)
                        if self.indicator_seconds == self.current_time_limit:
                            self.current_minigame = None
                            print("Mini Game Failed")
                    if self.progress_bar_bar_sprite.height == 0:
                        self.current_minigame = None
                        print('Mini Game Failed')
            self.indicator_change_direction = random.randint(0, 1)
            self.indicator_change_speed_ticks = random.randint(1, 2) * TICK_RATE
            self.indicator_change_direction_ticks = random.randint(1, 2) * TICK_RATE

            if self.indicator_ticks % self.indicator_change_speed_ticks == 0:
                self.indicator_sprite.change_y = random.randint(self.current_difficulty_low,
                                                                self.current_difficulty_high)

            if self.indicator_ticks % self.indicator_change_direction_ticks == 0:
                if self.indicator_change_direction == 1:
                    self.indicator_sprite.change_y = -self.indicator_sprite.change_y

            if self.mouse_hold:
                self.hook_sprite.change_y = HOOK_MOVEMENT_SPEED
            else:
                self.hook_sprite.change_y = -HOOK_MOVEMENT_SPEED

        if self.current_minigame == "Naval Bomb Minigame":
            # this is where naval bomb minigame will go
            if self.init_fish_animate is True:
                self.init_new_fish_animate()
            pass


    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = True

    def on_mouse_release(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = False


def main():
    """Main function"""
    window = FishingMiniGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
