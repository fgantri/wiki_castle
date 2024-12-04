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
            correct_title = random.choice(fantasy_pages)
            correct_article = wikipedia.page(correct_title, auto_suggest=False)
        except (wikipedia.DisambiguationError, wikipedia.PageError, wikipedia.RedirectError):
            # Skip to the next title if any error occurs
            continue

    # Extract some characters
    article_length = len(correct_article.content)
    character_count = 250
    start_point = random.randint(0, article_length - 1 - character_count)
    snippet = correct_article.content[start_point:start_point + character_count]

    # Generate wrong options
    wrong_options = random.sample([p for p in fantasy_pages if p != correct_title], 3)

    return {
        'title': correct_title,
        'description': '...' + snippet + '...',
        'options': random.sample([correct_title] + wrong_options, k=4)
    }


class Puzzle(ABC):

    def __init__(self, std_screen):
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self._std_screen = std_screen

    @abstractmethod
    def play(self):
        pass


class SolveTitle(Puzzle):

    def __init__(self, std_screen):
        super().__init__(std_screen)
        self._category = "Fantasy"

    def play(self):
        self._std_screen.clear()

        # Get random article
        article = get_random_fantasy_article()

        # Display description
        self._std_screen.addstr(2, 2,
            "Erschließe dir den Wikipedia Artikel anhand des folgenden Textes:", curses.A_BOLD | curses.color_pair(5))
        self._std_screen.addstr(4, 2, article['description'])

        user_choice = []
        # Display options
        options_menu = Menu(self._std_screen)
        for i, option in enumerate(article['options'], start=1):
            options_menu.add_option(option, lambda: user_choice.append(option))
            #self._std_screen.addstr(6 + i * 2, 2, f"{i}. {option}")
        options_menu.add_option(f"{article['title']}", lambda: user_choice.append(article['title']))
        options_menu.render(8)

        if user_choice[0] == article['title']:
            return True
        else:
            return False