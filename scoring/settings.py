# Global bar counter
global_bar_counter = 1
event_index = 0
tension_factor = 0.0
previous_tension_factor = 0.0
sequence_size = 0
global_events = []
last_played_pattern_ref = ''
# low and hi velocity for midi notes 
low_velo = 70
hi_velo = 120
# number of notes to be replaced in stochastic function 'modify_pattern' (3 levels)
stochastic_lo = 1   # ie mild 
stochastic_mid = 3  # ie medium 
stochastic_hi = 5   # strong
# for tension zones  
tension_zone_multipliers = {
    'very_sparse': 1.5,
    'sparse': 1.3,
    'light': 1.15,
    'neutral': 1.0,
    'dense': 0.85,
    'very_dense': 0.7,
    'ultra_dense': 0.55
}

instrument_allowances = {
    'HH': 0.2,    # Hi-Hat - only 20% can be modified
    'BD': 0.6,    # Bass Drum - up to 60% can be modified
    'SD': 0.8,    # Snare Drum - up to 60% can be modified
    'default': 1.0  # Default for other instruments (no restrictions)
}
    
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