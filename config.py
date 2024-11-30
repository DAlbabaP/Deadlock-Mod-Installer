import os
import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource """
    if getattr(sys, 'frozen', False):
        # If run through PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Directory paths
MEDIA_DIR = get_resource_path("media")
MODS_DIR = get_resource_path("mods")
NEW_LOCALIZATION_DIR = get_resource_path("new_localization")
ORIGINAL_LOCALIZATION_DIR = get_resource_path("original_localization")
GAMEINFO_PATH = get_resource_path("gameinfo.gi")

# Mod categories
MOD_CATEGORIES = [
    "Interface",
    "Game",
    "Sounds",
    "Post-processing",
    "Skins",
    "Other"
]

# Mod configuration
MODS = {
    "Skins": {
        "Abrams": [
            "Abrams Bull",
            "Abrams Dripbrams",
            "Abrams GUBAMI",
            "Abrams Hellboy",
            "Abrams Space Marine",
            "Abrams ZaHando"
        ],
        "Bebop": [
            "Bebop Delivery"
        ],
        "Dynamo": [
            "Dynamo Dunkamo"
        ],
        "GrayTalon": [
            "Just an owl drone",
            "Svoi Talon"
        ],
        "Haze": [
            "Haze VOIDWALKER",
            "Haze black+white",
            "Haze Checkmate",
            "Haze gold",
            "Haze Red",
            "Haze silver"
        ],
        "Infernus": [
            "Infernus Black+White",
            "Infernus Scoutfernus"
        ],
        "Ivy": [
            "Ivy Gardener",
            "Ivy Kali",
            "Ivy Low Poly"
        ],
        "Kelvin": [
            "Kelvin amazon employer"
        ],
        "Lady Geist": [
            "Lady Geist Date",
            "Lady Geist Fairy",
            "Lady Geist Green Geist",
            "Lady Geist Rainbow",
            "Lady Geist Remgeist",
            "Lady Geist Short"
        ],
        "Lash": [
            "Lash Belash",
            "Lash Lashton Hale",
            "Lash Yakuza"
        ],
        "McGinnis": [
            "McGinnis Engineer",
            "McGinnis Paw",
            "McGinnis Red"
        ],
        "Mirage": [
            "Mirage_s ult sound"
        ],
        "Mo and Krill": [
            "Mo and Krill Krill and Mo",
            "Mo and Krill Mo and Mo",
            "Mo and Krill Shark"
        ],
        "Paradox": [
            "Paradox Bikinidox",
            "Paradox Bunnydox",
            "Paradox Ivydox",
            "Paradox Light Pyradox",
            "Paradox Pyradox"
        ],
        "Pocket": [
            "Pocket Holiday over",
            "Pocket Loona"
        ],
        "Seven": [
            "Seven Halloween",
            "Seven Low Poly",
            "Seven NeonPrime",
            "Seven gigavatt"
        ],
        "Shiv": [
            "Shiv Bald",
            "Shiv Long hair",
            "Shiv Neon Prime",
            "Shiv V"
        ],
        "Vindicta": [
            "Vindicta Bikinidicta Full mod",
            "Vindicta Bikinidicta No 2 skill music",
            "Vindicta Bikinidicta No sounds",
            "Vindicta Black+White",
            "Vindicta Sandals",
            "Vindicta Shoes"
        ],
        "Viper": [
            "Viper snake"
        ],
        "Viscous": [
            "Viscous Cumcous",
            "Viscous Glorp",
            "Viscous Halloween",
            "Viscous Pink",
            "Viscous Viscoast"
        ],
        "Wraith": [
            "Wraith Black+White",
            "Wraith Without cloak"
        ],
        "Yamato": [
            "Yamato 2B",
            "Yamato 2B without drawn sword",
            "Yamato 2B without drawn sword and skirt",
            "Yamato 2B without skirt",
            "Yamato Mytrato",
            "Yamato NeonPrime",
            "Yamato Vergil"
        ]
    },
    "Game": [
        "Color-blind friendly",
        "Fairy bottle",
        "Haze Ball",
        "Interloper",
        "NeonPrime Shop",
        "Turrets from Portal"
    ],
    "Interface": [
        "Square Top Bar"
    ],
    "Post-processing": [
        "lamarrite_s post processing"
    ],
    "Sounds": [
        "Banana knockdown",
        "Crazy Wrecker",
        "Dinamo_s ult sound",
        "Ebaniy rot etogo kazino",
        "Haze_s dagger",
        "Heavy attack alert",
        "Jaws and Krill",
        "Mirage_s ult sound",
        "Sounds of death",
        "awp sound ult"
    ],
    "Other": []
}

# Interface settings
WINDOW_SIZE = "800x600"
WINDOW_TITLE = "Deadlock Mod Installer"

# Color settings
COLORS = {
    'bg': '#1e1e1e',       # Dark background
    'fg': '#ffffff',       # White text
    'accent': '#007acc',   # Blue accent
    'hover': '#2d2d2d',    # Hover color
    'select': '#264f78',   # Selection color
    'light': '#3c3c3c'     # Light background shade
}
