import re
import scoring.settings
from functions.display import *
from pprint import pprint

def import_sequence(pattern_sequence, patterns):
    """
    Expands pattern repetitions in the sequence and tracks special events.
    """
    expanded_sequence = []
    event_bar_counter = 1  # Local bar counter for events

    if not hasattr(scoring.settings, 'global_events'):
        scoring.settings.global_events = []  # Initialize if not already present

    # Matches '00', '01', etc.
    pattern_reference = re.compile(r'^[A-Z]\d{2}$') 
    # Detect +y or -y patterns (e.g., "+4" or "-6")
    tension_pattern = re.compile(r'^[+-](\d)$')  

    for entry in pattern_sequence:
        # Case 0 : tension factor adjustment pattern
        if tension_pattern.match(entry):  
            value = int(entry[1]) / 10  # Convert the digit to a float (e.g., "+4" → 0.4)
            if entry.startswith('-'):  
                value = -value  # Make it negative for decrements
            
            scoring.settings.global_events.append({
                'type': entry,
                'at_bar': event_bar_counter,  # Store current bar position
                'value': value
            })        

        # **Case 1: Special Patterns (Mode Change or Tension Change)**
        if pattern_reference.match(entry):
            scoring.settings.global_events.append({
                'type': entry,
                'at_bar': event_bar_counter  # Store current bar position + 1 for Xth starting bar (the next one) 
            })
            continue  # Skip adding to expanded_sequence
        
        # **Case 2: Normal Pattern with Multiplication (e.g., "A1x4")**
        if 'x' in entry:
            pattern_name, repeat_count = entry.split('x')
            repeat_count = int(repeat_count)

            if pattern_name in patterns:
                bars = patterns[pattern_name]['metadata'].get('Bars', 0)
                event_bar_counter += bars * repeat_count  # Multiply bars by repeat count

            expanded_sequence.extend([pattern_name] * repeat_count)
            continue  # Skip to next entry
        
        # **Case 3: Normal Pattern without Multiplication (e.g., "A1")**
        if entry in patterns:
            bars = patterns[entry]['metadata'].get('Bars', 0)
            event_bar_counter += bars  # Add bars to counter

            expanded_sequence.append(entry)

    scoring.settings.sequence_size = event_bar_counter - 1
    # debug infos 
    print(f"{BLUE}SEQUENCE:\n{GREEN}Size(bars): {YELLOW}{scoring.settings.sequence_size}\n{GREEN}Expanded Sequence: {YELLOW}{expanded_sequence}")
    print(f"{GREEN}Global Events: {YELLOW}")
    pprint(scoring.settings.global_events)
    print(f"{RESET}")

    return expanded_sequence
