import arcade
import subprocess



class EndView(arcade.View):
    key_pressed = False

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.MIDNIGHT_BLUE)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Game Over!",
                         self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE,
                         font_size=50,
                         font_name="Kenney Rocket", anchor_x="center")                 
        arcade.draw_text("Your score was:", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, font_name="Kenney Rocket", anchor_x="center")
        
        arcade.draw_text("To play again, press UP", self.window.width / 2, self.window.height / 2 - 120,
                         arcade.color.WHITE, font_size=15, font_name="Kenney Rocket", anchor_x="center")


    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            arcade.close_window()
            command = "python3 main.py"  
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                print("Command Output:")
                print(result.stdout)
                return result.returncode
            except subprocess.CalledProcessError as e:
                print("Command Failed with Error:")
                print(e.stderr)
                return e.returncode
            