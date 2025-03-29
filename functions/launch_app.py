import subprocess
import time
import sys
import mido
from functions.display import *
import scoring.settings
import scoring.sequence
from functions.quick_import_patterns import quick_import_patterns  
from functions.playPattern import play_pattern
from functions.import_sequence import import_sequence
from functions.display import *


def launch_app():
    # first launch a synth instance (FluidSynth or Qsynth)
    synth_instance = launch_synth()
    # then open the relevant midi port
    midi_out_handler = open_midi_port()
    # then get the user's inputs (or defaults)
    time_signature, tempo = get_seq_params()
    # then import score/sequence
    patterns_libs, score = load_score_and_patterns(time_signature)  # type: ignore
    # finally launch pattern play
    start_sequencer(tempo, time_signature, midi_out_handler, synth_instance, patterns_libs, score)


def launch_synth():
    try:
        #launch automatically the FluidSynth instance locally
        print(f"\n{YELLOW}launching FluidSynth instance !{RESET}")
        synth_process = subprocess.Popen(
            ["fluidsynth", "-a", "pulseaudio", "-f", "scoring/FSconfig.txt" , "-m", "alsa_seq",  "/usr/share/sounds/sf2/FluidR3_GM.sf2"],
#            ["fluidsynth", "-a", "alsa", "-f", "scoring/FSconfig.txt" , "-m", "alsa_seq",  "/usr/share/sounds/sf2/FluidR3_GM.sf2"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        time.sleep(1)
    except FileNotFoundError as e:
        print(f"Error: FluidSynth or one of the specified files (e.g., soundfont, config) was not found. {e}")

    except OSError as e:
        print(f"OS Error: There was an error launching FluidSynth. {e}")

    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: FluidSynth returned an error code. {e}")

    except ValueError as e:
        print(f"ValueError: There was an issue with the command arguments. {e}")
    print(f"{BLUE}MIDI opens : {mido.open_output(mido.get_output_names()[2])}{RESET}\n") # type: ignore # to check if the port is existing ... 
    return synth_process # type: ignore


def open_midi_port():
        # Open MIDI output port
    try:
        midi_out = mido.open_output(mido.get_output_names()[2])  # type: ignore # Modify this if you have a specific output port

    except (OSError, IOError):
        print(f"{RED}Error: Could not open MIDI output port. Check your MIDI device connection.{RESET}")
        midi_out = None  # Set to None to avoid crashing if used later

    except IndexError:
        print(f"{RED}rror: MIDI output port index is out of range. Available ports: ", mido.get_output_names(), f"{RESET}") # type: ignore
        midi_out = None
    
    except ValueError as e:
        print(f"{RED}Error: {e} {RESET}")
        midi_out = None
    return midi_out


def get_seq_params():
    try:
        #print(f"{mido.open_output(mido.get_output_names()[2])}")
        # Default values
        default_signature = "4/4"
        default_tempo = 120
        # Prompt user with default values in parentheses
        time_signature = input(f"{YELLOW}SIGNATURE ? {RESET}(2/4 to 19/8) [default: {default_signature}] : ") or default_signature
        tempo_input = input(f"{YELLOW}TEMPO / BPM ? {RESET}[default: {default_tempo}] : ")
        # If user didn't enter a tempo, use the default
        tempo = int(tempo_input) if tempo_input else default_tempo
    except ValueError:
        print(f"{RED}Veuillez entrer des valeurs valides.{RESET}")
    return time_signature, tempo # type: ignore


def load_score_and_patterns(time_signature):
    # Load patterns from a file named from the user's input 
    patterns_file_name = time_signature.replace('/', '_') + '_patterns.txt'
    patterns_file_path = f'./scoring/{patterns_file_name}'
    try:
        patterns_lib = quick_import_patterns(patterns_file_path)
    except FileNotFoundError:
        print(f"{RED}⚠️ Warning: Pattern file '{patterns_file_name}' not found.{RESET}")
        patterns_lib = {}  # Or provide a fallback mechanism
        return
    # if sequence/score is missing ... 
    if not scoring.sequence.main_sequence:
        print(f"{RED} No valid pattern sequence found. Exiting. {RESET}")
        return
    
    pattern_sequence = import_sequence(scoring.sequence.main_sequence, patterns_lib)
    # if patterns in sequence/score doesn't match with patterns in the lib/
    if not verify_patterns_presence(pattern_sequence, patterns_lib):
        print(f"{RED}⚠️ Some patterns are missing. Please check your pattern files.{RESET}")
        return
    return patterns_lib, pattern_sequence

# in fact not really needed as missing patterns will be truncated in the score ... 
def verify_patterns_presence(pattern_sequence, patterns_lib):
    missing_patterns = [pattern for pattern in pattern_sequence if pattern not in patterns_lib]
    
    if missing_patterns:
        print(f"{RED}⚠️ Warning: The following patterns are missing from the library: {missing_patterns}{RESET}")
        return False
    return True


def start_sequencer(tempo, time_signature, midi_out_handler, synth_instance, patterns_libs, score):
    hide_cursor()
    # Start an infinite loop to repeat the sequence
    while True:  # Infinite loop to keep repeating the sequence
        try:
            for pattern_ref in score:
                if pattern_ref in patterns_libs:
                    pattern = patterns_libs[pattern_ref]
                    # Call the function to play the pattern
                    print(f"{BLUE}Bar {YELLOW}{scoring.settings.global_bar_counter}{RESET}:\t\t {BLUE}Pattern {GREEN}{pattern_ref} \tTF : {RED}{scoring.settings.tension_factor}{RESET}", end="\n") #\r to return 
                    play_pattern(pattern, tempo, midi_out_handler, channel=9)
                else:
                    print(f"{RED}Pattern {pattern_ref} not found in the loaded patterns.{RESET}")
            
            # After all patterns in the sequence are played, the loop will restart
            print(f"{BLUE}Looping the sequence ... {RESET}                   ")

        except KeyboardInterrupt:
            print(f"\n{RED}Stopping Sequencer, Script & Synth...{RESET}")
            synth_instance.terminate()  # Ensure FluidSynth is closed
            sys.exit(0)  # Exit script
