import arcade
import subprocess



class EndView(arcade.View):
    def __init__(self, player_sprite):
        super().__init__()

        # Store the player sprite as an instance variable
        self.player_sprite = player_sprite

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.MIDNIGHT_BLUE)
        #sound from https://pixabay.com/music/modern-classical-gymnopedie-1-erik-satie-176573/
        sound = arcade.load_sound("static/sounds/Satie.wav")
        arcade.play_sound(sound, looping=True)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Game Over!",
                         self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE,
                         font_size=50,
                         font_name="Kenney Rocket", anchor_x="center")                 
        arcade.draw_text("You ended with " + str(self.player_sprite.gold) + " Gold", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, font_name="Kenney Rocket", anchor_x="center")
        
        arcade.draw_text("Your level was: " + str(self.player_sprite.level), self.window.width / 2, self.window.height / 2 - 120,
                         arcade.color.WHITE, font_size=15, font_name="Kenney Rocket", anchor_x="center")


    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            arcade.close_window()
            
            
