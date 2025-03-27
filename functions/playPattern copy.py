import time
import mido
import scoring.settings  # Import the whole module
from functions.check_events import trigger_events

# Function to play a pattern using MIDI output
def play_pattern(pattern, tempo, midi_output_port, channel):
    """
    Plays a pattern using MIDI output where all instruments play simultaneously at each step.
    The `midi_output_port` is the opened MIDI output port.
    """
    # Set up time between steps based on tempo (BPM)
    # !!! should be calculated before calling 'play'
    step_duration = 60 / (tempo * int(pattern['metadata']['Signature'].split("/")[1]))  
    nb_bars = int(pattern['metadata']['Bars'])
    # Get the number of steps from the sequence length (all instruments should have the same length sequence)
    num_steps = len(pattern['instruments']['BD']['steps'])
    
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
                # Get the alternate sound MIDI note (example: for HH, alternate sound might be 'X' or 'O')
                midi_note = scoring.settings.alternate_instrument_mapping.get(instrument)  # Assume mapping includes alternate note logic
                if midi_note:
                    midi_output_port.send(mido.Message('note_on', note=midi_note, velocity=velocity, channel=channel))
                    note_played = True

            elif sequence[step_idx] == 'o':  # Alternate sound normal
                velocity = scoring.settings.low_velo
                # Get the alternate sound MIDI note (example: for HH, alternate sound might be 'X' or 'O')
                midi_note = scoring.settings.alternate_instrument_mapping.get(instrument)  # Assume mapping includes alternate note logic
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

    scoring.settings.global_bar_counter += nb_bars # add this(these) bar to counter 
    trigger_events()
    