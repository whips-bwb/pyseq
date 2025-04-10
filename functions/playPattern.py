import time
import mido
import scoring.settings  # Import the whole module
import scoring.rules_dict
from functions.modify_pattern import modify_pattern, stochastic_modify_line  # Import the modification function
from functions.analysis import analyze_pattern_complexity
from pprint import pprint
import copy
from functions.display import *

# Function to play a pattern using MIDI output
def play_pattern(pattern, tempo, midi_output_port, channel):
    import copy
    current_pattern = copy.deepcopy(pattern)
    
    tension_factor = round(scoring.settings.tension_factor, 2)
    previous_tension_factor = round(scoring.settings.previous_tension_factor, 2)
    delta_tf = round(tension_factor - previous_tension_factor, 2)

    if tension_factor != 0 and delta_tf != 0:
        direction = 'complexify' if delta_tf > 0 else 'simplify'
        dtf_abs = abs(delta_tf)

        # Delta-based strength level
        level = (
            'mild' if dtf_abs <= 0.3 else
            'medium' if dtf_abs <= 0.7 else
            'strong'
        )

        # Absolute TF density zone
        if tension_factor >= 0.9:
            density_zone = 'ultra_dense'
        elif tension_factor >= 0.6:
            density_zone = 'very_dense'
        elif tension_factor >= 0.3:
            density_zone = 'dense'
        elif tension_factor >= -0.3:
            density_zone = 'neutral'
        elif tension_factor >= -0.9:
            density_zone = 'sparse'
        else:
            density_zone = 'very_sparse'
            
        print(f"DIR : {PURPLE} {direction} {RESET}, LVL : {PURPLE} {level} {RESET},  Tzone : {PURPLE} {density_zone} {RESET}")
        
        for instrument, line_dict in current_pattern['instruments'].items():
            if 'steps' in line_dict:
                old_line = line_dict['steps']
                new_line = stochastic_modify_line(old_line, direction, level, density_zone)
                current_pattern['instruments'][instrument]['steps'] = new_line

    # Play MIDI pattern
    step_duration = 60 / (tempo * int(current_pattern['metadata']['Signature'].split("/")[1]))  
    nb_bars = int(current_pattern['metadata']['Bars'])
    num_steps = len(current_pattern['instruments']['SD']['steps'])

    for step_idx in range(num_steps):
        for instrument, data in current_pattern['instruments'].items():
            sequence = data['steps']
            char = sequence[step_idx]
            if char in {'X', 'x', 'O', 'o'}:
                velocity = scoring.settings.hi_velo if char.isupper() else scoring.settings.low_velo
                mapping = (
                    scoring.settings.alternate_instrument_mapping
                    if char.lower() == 'o' else scoring.settings.instrument_mapping
                )
                midi_note = mapping.get(instrument)
                if midi_note:
                    midi_output_port.send(mido.Message('note_on', note=midi_note, velocity=velocity, channel=channel))

        time.sleep(step_duration)

        for instrument in current_pattern['instruments']:
            midi_note = scoring.settings.instrument_mapping.get(instrument)
            if midi_note:
                midi_output_port.send(mido.Message('note_off', note=midi_note, velocity=0, channel=channel))

    scoring.settings.global_bar_counter += nb_bars
    scoring.settings.last_played_pattern_ref = current_pattern['metadata']['Reference']
