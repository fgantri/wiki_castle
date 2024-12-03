import os.path

from castle import Castle
from menu import Menu
from room import Room
from sprite import AsciiSprite, Text


class Game:

    def __init__(self, std_screen):
        self._std_screen = std_screen
        self._current_room_idx = 0
        self._rooms = [
            Room(self._std_screen,
            AsciiSprite(os.path.join(os.getcwd(), "assets", "ascii_sprites", "rooms", "room1.txt")),
            Text(os.path.join(os.getcwd(), "assets", "chapter_texts", "chapter1.txt")),
            puzzle=None, handle_next_room=self.handle_next_room),
            Room(self._std_screen,
            AsciiSprite(os.path.join(os.getcwd(), "assets", "ascii_sprites", "rooms", "room2.txt")),
            Text(os.path.join(os.getcwd(), "assets", "chapter_texts", "chapter1.txt")),
            puzzle=None, handle_next_room=self.handle_next_room)
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
        self._std_screen.clear()
        self._std_screen.addstr(0, 0, "Credit Screen")
        self._std_screen.refresh()
        self._std_screen.getch()
        exit()