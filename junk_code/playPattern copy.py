import time
import mido
import scoring.settings  # Import the whole module
import scoring.rules_dict
from functions.check_tf import update_tf
from functions.modify_pattern import modify_pattern  # Import the modification function
from functions.analysis import analyze_pattern_complexity

# Function to play a pattern using MIDI output
def play_pattern(pattern, tempo, midi_output_port, channel):
    """
    Plays a pattern using MIDI output where all instruments play simultaneously at each step.
    The `midi_output_port` is the opened MIDI output port.
    """
    # Access the global tension_factor directly from scoring.settings if TF != 0
    tension_factor = scoring.settings.tension_factor  # Access the tension_factor here
    previous_tension_factor = scoring.settings.previous_tension_factor  # Store the previous TF value (you might need to store this in scoring.settings)
    delta_tf = tension_factor - previous_tension_factor
    current_pattern = {}
    selected_rules = {}
    current_complexity, current_inst_complexity = analyze_pattern_complexity(pattern)
    print("PATTERN COMPLEXITY : ", current_complexity, current_inst_complexity )
    #print(pattern)
    # do nothing if TF is zero (ALSO ADD the DELTA TF == 0)
    if tension_factor == 0:
        current_pattern = pattern   
    else:  
        if delta_tf > 0:  # TF has increased
            direction = 'complexify'
        elif delta_tf < 0:  # TF has decreased
            direction = 'simplify'

        dtf_abs = abs(delta_tf)
        if dtf_abs <= 0.3:
            level = 'mild'
        elif dtf_abs <= 0.7:
            level = 'medium'
        else:
            level = 'strong'
        
        # get the right rules  
        selected_rules = scoring.rules_dict.rules[direction][level]   
        print("MOTION : " , direction , level )
        #print(pattern)
        print("SELECTED RULES : ", selected_rules)
        # kept just for debug as it should be : current_pattern = modify_pattern(pattern,rules)     
        current_pattern = modify_pattern(pattern,selected_rules)
        #print(current_pattern)

    # START analyzing & modifying the pattern locally 
        
    # Set up time between steps based on tempo (BPM)
    step_duration = 60 / (tempo * int(current_pattern['metadata']['Signature'].split("/")[1]))  
    nb_bars = int(current_pattern['metadata']['Bars'])
    num_steps = len(current_pattern['instruments']['SD']['steps'])

    # Add debug to check the selected rules based on tension factor
    # IN FACT this is wrong, as a positive tension factor doesn't mean complexify ...
    # IT should be the difference from the previous TF ... augmenting or decreasing 
    # the current value of the TF should be used only to say if the pattern is already complex or simple 
    #print(f"Tension Factor: {tension_factor}")

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
    update_tf()
    scoring.settings.last_played_pattern_ref = current_pattern['metadata']['Reference'] # indicate last played pattern
    