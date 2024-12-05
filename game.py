import curses
import os.path

from puzzle import SolveTitle
from room import Room
from sprite import AsciiSprite, Text

ROOMS_IMG_PATH = os.path.join(os.getcwd(), "assets", "ascii_sprites", "rooms")
TEXTS_PATH = os.path.join(os.getcwd(), "assets", "chapter_texts")

class Game:

    def __init__(self, std_screen):
        self._std_screen = std_screen
        self._current_room_idx = 0
        self._rooms = [
            Room(self._std_screen,
            AsciiSprite(os.path.join(ROOMS_IMG_PATH, "room1.txt")),
            Text(os.path.join(TEXTS_PATH, "chapter1.txt")),
            puzzle=SolveTitle(std_screen), handle_next_room=self.handle_next_room),
            Room(self._std_screen,
            AsciiSprite(os.path.join(ROOMS_IMG_PATH, "room2.txt")),
            Text(os.path.join(TEXTS_PATH, "chapter2.txt")),
            puzzle=SolveTitle(std_screen), handle_next_room=self.handle_next_room),
            Room(self._std_screen,
            AsciiSprite(os.path.join(ROOMS_IMG_PATH, "room3.txt")),
            Text(os.path.join(TEXTS_PATH, "chapter3.txt")),
            puzzle=SolveTitle(std_screen), handle_next_room=self.handle_next_room),
            Room(self._std_screen,
            AsciiSprite(os.path.join(ROOMS_IMG_PATH, "room4.txt")),
            Text(os.path.join(TEXTS_PATH, "chapter4.txt")),
            puzzle=SolveTitle(std_screen), handle_next_room=self.handle_next_room),
            Room(self._std_screen,
            AsciiSprite(os.path.join(ROOMS_IMG_PATH, "room5.txt")),
             Text(os.path.join(TEXTS_PATH, "chapter5.txt")),
             puzzle=SolveTitle(std_screen), handle_next_room=self.handle_next_room)
        ]

    def handle_next_room(self):
        next_room_idx = self._current_room_idx + 1

        if next_room_idx == len(self._rooms):
            self.credit_screen()
        else:
            self._current_room_idx += 1
            self.run()

    def run(self):
        self._std_screen.clear()
        self._rooms[self._current_room_idx].run()

    def credit_screen(self):
        dev_list = [
            "Fouad - Game Engine Developer",
            "Joshua - Story Writer, Puzzle Dev",
            "Kirill - Audio Engineer",
            "Feras - Puzzle Dev"
        ]
        self._std_screen.clear()

        screen_height, screen_width = self._std_screen.getmaxyx()
        congrats = "Glückwunsch du hast es aus dem Schloss geschafft!"
        title = "CREDIT SCREEN RAUM"
        self._std_screen.addstr(6, screen_width // 2 - len(congrats) // 2, congrats, curses.color_pair(6) | curses.A_BOLD)
        self._std_screen.addstr(8, screen_width // 2 - len(title) // 2, title, curses.color_pair(1) | curses.A_BOLD)
        for i, dev in enumerate(dev_list):
            x = screen_width // 2 - len(dev) // 2
            y = screen_height // 2 - len(dev_list) + i * 2
            self._std_screen.addstr(y, x, dev)
        self._std_screen.refresh()
        self._std_screen.getch()
        exit()