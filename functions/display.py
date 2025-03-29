# Hide cursor function
def hide_cursor():
    print("\033[?25l", end='')

# Show cursor function
def show_cursor():
    print("\033[?25h", end='')

YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[36m"
WHITE = "\033[37m"
BGgreen = "\033[42m"
BGred = "\033[41m"
RESET = "\033[0m"