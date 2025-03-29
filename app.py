from functions.launch_app import launch_app

if __name__ == "__main__":
    # very beautiful ascii intro 
    title = "PYTHON MIDI SEQUENCER by whips@musinux.com"
    border = "=" * (len(title)+10)
    ascii_intro = f"\n\033[44m{border}\033[00m\n    \033[35m{title}\033[00m\n\033[44m{border}\033[00m\n"
    print(ascii_intro)
    # delegate to separated functions
    launch_app()
