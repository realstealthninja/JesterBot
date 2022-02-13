## environ

from asyncpraw import Reddit
from os import environ
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = environ["BOT_TOKEN"]
WEATHER_KEY = environ["WEATHER_KEY"]
COORDS_KEY = environ["COORDS_KEY"]
CHATBOT_KEY = environ["CHATBOT_KEY"]
RAPID_API_KEY = environ["RAPID_API_KEY"]

CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
USERNAME = environ["REDDIT_USERNAME"]
PASSWORD = environ["PASSWORD"]
USER_AGENT = environ["USER_AGENT"]


## reddit 

REDDIT = Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT,
    username = USERNAME,
    password = PASSWORD
)


## emojis

THUMBS_UP = "👍"
THUMBS_DOWN = "👎"
CONFETTI = "🎊"
CLOSED_LOCK = "🔐"
BOOM = "💥"
HANDSHAKE = "🤝"


## custom emojis

LOCATION_EMOJIS = {
    "fastbackwards": "<:fast_forward_left:870781340692402226>",
    "backwards": "<:left_arrow:870781340990197860>",
    "close": "<:Cross:863313854069997578>",
    "forwards": "<:right_arrow:870781340314898473>",
    "fastforwards": "<:fast_forward_right:870781340839202837>",
}
COG_EMOJIS = {
    "JesterInfo": 863075610048987166,
    "Feedback": 863075610851147777,
    "Music": 863075611320647719,
    "Snipe": 863075611269791794,
    "Fun": 863075609781075968,
    "Mod": 863075610784301068,
    "Games": 863075611329167380,
    "Utils": 863075611161788478,
    "Images": 863075611277656124,
    "Economy": 863075610913800233,
    "Misc": 863075610979729409,
    "Levels": 863075611182628895,
    "Config": 863075611169259550,
    "Love": 863075611374125056,
    "JesterJokes": 873327129016811528,
    "Countries": 872473402638762025,
    "ChatBot": 872473402693259324,
    "DiscordTogether": 872473402840076288,
    "UrbanDictionary": 924074967673503796,
    "Random": 924074967405051965,
    "Trivia": 924152372001910834,
    "Crime": 924411072729985046,
    "Docs": 925222917946605629,
}

CLOSE = "<:Cross:863313854069997578>"
HOME = "<:Arrow:863313854040506379>"
LINK = "<:links:870781340700782612>"
CATEGORIES = "<:menus:870781340746932225>"
TRASHCAN = "<:trashbin:873564727006089287>"
LOADING = "<a:loading_grey:942386360877219881>"

_J = "<:J_:863313855286607932>"
_E = "<:E_:863313854150606848>"
_S = "<:S:863313855061164062>"
_T = "<:T:863313855399329812>"
_R = "<:R_:863313855119360022>"


## game

CARD_SUITS = {
    "hearts": "♥️",
    "diamonds": "♦️",
    "clubs": "♣️",
    "spades": "♠️",
}
BLACKJACK_WELCOME = """```yaml
Welcome to the blackjack game. 
==============================

It is recommended that you research the rules to familiarize yourself how the game is played.```
"""
BLACKJACK_HOW_TO = """```yaml
How to play blackjack
=====================x

Start
-----
• When you play you will get a hand with 2 cards.
• If you get an ace you can choose it's value to be 1 or 11. 
• All face cards are equal to 10 this includes; King, Queen and Jack.

Game over
---------
• The player who's card's overall score is closer to 21 wins.
• The game ends when you stand.```
"""
HANGMAN = [
    "",
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
    """

  +---+   _   _  _____   ____   ___  _____  ____
  |   |  | | | || ____| |  _ \ |_ _|| ____||  _ \
  O   |  | |_| ||  _|   | | | | | | |  _|  | | | |
 /|\  |  |  _  || |___  | |_| | | | | |___ | |_| |
 / \  |  |_| |_||_____| |____/ |___||_____||____/
      |
=========""",
][::-1]


## utils

TEXT_TO_MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ",": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
    ":": "---...",
    "'": ".----.",
    "’": ".----.",
    '"': ".-..-.",
    " ": ".......",
    "!": "-.-.--",
    "@": ".--.-.",
    "$": "...-..-",
    "&": ".-...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "_": "..--.-",
}

MORSE_TO_TEXT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
    "--..--": ",",
    ".-.-.-": ".",
    "..--..": "?",
    "-..-.": "/",
    "-....-": "-",
    "-.--.": "(",
    "-.--.-": ")",
    "---...": ":",
    ".----.": "'",
    ".-..-.": '"',
    ".......": " ",
    "-.-.--": "!",
    ".--.-.": "@",
    "...-..-": "$",
    ".-...": "&",
    "-.-.-.": ";",
    "-...-": "=",
    ".-.-.": "+",
    "..--.-": "_",
}
ASCII_DESCRIPTION = """ASCII was developed from telegraph code. Work on the ASCII standard began in May 1961. The first edition of the standard was published in 1963. Compared to earlier telegraph codes, the proposed Bell code and ASCII were both ordered for more convenient sorting (i.e., alphabetization) of lists.

The use of ASCII format for Network Interchange was described in 1969. That document was formally elevated to an Internet Standard in 2015.

Originally based on the English alphabet, ASCII encodes 128 specified characters into seven-bit integers as shown by the ASCII chart above. Ninety-five of the encoded characters are printable: these include the digits 0 to 9, lowercase letters a to z, uppercase letters A to Z, and punctuation symbols. 

For example, lowercase i would be represented in the ASCII encoding by binary 1101001 = hexadecimal 69 (i is the ninth letter) = decimal 105.
To get the ascii table type j.ascii

Source: [Website](https://en.wikipedia.org/wiki/ASCII)
    """


## docs

ZEN_OF_PYTHON = """\
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""
