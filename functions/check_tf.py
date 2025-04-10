import scoring.sequence
import scoring.settings
from functions.display import *

def update_tf():
    """
    Checks if the current global_bar_counter matches any scheduled event
    and triggers it.
    """
    if not hasattr(scoring.settings, 'global_events'):
        scoring.settings.global_events = []
    
    if not hasattr(scoring.settings, 'sequence_size') or scoring.settings.sequence_size == 0:
        print(f"{RED}⚠ ERROR: sequence_size is not set or is zero!{RESET}")
        return

    # Get current global bar count
    current_bar = scoring.settings.global_bar_counter

    # Compute absolute position in the sequence (in case of looping)
    absolute_loop_bar = current_bar % scoring.settings.sequence_size

    # Special case: if absolute_loop_bar == 0 and not the first bar, interpret it as end of sequence
    if absolute_loop_bar == 0 and current_bar != 0:
        sequence_index = scoring.settings.sequence_size - 1
    else:
        sequence_index = absolute_loop_bar

    # Check all events and trigger those that match the current sequence index
    for event in scoring.settings.global_events:
        if event['at_bar'] % scoring.settings.sequence_size == absolute_loop_bar:
            if event['type'].startswith(('+', '-')):  # Detect tension factor events
                scoring.settings.previous_tension_factor = scoring.settings.tension_factor
                scoring.settings.tension_factor += event['value']
                scoring.settings.tension_factor = round(scoring.settings.tension_factor, 2)  # Round to 2 decimals

            print(f"{WHITE}⚡ EVENT TRIGGERED {RESET} : {BGyellow} {event['type']} {RESET} at bar {BGyellow} {current_bar} {RESET}              ")
