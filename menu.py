import arcade
import arcade.gui

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Menu", resizable=True)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.v_box = arcade.gui.UIBoxLayout()

        restart_button = arcade.gui.UIFlatButton(text="Restart Game", width=200)
        self.v_box.add(restart_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit Game", width=200)
        self.v_box.add(quit_button)

        restart_button.on_click = self.on_click_restart
        quit_button.on_click = self.on_click_quit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_restart(self, _event: arcade.gui.UIOnClickEvent):
        # TODO restart the game
        pass

    def on_click_quit(self, _event: arcade.gui.UIOnClickEvent):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()

if __name__ == "__main__":
    window = MyWindow()
    arcade.run()
