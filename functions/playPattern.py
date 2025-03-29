import time
import mido
import scoring.settings  # Import the whole module
from functions.check_tf import update_tf
from functions.modify_pattern import modify_pattern  # Import the modification function

# Function to play a pattern using MIDI output
def play_pattern(pattern, tempo, midi_output_port, channel):
    """
    Plays a pattern using MIDI output where all instruments play simultaneously at each step.
    The `midi_output_port` is the opened MIDI output port.
    """
    # Set up time between steps based on tempo (BPM)
    step_duration = 60 / (tempo * int(pattern['metadata']['Signature'].split("/")[1]))  
    nb_bars = int(pattern['metadata']['Bars'])
    num_steps = len(pattern['instruments']['BD']['steps'])
    # Access the global tension_factor directly from scoring.settings
    tension_factor = scoring.settings.tension_factor  # Access the tension_factor here
    
    # Add debug to check the selected rules based on tension factor
    # IN FACT this is wrong, as a positive tension factor doesn't mean complexify ...
    # IT should be the difference from the previous TF ... augmenting or decreasing 
    # the current value of the TF should be used only to say if the pattern is already complex or simple 
    #print(f"Tension Factor: {tension_factor}")
    if tension_factor > 0:
        selected_rules = scoring.rules.rules['complexify']
        #print(f"Applying complexify rules: {selected_rules}")
    else:
        selected_rules = scoring.rules.rules['simplify']
        #print(f"Applying simplify rules: {selected_rules}")

    # Modify the pattern if tension factor is non-zero
    if tension_factor != 0:
        pattern['instruments'] = modify_pattern(pattern, tension_factor)
        #print(pattern['instruments'])
    
    # Loop through the steps of the pattern
    for step_idx in range(num_steps):
        # For each step, check the sequence for all instruments
        for instrument, data in pattern['instruments'].items():
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
        for instrument in pattern['instruments']:
            midi_note = scoring.settings.instrument_mapping.get(instrument)
            if midi_note:
                midi_output_port.send(mido.Message('note_off', note=midi_note, velocity=velocity, channel=channel))

    scoring.settings.global_bar_counter += nb_bars  # add these bars to counter 
    update_tf()
