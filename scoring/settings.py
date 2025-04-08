# Global bar counter
global_bar_counter = 1
event_index = 0
tension_factor = 0.0
previous_tension_factor = 0.0
sequence_size = 0
global_events = []
last_played_pattern_ref = ''

low_velo = 80
hi_velo = 120

instrument_mapping = {
    'BD': 35,   # Bass Drum
    'SD': 38,   # Snare Drum
    'HH': 42,   # Hi-Hat
    'RC': 51,   # RIDE Cymbal  
    'HT': 41,   # hi tom 
    'MT': 43,   # mid tom
    'LT': 45,   # lo tom
    'AG': 67,   # hi agogo
    'WB': 76,   # hi woodblock
    'TR': 80    # muted triangle

}
alternate_instrument_mapping = {
    'BD': 36,   # Bass Drum hi
    'SD': 37,   # Snare Drum Stick/rimshot
    'HH': 46,   # Open Hi-Hat
    'RC': 53,   # Ride Bell
    'HT': 41,   # hi tom 
    'MT': 43,   # mid tom
    'LT': 45,   # lo tom  
    'AG': 68,   # lo agogo 
    'WB': 77,   # lo woodblock  
    'TR': 81    # open triangle 
} 