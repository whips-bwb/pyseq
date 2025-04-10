import random
import re
import scoring.settings

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


def stochastic_modify_line(line, direction, strength='mild', density_zone='neutral', instrument='default'):
    """
    Applies a stochastic modification to a line of drum steps, allowing for instrument-specific modification allowances.
    
    :param line: 16-step pattern (e.g., 'X---x---X---x---')
    :param direction: 'complexify' or 'simplify'
    :param strength: 'mild', 'medium', or 'strong'
    :param density_zone: 'very_sparse' to 'very_dense'
    :param instrument: Name of the instrument being modified (for specific allowance control)
    :return: modified pattern string
    """
    active_hits = {'x', 'X', 'o', 'O'}
    steps = list(line)
    indices = list(range(len(steps)))
    

    # Get the allowance for the instrument
    allowance = scoring.settings.instrument_allowances.get(instrument, scoring.settings.instrument_allowances['default'])

    # Adjust number of changes based on strength and density_zone
    base_changes = {
        'mild': scoring.settings.stochastic_lo,
        'medium': scoring.settings.stochastic_mid,
        'strong': scoring.settings.stochastic_hi
    }.get(strength, 2)

    density_mod = scoring.settings.tension_zone_multipliers.get(density_zone, 1.0)
    num_changes = max(1, round(base_changes * density_mod * allowance))

    if direction == 'complexify':
        empty_indices = [i for i in indices if steps[i] == '-']
        chosen = random.sample(empty_indices, min(num_changes, len(empty_indices)))
        for i in chosen:
            steps[i] = random.choice(['x', 'X', 'o', 'O'])  # Add hit

    elif direction == 'simplify':
        hit_indices = [i for i in indices if steps[i] in active_hits]
        chosen = random.sample(hit_indices, min(num_changes, len(hit_indices)))
        for i in chosen:
            steps[i] = '-'  # Remove hit

    return ''.join(steps)


    """
    # TO TEST , enhanced function with low symplify strength @ instrument protection 
    def stochastic_modify_line(line, direction, strength='mild', density_zone='neutral', instrument='A1'):
    '''
    Applies a stochastic modification to a line of drum steps.
    :param line: 16-step pattern (e.g., 'X---x---X---x---')
    :param direction: 'complexify' or 'simplify'
    :param strength: 'mild', 'medium', or 'strong'
    :param density_zone: 'very_sparse' to 'very_dense'
    :param instrument: Name of the instrument being processed (for applying instrument-specific rules)
    :return: modified pattern string
    '''
    import random
    active_hits = {'x', 'X', 'o', 'O'}
    steps = list(line)
    indices = list(range(len(steps)))

    # Adjust number of changes based on strength + density_zone
    base_changes = {
        'mild': scoring.settings.stochastic_lo,
        'medium': scoring.settings.stochastic_mid,
        'strong': scoring.settings.stochastic_hi
    }.get(strength, 2)

    density_mod = scoring.settings.tension_zone_multipliers.get(density_zone, 1.0)
    
    # Adjust the number of changes based on the TF value itself (for more gradual changes)
    tf_mod = 1.0 if scoring.settings.tension_factor >= 0.5 else (scoring.settings.tension_factor / 2)  # Less aggressive for high TF
    num_changes = max(1, round(base_changes * density_mod * tf_mod))

    # If the instrument is the HH (or other key instruments), reduce the number of changes
    if instrument in ['HH']:
        num_changes = max(1, num_changes // 2)  # Half the simplification for HH

    if direction == 'complexify':
        empty_indices = [i for i in indices if steps[i] == '-']
        chosen = random.sample(empty_indices, min(num_changes, len(empty_indices)))
        for i in chosen:
            steps[i] = random.choice(['x', 'X', 'o', 'O'])  # Add soft/hard hit

    elif direction == 'simplify':
        hit_indices = [i for i in indices if steps[i] in active_hits]
        chosen = random.sample(hit_indices, min(num_changes, len(hit_indices)))
        for i in chosen:
            steps[i] = '-'  # Remove hit

    return ''.join(steps)

    """
