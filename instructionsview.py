import arcade
from gameview import GameView


class StartView(arcade.View):
    key_pressed = False
    sound = None
    sp = None

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.MIDNIGHT_BLUE)
        #sound from freesound.org https://freesound.org/people/holizna/sounds/629154/
        self.sound = arcade.load_sound("static/sounds/intro.wav")
        self.sp = arcade.play_sound(self.sound, looping=True)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Welcome to Rogue",
                         self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE,
                         font_size=50,
                         font_name="Kenney Rocket", anchor_x="center")
        arcade.draw_text("press up to begin", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, font_name="Kenney Rocket", anchor_x="center")

        arcade.draw_text("Noah Schonhorn, Michael Piscione, Max Ivry, Evan Satterfield ", (self.window.width / 2) - 570,
                         self.window.height / 2 - 310,
                         arcade.color.WHITE, font_size=14, font_name="Arial")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.sound:
                arcade.stop_sound(self.sp)
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
