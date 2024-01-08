from .Menu import *
# import cv2
# import numpy


class LevelsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.levels_gui_main = Picture("Resources/Images/Backgrounds/levels_gui.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.levels_gui_sub = Picture("Resources/Images/Backgrounds/window_trans.png", (615, 355))
        self.levels_text = Text("LEVELS", 40)

        self.levels_close_button = Button("Resources/Images/Buttons/close_button_off.png",
                                          "Resources/Images/Buttons/close_button_on.png", button_sound, 0.15)
        self.levels_start_button = Button("Resources/Images/Buttons/start_button_off.png",
                                          "Resources/Images/Buttons/start_button_on.png", button_sound, 0.2)
        self.levels_back_button = Button("Resources/Images/Buttons/back_button_off.png",
                                         "Resources/Images/Buttons/back_button_on.png", button_sound, 0.15)
        self.levels_forward_button = Button("Resources/Images/Buttons/forward_button_off.png",
                                            "Resources/Images/Buttons/forward_button_on.png", button_sound, 0.15)
        self.levels_statistics_button = Button("Resources/Images/Buttons/statistic_button_off.png",
                                               "Resources/Images/Buttons/statistic_button_on.png", button_sound, 0.08)

        self.levels_bg, self.levels_bg_speed = load_bg("levels_bg")
        self.bg_sound = load_bg_sound("levels_bg")

        self.sub_state = "LEVELS"
        self.block = False

    def display_menu(self):

        index = 0
        for level_info in settings.levels:
            if level_info["score"] <= settings.player_stats["score"]:
                settings.levels[index]["access"] = True
            else:
                settings.levels[index]["access"] = False
            index += 1

        levels = []
        index = 0
        for file in sorted(os.listdir("Resources/Images/Backgrounds/Levels/")):
            if not file.startswith("."):
                pictures = [file for file in sorted(os.listdir("Resources/Images/Backgrounds/Levels/" + file + "/")) if
                            not file.startswith(".")]
                level = Background("Resources/Images/Backgrounds/Levels/" + file + "/" + pictures[0], (540, 330))

                # cv2_img = cv2.imread("Resources/Images/Backgrounds/Levels/" + file + "/" + pictures[0])
                # average_color_row = numpy.average(cv2_img, axis=0)
                # average_color = list(int(i) for i in numpy.average(average_color_row, axis=0))
                # settings.levels[index]["description"]["bar_color"] = average_color + [200]

                level_pictures = []
                pictures = pictures[1:]
                for picture in pictures:
                    level_picture = Picture("Resources/Images/Backgrounds/Levels/" + file + "/" + picture, (540, 330))
                    level_pictures.append(level_picture)
                level.set_bgs(level_pictures, (60, 5, 20, 30, 5), 10)
                levels.append({"level": level, "description": Text(settings.levels[index]["description"]["text"], 15),
                               "bar_color": settings.levels[index]["description"]["bar_color"], "index": index})
                index += 1

        curr_lvl_x = 640
        while self.game.running and not self.game.playing and self.game.menu_state == "LEVELS":
            self.check_events()

            self.levels_bg.draw(self.game.screen, self.levels_bg_speed)

            if not self.bg_sound.num_channels:
                self.bg_sound.play(loops=-1, fade_ms=500)

            self.levels_gui_main.draw(self.game.screen, (640, 360))
            self.levels_text.draw(self.game.screen, (640, 40))

            sub_text_bars = []

            distance = 0
            for level in levels:
                bar = pg.Surface((540, 330)).convert_alpha()
                bar_rect = bar.get_rect()
                bar_rect.center = (curr_lvl_x + distance, 360)
                level["level"].random_scroll(bar, 0.2)
                self.game.screen.blit(bar, bar_rect)

                if settings.levels[level["index"]]["access"] and bar_rect.centerx == 640:
                    if self.levels_start_button.draw(self.game.screen, (640, 585), self.block) and self.game.keys["MOUSE DOWN"]:
                        self.game.playing = True
                        self.game.curr_level = levels.index(level)
                        self.game.menu_state = "LEVELS"
                    if self.levels_statistics_button.draw(self.game.screen, (885, 470), self.block) and self.game.keys["MOUSE DOWN"]:
                        self.sub_state = "LEVEL_STATISTIC"
                elif not settings.levels[level["index"]]["access"]:
                    block = pg.surface.Surface(bar.get_size(), pg.SRCALPHA).convert_alpha()
                    block.fill((0, 0, 0, 200))
                    curr_score = Text(
                        str(settings.player_stats["score"]) + "/" + str(settings.levels[level["index"]]["score"]), 40)
                    curr_score.draw(block, (block.get_width() // 2, block.get_height() // 2))
                    self.game.screen.blit(block, bar_rect)

                self.levels_gui_sub.draw(self.game.screen, (curr_lvl_x + distance, 360),
                                         surface_topleft=bar_rect.topleft)

                sub_text_bars.append(level["description"].get_text_bar(bar_rect, bar_color=level["bar_color"]))

                difficulty_text = Text(f'DIFFICULTY: {settings.levels[level["index"]]["difficulty"]}', 30)
                difficulty_text.draw(self.game.screen, (curr_lvl_x + distance, 690))

                distance += 700
            distance -= 700

            if curr_lvl_x + 700 <= 640:
                if (self.levels_back_button.draw(self.game.screen, (300, 360), self.block) and self.game.keys["MOUSE DOWN"]) or (
                        self.game.keys["MOVE LEFT"] and not self.block):
                    curr_lvl_x += 700

            if curr_lvl_x + distance - 700 >= 640:
                if (self.levels_forward_button.draw(self.game.screen, (1000, 360), self.block) and self.game.keys[
                    "MOUSE DOWN"]) or (
                        self.game.keys["MOVE RIGHT"] and not self.block):
                    curr_lvl_x -= 700

            if self.levels_close_button.draw(self.game.screen, (40, 40), self.block) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "MENU"

            for sub_text_bar in sub_text_bars:
                if sub_text_bar:
                    self.game.screen.blit(*sub_text_bar)

            self.check_input()
            self.game.blit_screen()

        pg.time.delay(500)
        self.bg_sound.stop(fadeout=500)

    def __display_level_statistic(self):
        # bar = pg.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA).convert_alpha()
        # bar.fill((0, 0, 0, 150))

        if self.game.keys["BACK"]:
            self.sub_state = "LEVELS"

    def check_input(self):
        self.block = (self.sub_state == "LEVEL_STATISTIC")

        if self.sub_state == "LEVEL_STATISTIC":
            self.__display_level_statistic()
