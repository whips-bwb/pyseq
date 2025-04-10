import time
import mido
import scoring.settings  # Import the whole module
import scoring.rules_dict
from functions.modify_pattern import modify_pattern, stochastic_modify_line  # Import the modification function
from functions.analysis import analyze_pattern_complexity
from pprint import pprint
import copy


# Function to play a pattern using MIDI output
def play_pattern(pattern, tempo, midi_output_port, channel):
    """
    Plays a pattern using MIDI output where all instruments play simultaneously at each step.
    The `midi_output_port` is the opened MIDI output port.
    """

    current_pattern = copy.deepcopy(pattern)
    # Access the global tension_factor directly from scoring.settings if TF != 0
    tension_factor = round(scoring.settings.tension_factor ,2) # Access the tension_factor here
    previous_tension_factor = round(scoring.settings.previous_tension_factor,2)  # Store the previous TF value (you might need to store this in scoring.settings)
    delta_tf = round(tension_factor - previous_tension_factor, 2)
    #print("dTF : ", delta_tf)
    # do nothing if TF is zero (ALSO ADD the DELTA TF == 0)
    if tension_factor == 0:
        pass
    else:  
        if delta_tf != 0:
            if delta_tf > 0:
                direction = 'complexify'
            else:
                direction = 'simplify'
            dtf_abs = abs(delta_tf)
            level = (
                'mild' if dtf_abs <= 0.3 else
                'medium' if dtf_abs <= 0.7 else
                'strong'
            )
            #print("MOTION : " , "dTF : " , delta_tf , " dir : " , direction , " lvl : ", level )
            
            for instrument, line_dict in current_pattern['instruments'].items():
                if 'steps' in line_dict:
                    old_line = line_dict['steps']
                    new_line = stochastic_modify_line(old_line, direction, level)
                    current_pattern['instruments'][instrument]['steps'] = new_line
        #pprint(current_pattern)
    # Set up time between steps based on tempo (BPM)
    step_duration = 60 / (tempo * int(current_pattern['metadata']['Signature'].split("/")[1]))  
    nb_bars = int(current_pattern['metadata']['Bars'])
    num_steps = len(current_pattern['instruments']['SD']['steps'])

    # Loop through the steps of the pattern
    for step_idx in range(num_steps):
        # For each step, check the sequence for all instruments
        for instrument, data in current_pattern['instruments'].items():
            sequence = data['steps']

            if sequence[step_idx] == 'X':  # Accent hit
                velocity = scoring.settings.hi_velo
                midi_note = scoring.settings.instrument_mapping.get(instrument)
                if midi_note:
                    midi_output_port.send(mido.Message('note_on', note=midi_note, velocity=velocity, channel=channel))
                    note_played = True

            elif sequence[step_idx] == 'x':  # Normal hit
                velocity = scoring.settings.low_velo
                midi_note = scoring.settings.instrument_mapping.get(instrument)
                if midi_note:
                    midi_output_port.send(mido.Message('note_on', note=midi_note, velocity=velocity, channel=channel))
                    note_played = True

            elif sequence[step_idx] == 'O':  # Alternate sound with accent
                velocity = scoring.settings.hi_velo
                midi_note = scoring.settings.alternate_instrument_mapping.get(instrument)
                if midi_note:
                    midi_output_port.send(mido.Message('note_on', note=midi_note, velocity=velocity, channel=channel))
                    note_played = True

            elif sequence[step_idx] == 'o':  # Alternate sound normal
                velocity = scoring.settings.low_velo
                midi_note = scoring.settings.alternate_instrument_mapping.get(instrument)
                if midi_note:
                    midi_output_port.send(mido.Message('note_on', note=midi_note, velocity=velocity, channel=channel))
                    note_played = True  
        
        # After triggering all instruments for this step, wait for the next step
        time.sleep(step_duration)
        
        # After each step, send a MIDI note off message to stop the sounds
        for instrument in current_pattern['instruments']:
            midi_note = scoring.settings.instrument_mapping.get(instrument)
            if midi_note:
                midi_output_port.send(mido.Message('note_off', note=midi_note, velocity=0, channel=channel))
                

    scoring.settings.global_bar_counter += nb_bars  # add these bars to counter 
    scoring.settings.last_played_pattern_ref = current_pattern['metadata']['Reference'] # indicate last played pattern
    