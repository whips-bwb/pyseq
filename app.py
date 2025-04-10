from functions.launch_app import launch_app
from functions.display import *

if __name__ == "__main__":
    # very beautiful ascii intro 
    title = "PYTHON MIDI SEQUENCER by whips@musinux.com"
    border = "=" * (len(title)+10)
    ascii_intro = f"\n{border_col}{border}{RESET}\n\n     {title_col}{title}{RESET}\n\n{border_col}{border}{RESET}\n"
    print(ascii_intro)
    # delegate to separated functions
    launch_app()