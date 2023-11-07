import arcade
from gameview import GameView


# import tile
# from classes.actor import Player

class StartView(arcade.View):
    key_pressed = False

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.MIDNIGHT_BLUE)

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

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:  
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        