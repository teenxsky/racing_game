from .Menu import *
import webbrowser


class Authors(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.authors_bg = Picture("Resources/Images/Backgrounds/window.png", 0.5)

        button_sound = pg.mixer.Sound("Resources/Audio/button_sound.mp3")
        self.authors_close_button = Button("Resources/Images/Buttons/close_button_off.png",
                                           "Resources/Images/Buttons/close_button_on.png", button_sound, 0.15)

        self.text_authors = Text("AUTHORS", 45)
        self.authors = [Text("ROMAN SOKOLOVSKII", 17, color=BLUE),
                        Text("RUSLAN KUTORGIN", 17, color=BLUE),
                        Text("PAVEL SHAHMATOV", 17, color=BLUE)]

        self.girl = Sheet("Resources/Images/Hud/Sheets/girl.png", scale=2.8)

        self.github_icon = Picture("Resources/Images/github_icon.png", 0.013)

        self.team_name = Text("00TEAM", 12)
        self.fefu_icon = Picture("Resources/Images/fefu_icon.png", 0.5)

    def display_menu(self):
        self.authors_bg.draw(self.game.screen, (640, 360))
        self.text_authors.draw(self.game.screen, (640, 225))

        distance = 0
        for text in self.authors:
            text.draw(self.game.screen, (640, 275 + distance))
            distance += 30

        self.team_name.draw(self.game.screen, (640, 480))
        self.fefu_icon.draw(self.game.screen, (660, 445))

        if self.github_icon.draw(self.game.screen, (620, 445)) and self.game.keys["MOUSE DOWN"]:
            webbrowser.open("https://github.com/teenxsky/racing_game", new=0, autoraise=True)

        self.girl.draw(self.game.screen, (825, 375), speed=200)
        if self.authors_close_button.draw(self.game.screen, (865, 225)) and self.game.keys["MOUSE DOWN"]:
            self.game.menu_state = "MENU"
