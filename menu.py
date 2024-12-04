import curses
import os.path
import threading

from playsound import playsound
from sprite import AsciiSprite

KEY_PRESS_SFX = os.path.join(os.getcwd(), "assets", "sound_effects", "menu_mov_sfx.wav")
SELECT_PRESS_SFX = os.path.join(os.getcwd(), "assets", "sound_effects", "select_sfx.wav")

stop_music = threading.Event()

def loopSound():
    while not stop_music.is_set():
        playsound(os.path.join(os.getcwd(), "assets", "sound_effects", "background_music_8bit.mp3"), block=True)

loopThread = threading.Thread(target=loopSound, name='backgroundMusicThread')
loopThread.start()


class Menu:

    def __init__(self, std_screen, is_centered = False, highlight=None):
        self._std_screen = std_screen
        self._options = []
        self._current_option_index = 0
        self._is_centered = is_centered
        self._highlight = highlight

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN) # select

        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE) # select highlighted

    def add_option(self, label, callback):
        self._options.append((label, callback))

    def render(self, margin_top = 0):

        while True:
            self._print_menu(self._current_option_index, margin_top)
            key = self._std_screen.getch()
            if key == curses.KEY_UP:
                playsound(KEY_PRESS_SFX)
                self._current_option_index -= 1
                if self._current_option_index == -1:
                    self._current_option_index = len(self._options)-1
            elif key == curses.KEY_DOWN:
                playsound(KEY_PRESS_SFX)
                self._current_option_index += 1
                if self._current_option_index == len(self._options):
                    self._current_option_index = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:
                playsound(SELECT_PRESS_SFX)
                return self._options[self._current_option_index][1]()
            self._std_screen.refresh()

    def _print_menu(self, selected_row_idx, margin_top = 0):
        screen_height, screen_width = self._std_screen.getmaxyx()

        for idx, option in enumerate(self._options):
            label, callback = option
            # position menu
            if self._is_centered:
                x = screen_width // 2 - len(label) // 2
                y = screen_height // 2 - len(self._options) + idx
            else:
                x = 0
                y = margin_top + len(self._options) + idx
            if idx == selected_row_idx:
                color = 4 if idx == self._highlight else 2
                self._std_screen.addstr(y, x, f"> {label} ", curses.color_pair(color) | curses.A_BOLD)
            else:
                color = 3 if idx == self._highlight else 1
                self._std_screen.addstr(y, x, f"  {label} ", curses.color_pair(color) | curses.A_BOLD)


class MainMenu(Menu):

    def __init__(self, std_screen):
        super().__init__(std_screen, True)

    def render(self, margin_top = 0, highlight=False):
        screen_height, screen_width = self._std_screen.getmaxyx()
        title = AsciiSprite(os.path.join(os.getcwd(), "assets", "ascii_sprites", "ui", "title.txt"))
        castle = AsciiSprite(os.path.join(os.getcwd(), "assets", "ascii_sprites", "castle.txt"))
        title.add_left_margin(screen_width // 2 - title.width // 2)
        castle.add_left_margin(screen_width // 2 - castle.width // 2)
        while True:
            self._std_screen.clear()
            self._std_screen.addstr(0, 0, str(title))
            self._std_screen.addstr(
                screen_height - castle.height, 0, str(castle))
            self._print_menu(self._current_option_index)
            key = self._std_screen.getch()
            if key == curses.KEY_UP:
                playsound(KEY_PRESS_SFX)
                self._current_option_index -= 1
                if self._current_option_index == -1:
                    self._current_option_index = len(self._options)-1
            elif key == curses.KEY_DOWN:
                playsound(KEY_PRESS_SFX)
                self._current_option_index += 1
                if self._current_option_index == len(self._options):
                    self._current_option_index = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:
                playsound(SELECT_PRESS_SFX)
                return self._options[self._current_option_index][1]()
            self._std_screen.refresh()