import curses
import os
import threading
import sys
from playsound import playsound

from game import Game
from menu import MainMenu, Menu


stop_music = threading.Event()

def loop_sound():
    while not stop_music.is_set():
        playsound(os.path.join(os.getcwd(), "assets", "sound_effects", "background_music_8bit.mp3"), block=True)

loop_thread = threading.Thread(target=loop_sound, name='backgroundMusicThread', daemon=True)

def main(std_screen):
    loop_thread.start()
    curses.curs_set(0)
    game = Game(std_screen)
    main_menu = MainMenu(std_screen)
    main_menu.add_option("Spiel Starten", game.run)
    main_menu.add_option("Spiel beenden", sys.exit)
    main_menu.render()


curses.wrapper(main)