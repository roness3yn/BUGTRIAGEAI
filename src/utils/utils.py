# src/code/utils.py
import os

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def clear_console():
    """Clears the terminal screen regardless of the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def color_text(text, color_code):
    """Wraps text in a color code and ensures it resets at the end."""
    return f"{color_code}{text}{RESET}"