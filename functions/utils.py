from functions.display import *
from scoring.settings import *
import mido # type: ignore
from mido import Message, MidiFile, MidiTrack, open_output
import time

def metro_precount(tempo, time_signature, midi_out_handler, precount_measures):
    print(f"{BGyellow}precounting a {time_signature} at {tempo}{RESET}\n")
    play_click(time_signature, tempo, midi_out_handler , precount_measures)
    

# Fonction pour jouer un clic de métronome
def play_click(time_signature_input, tempo, midi_out_handler , nb_measures):
    # Analyser la signature temporelle
    time_signature = tuple(map(int, time_signature_input.split("/")))
    beats_per_bar, note_value = time_signature
    beat_count = 1
    bar_count = 1
    beat_duration = 60000 / tempo
    beat_duration = beat_duration / 2 if note_value == 8 else beat_duration
    sound_duration = 0.0001
    interval_between_notes = (beat_duration/1000) - sound_duration

    hide_cursor()
    # start the loop 
    try:
        while bar_count <= nb_measures:
            # Colorize the bar and beat count using variables
            if beat_count == 1:
                print(f"{YELLOW}Bar {bar_count} - Beat {beat_count} {RESET}", end="\r")  # Yellow for the first bar
                metro_note = instrument_mapping[hi_inst] 
            else:
                print(f"{RED}Bar {bar_count} - Beat {beat_count} {RESET}", end="\r")  # Red for subsequent bars
                metro_note = alternate_instrument_mapping[lo_inst]
            # Add a new line
            print("")  # Add a new line for space
            # Move the cursor back to the previous line
            print("\033[F", end='')
            # Envoi d'un message "note_on" (clic)
            midi_out_handler.send(mido.Message('note_on', note=metro_note, velocity=100, channel=9))  # Note 60 correspond au C4
            # Durée de la note (son) avant de l'arrêter
            time.sleep(sound_duration)
            # Envoi du message "note_off" (fin de note)
            midi_out_handler.send(mido.Message('note_off', note=metro_note, velocity=100, channel=9))  # Fin de note
            # Attente pour la durée du battement avant le prochain clic
            time.sleep(interval_between_notes)
            # Mise à jour du compteur de battements et réinitialisation après la fin de la barre
            beat_count += 1
            if beat_count > beats_per_bar:
                beat_count = 1
                bar_count += 1
    finally:
        show_cursor()
        