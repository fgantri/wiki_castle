import curses

from game import Game
from menu import MainMenu, Menu


def main(std_screen):
    curses.curs_set(0)
    game = Game(std_screen)
    main_menu = MainMenu(std_screen)
    main_menu.add_option("Spiel Starten", game.run)
    main_menu.add_option("Spiel beenden", exit)
    main_menu.render()


curses.wrapper(main)