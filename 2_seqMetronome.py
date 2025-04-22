import mido # type: ignore
import time
import random
from mido import Message, MidiFile, MidiTrack, open_output

msg = "--- PySeq Midi Sequencer ---"
print(f"\nWelcome to {msg} !\n")

#alternate port for inside synth 
# FLUID Synth (5913):Synth input port (5913:0) 128:0
#"FLUID Synth (15687):Synth input port (15687:0) 128:0"
# "MPX8:MPX8 MIDI 1 20:0"
midi_port_name = mido.get_output_names()[2]
out_midi_channel = 9 # standard midi drums
metro_low = 80 # 40 for MP8X, 44 for GM (pedal HH) 77 low woodblock 80 for mute triangle 
metro_high = 81 # 41 for MP8X, 42 for GM (Closed HH) 76 hi woodblock 81 for open triangle
# see GMdrumSounds file for more sound references ... s
YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# Hide cursor function
def hide_cursor():
    print("\033[?25l", end='')

# Show cursor function
def show_cursor():
    print("\033[?25h", end='')

# Function to fill the console width with a specific character
def fill_line(character, width):
    return character * width

# Fonction pour jouer un clic de métronome
def jouer_clic(time_signature_input, tempo):
    # Analyser la signature temporelle
    time_signature = tuple(map(int, time_signature_input.split("/")))
    beats_per_bar, note_value = time_signature
    beat_count = 1
    bar_count = 1
    beat_duration = 60000 / tempo
    beat_duration = beat_duration / 2 if note_value == 8 else beat_duration
    sound_duration = 0.0001
    interval_between_notes = (beat_duration/1000) - sound_duration
    output = mido.open_output(midi_port_name)  # Ouvre un port MIDI par défaut

    hide_cursor()
    # start the loop 
    try:
        while True:
            velocity = random.randint(80, 120)
            # Colorize the bar and beat count using variables
            if beat_count == 1:
                print(f"{YELLOW}Bar {bar_count} - Beat {beat_count} {RESET}", end="\r")  # Yellow for the first bar
                metro_note = metro_high
            else:
                print(f"{RED}Bar {bar_count} - Beat {beat_count} {RESET}", end="\r")  # Red for subsequent bars
                metro_note = metro_low
            # Add a new line
            print("")  # Add a new line for space
            # Move the cursor back to the previous line
            print("\033[F", end='')
            # Envoi d'un message "note_on" (clic)
            output.send(mido.Message('note_on', note=metro_note, velocity=100, channel=out_midi_channel))  # Note 60 correspond au C4
            # Durée de la note (son) avant de l'arrêter
            time.sleep(sound_duration)
            # Envoi du message "note_off" (fin de note)
            output.send(mido.Message('note_off', note=metro_note, velocity=100, channel=out_midi_channel))  # Fin de note
            # Attente pour la durée du battement avant le prochain clic
            time.sleep(interval_between_notes)
            # Mise à jour du compteur de battements et réinitialisation après la fin de la barre
            beat_count += 1
            if beat_count > beats_per_bar:
                beat_count = 1
                bar_count += 1
    finally:
        show_cursor()

# user prompt and calculus before starting 
if __name__ == "__main__":
    try:
        time_signature_input = input("SIGNATURE ? (2/4 to 19/8) ? : ")
        tempo = int(input("TEMPO / BPM ? : "))
        jouer_clic(time_signature_input=time_signature_input, tempo=tempo)
    except ValueError:
        print("Veuillez entrer des valeurs valides.")
