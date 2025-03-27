import subprocess
import time
import sys
import mido
import scoring.settings
import scoring.sequence
from functions.quick_import_patterns import quick_import_patterns  
from functions.playPattern import play_pattern
from functions.import_sequence import import_sequence
from functions.display import *


# Main function to load pattern, sequence, and play
def main():
    try:
        #launch automatically the FluidSynth instance locally
        print(f"\n{YELLOW}launching FluidSynth instance !{RESET}\n")
        synth_process = subprocess.Popen(
            ["fluidsynth", "-a", "alsa", "-f ", "scoring/FSconfig.txt" , "-m", "alsa_seq",  "/usr/share/sounds/sf2/FluidR3_GM.sf2"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        # wait a little to ensure midi channel is up ... (reduce if needed)
        time.sleep(2)
        print(f"{mido.open_output(mido.get_output_names()[2])}")
        # Default values
        default_signature = "4/4"
        default_tempo = 120
        # Prompt user with default values in parentheses
        time_signature_input = input(f"{YELLOW}SIGNATURE ? {RESET}(2/4 to 19/8) [default: {default_signature}] : ") or default_signature
        tempo_input = input(f"{YELLOW}TEMPO / BPM ? {RESET}[default: {default_tempo}] : ")
        # If user didn't enter a tempo, use the default
        tempo = int(tempo_input) if tempo_input else default_tempo
    except ValueError:
        print(f"{RED}Veuillez entrer des valeurs valides.{RESET}")



    # Open MIDI output port
    try:
        midi_out = mido.open_output(mido.get_output_names()[2])  # Modify this if you have a specific output port

    except (OSError, IOError):
        print(f"{RED}Error: Could not open MIDI output port. Check your MIDI device connection.{RESET}")
        midi_out = None  # Set to None to avoid crashing if used later

    except IndexError:
        print(f"{RED}rror: MIDI output port index is out of range. Available ports: ", mido.get_output_names(), f"{RESET}")
        midi_out = None
    
    except ValueError as e:
        print(f"{RED}Error: {e} {RESET}")
        midi_out = None

    # Load patterns from a file named from the user's input 
    patterns_file_name = time_signature_input.replace('/', '_') + '_patterns.txt'
    patterns = quick_import_patterns(f'./scoring/{patterns_file_name}')  
    
    if not scoring.sequence.main_sequence:
        print(f"{RED} No valid pattern sequence found. Exiting. {RESET}")
        return
    pattern_sequence = import_sequence(scoring.sequence.main_sequence, patterns)
    hide_cursor()
    # Start an infinite loop to repeat the sequence
    while True:  # Infinite loop to keep repeating the sequence
        try:
            for pattern_ref in pattern_sequence:
                if pattern_ref in patterns:
                    pattern = patterns[pattern_ref]
                    # Call the function to play the pattern
                    print(f"{BLUE}Bar {YELLOW}{scoring.settings.global_bar_counter}{RESET}:\t\t {BLUE}Pattern {GREEN}{pattern_ref} \tTF : {RED}{scoring.settings.tension_factor}{RESET}", end="\n") #\r to return 
                    play_pattern(pattern, tempo, midi_out, channel=9)
                else:
                    print(f"{RED}Pattern {pattern_ref} not found in the loaded patterns.{RESET}")
            
            # After all patterns in the sequence are played, the loop will restart
            print(f"{BLUE}Looping the sequence ... {RESET}                   ")

        except KeyboardInterrupt:
            print(f"\n{RED}Stopping Sequencer, Script & Synth...{RESET}")
            synth_process.terminate()  # Ensure Qsynth is closed
            sys.exit(0)  # Exit script

if __name__ == "__main__":
    main()
