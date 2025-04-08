import random
import re

def modify_pattern(pattern, rules):
    """
    Modifies a given pattern using the selected rules.
    Applies instrument-specific rules first if available, otherwise applies general rules.
    The pattern will not have both applied at the same time.
    """
    modified_pattern = pattern.copy() 

    for instrument, data in pattern['instruments'].items():
        original_sequence = data['steps']
        
        # Apply the rules (first check for instrument-specific rules, otherwise apply general rules)
        modified_sequence = modify_line_with_randomness(original_sequence, rules, instrument)

        # Ensure sequence length remains the same after modification
        if len(modified_sequence) < len(original_sequence):
            modified_sequence = modified_sequence.ljust(len(original_sequence), "-")
        elif len(modified_sequence) > len(original_sequence):
            modified_sequence = modified_sequence[:len(original_sequence)]

        # Store the modified pattern
        modified_pattern['instruments'][instrument]['steps'] = modified_sequence

    return modified_pattern


def modify_line_with_randomness(line, rules, instrument):
    #print(f"Original line ({instrument}): {line}")  # Debug

    # Apply general rules
    for pattern, replacement in rules.get('general', []):  # Using .get() to handle the case where 'general' might be missing
        if re.search(pattern, line):
            #print(f"Applying general rule: {pattern} -> {replacement}")  # Debug
            line = re.sub(pattern, replacement, line)

    # Apply instrument-specific rules (only if they exist)
    if 'instrument_specific' in rules:
        instrument_rules = rules['instrument_specific'].get(instrument, [])
        for pattern, replacement in instrument_rules:
            if re.search(pattern, line):
                print(f"Applying specific rule for {instrument}: {pattern} -> {replacement}")  # Debug
                line = re.sub(pattern, replacement, line)

    #print(f"Modified line ({instrument}): {line}\n")  # Debug
    return line

def stochastic_modify_line(line, direction, strength='mild'):
    """
    Applies a stochastic modification to a line of drum steps.

    :param line: str, 16-step pattern (e.g., 'X---x---X---x---')
    :param direction: 'complexify' or 'simplify'
    :param strength: 'mild', 'medium', or 'strong'
    :return: modified pattern string
    """
    active_hits = {'x', 'X', 'o', 'O'}
    steps = list(line)
    indices = list(range(len(steps)))

    # Define probabilities for adding/removing hits
    levels = {
        'mild': 2,
        'medium': 4,
        'strong': 6
    }
    num_changes = levels.get(strength, 2)

    if direction == 'complexify':
        empty_indices = [i for i in indices if steps[i] == '-']
        chosen = random.sample(empty_indices, min(num_changes, len(empty_indices)))
        for i in chosen:
            steps[i] = random.choice(['x', 'X', 'o' , 'O'])  # Add soft/hard hit

    elif direction == 'simplify':
        hit_indices = [i for i in indices if steps[i] in active_hits]
        chosen = random.sample(hit_indices, min(num_changes, len(hit_indices)))
        for i in chosen:
            steps[i] = '-'  # Remove hit

    return ''.join(steps)
