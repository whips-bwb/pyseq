import random
import re
import scoring.rules

def modify_pattern(pattern, tension_factor):
    """
    Modifies a given pattern based on the tension factor.
    The modification can either be to complexify or simplify the pattern.
    """
    modified_pattern = {}
    
    for instrument, data in pattern['instruments'].items():
        original_sequence = data['steps']
        
        # Apply modification rules if the tension factor is non-zero
        if tension_factor != 0:
            if tension_factor > 0:  # Complexify the pattern
                modified_sequence = modify_line_with_randomness(original_sequence, scoring.rules.rules['complexify'], instrument)
            else:  # Simplify the pattern
                modified_sequence = modify_line_with_randomness(original_sequence, scoring.rules.rules['simplify'], instrument)
            
            # Update the instrument steps with the modified sequence
            # ✅ Ensure same length as original
            if len(modified_sequence) < len(original_sequence):
                modified_sequence = modified_sequence.ljust(len(original_sequence), "-")  # Pad with silence
            elif len(modified_sequence) > len(original_sequence):
                modified_sequence = modified_sequence[:len(original_sequence)]  # Trim excess
                
            modified_pattern[instrument] = data.copy()
            modified_pattern[instrument]['steps'] = modified_sequence
        else:
            modified_pattern[instrument] = data  # No modification if TF is 0
    
    return modified_pattern

def modify_line_with_randomness(line, rules, instrument):
    """
    Apply random modifications based on the provided rules to the given sequence line.
    """
    modified_line = list(line)
    
    for rule in rules['general']:
        pattern, replacement = rule
        if re.search(pattern, line):
            modified_line = [re.sub(pattern, replacement, char) for char in line]
    
    # Apply instrument-specific rules
    for rule in rules['instrument_specific'].get(instrument, []):
        pattern, replacement = rule
        if re.search(pattern, line):
            modified_line = [re.sub(pattern, replacement, char) for char in line]

    # Return the modified line, making sure it's the same length as the original
    return ''.join(modified_line[:len(line)])



