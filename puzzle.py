import random
import curses
from abc import ABC, abstractmethod
from menu import Menu
import warnings

from bs4 import GuessedAtParserWarning
# wikipedia library has internal problem, supress warning
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

import wikipedia

wikipedia.set_lang("de")

def get_random_fantasy_article():
    wikipedia.set_lang("de")

    # List of page titles
    fantasy_pages = [
    "Burg Eltz", "Neuschwanstein", "Schloss Hohenzollern", "Schloss Dracula",
    "Gespenst", "Vampir", "Werwolf", "Hexe", "Schwarze Magie", "Mittelalter",
    "Alchemie", "Zauberei", "Drachen", "Schatten", "Magisches Schwert",
    "Zauberwald", "Ritter", "Gruselgeschichten", "Spukschloss",
    "Schwarzwald", "Ungeheuer", "Kobold", "Dunkelheit", "Kerker",
    "Nebel", "Raben", "Knochenschloss", "Feuerdrache", "Gargoyle",
    "Fluch", "Schwarze Katze", "Geisterstadt"
    ]

    correct_article = None

    while correct_article is None:
        try:
            # Randomly select a title and attempt to fetch the Wikipedia page
            correct_article = wikipedia.page(random.choice(fantasy_pages), auto_suggest=False)
        except (wikipedia.DisambiguationError, wikipedia.PageError, wikipedia.RedirectError):
            # Skip to the next title if any error occurs
            continue

    # Extract some characters
    article_length = len(correct_article.content)
    character_count = 350
    start_point = random.randint(0, article_length - 1 - character_count)
    snippet = correct_article.content[start_point:start_point + character_count]

    # Generate wrong options
    wrong_options = random.sample([p for p in fantasy_pages if p != correct_article.title], 3)

    return {
        'title': correct_article.title,
        'description': '...' + snippet + '...',
        'options': random.sample([correct_article.title] + wrong_options, k=4)
    }


class Puzzle(ABC):

    def __init__(self, std_screen):
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_GREEN) # win
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)  # win
        self._std_screen = std_screen
        self._user_choice = None

    @abstractmethod
    def play(self):
        pass


class SolveTitle(Puzzle):

    def __init__(self, std_screen):
        super().__init__(std_screen)
        self._category = "Fantasy"

    def play(self):
        self._std_screen.clear()
        screen_height, screen_width = self._std_screen.getmaxyx()
        # Get random article
        article = get_random_fantasy_article()

        # Display description
        instruction = "Erschließe dir den Wikipedia Artikel anhand des folgenden Textes:"
        hr = "##|===========================|##"
        self._std_screen.addstr(2, screen_width // 2 - len(instruction) // 2,
            instruction, curses.A_BOLD | curses.color_pair(5))
        self._std_screen.addstr(4, screen_width // 2 - len(hr) // 2,
                                hr, curses.A_BOLD | curses.color_pair(5))
        article_words = article['description'].split(" ")
        lines = []
        line = ""
        word_counter = 0
        for word in article_words:
            if word_counter == 15:
                word_counter = 0
                lines.append(line)
                line = ""
            line += word + " "
            word_counter += 1

        for i, line in enumerate(lines):
            self._std_screen.addstr(6 + i, screen_width // 2 - len(line) // 2, line)

        def set_choice(opt):
            self._user_choice = opt
        # Display options
        options_menu = Menu(self._std_screen, True)
        for i, option in enumerate(article['options']):
            options_menu.add_option(option, lambda opt=option: set_choice(opt))
            #self._std_screen.addstr(6 + i * 2, 2, f"{i}. {option}")
        options_menu.render()

        win_message = "*** Herzlichen Glückwunsch :) Du hast dieses Rätsel gelöst. Die Tür ist offen! Drücke eine beliebige Taste... ***"
        lose_message = f"Leider Falsch! Correct ist {article['title']}. Drücke eine beliebige Taste..."
        if self._user_choice == article['title']:
            self._std_screen.addstr(0, screen_width // 2 - len(win_message) // 2, win_message, curses.A_BOLD | curses.color_pair(6))
        else:
            self._std_screen.addstr(0, screen_width // 2 - len(lose_message) // 2, lose_message, curses.A_BOLD | curses.color_pair(7))

        self._std_screen.getch()
        return self._user_choice == article['title']
