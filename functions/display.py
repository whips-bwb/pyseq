# Hide cursor function
def hide_cursor():
    print("\033[?25l", end='')

# Show cursor function
def show_cursor():
    print("\033[?25h", end='')

YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
PURPLE = "\033[35m"
BLUE = "\033[36m"
WHITE = "\033[37m"
BGgreen = "\033[42m"
BGred = "\033[41m"
BGyellow = "\033[43m"
BGblue = "\033[46m"
BoldRed = "\033[1;91m"
BoldGreen = "\033[1;92m"
BoldYellow = "\033[1;93m"
BoldBlue = "\033[1;94m"
BoldPurple = "\033[1;95m"
border_col = "\033[44m"
title_col =  "\033[1;100m"
RESET = "\033[0m"