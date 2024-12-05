from menu import Menu
import sys

class Room:

    def __init__(self, std_screen, ascii_sprite, description, puzzle, handle_next_room):
        self._std_screen = std_screen
        self._ascii_sprite = ascii_sprite
        self._description = description
        self._puzzle = puzzle
        self._chapter_menu = Menu(self._std_screen, False)
        self._chapter_menu.add_option("Wiki Rätsel lösen", self._call_puzzle)
        self._chapter_menu.add_option("Spiel beenden", sys.exit)
        self._handle_next_room = handle_next_room
        self._is_solved = False

    def _call_puzzle(self):
        if self._puzzle is None:
            return
        self._is_solved = self._puzzle.play()
        if self._is_solved:
            self._chapter_menu = Menu(self._std_screen, False, 0)
            self._chapter_menu.add_option("Nächsten Raum betreten", self._handle_next_room)
            self._chapter_menu.add_option("Spiel beenden", sys.exit)
        else:
            self._chapter_menu = Menu(self._std_screen, False)
            self._chapter_menu.add_option("Wiki Rätsel lösen", self._call_puzzle)
            self._chapter_menu.add_option("Spiel beenden", sys.exit)
        self.run()

    def run(self):
        self._std_screen.clear()
        self._std_screen.addstr(str(self._ascii_sprite))
        for i, line in enumerate(self._description.lines):
            self._std_screen.addstr(i, self._ascii_sprite.width + 5, line)
        self._chapter_menu.render(self._ascii_sprite.height)
        self._std_screen.getch()
        self._std_screen.refresh()