from menu import Menu


class Room:

    def __init__(self, std_screen, ascii_sprite, description, puzzle, handle_next_room):
        self._std_screen = std_screen
        self._ascii_sprite = ascii_sprite
        self._description = description
        self._chapter_menu = Menu(self._std_screen, False, 2)
        self._chapter_menu.add_option("Solve Puzzle", None)
        self._chapter_menu.add_option("Exit Game", exit)
        self._chapter_menu.add_option("Next Room", handle_next_room)
        self._is_solved = False


    def run(self):
        self._std_screen.clear()
        self._std_screen.addstr(str(self._ascii_sprite))
        for i, line in enumerate(self._description.lines):
            self._std_screen.addstr(i, self._ascii_sprite.width, line)
        self._chapter_menu.render(self._ascii_sprite.height)
        self._std_screen.getch()
        self._std_screen.refresh()

