
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

        # Select rules dynamically based on tension_factor intensity
        if tension_factor != 0:
            rule_type = 'complexify' if tension_factor > 0 else 'simplify'
            rule_set = scoring.rules.rules[rule_type]
           

            # Determine rule intensity range (mild, medium, strong changes)
            if abs(tension_factor) <= 0.3:
                selected_rules = rule_set['mild']
            elif abs(tension_factor) <= 0.6:
                selected_rules = rule_set['medium']
            else:
                selected_rules = rule_set['strong']

            # Apply modifications
            modified_sequence = modify_line_with_randomness(original_sequence, selected_rules, instrument)

            # Ensure sequence length remains unchanged
            if len(modified_sequence) < len(original_sequence):
                modified_sequence = modified_sequence.ljust(len(original_sequence), "-")
            elif len(modified_sequence) > len(original_sequence):
                modified_sequence = modified_sequence[:len(original_sequence)]

            modified_pattern[instrument] = data.copy()
            modified_pattern[instrument]['steps'] = modified_sequence
        else:
            modified_pattern[instrument] = data  # No modification if TF is 0

    return modified_pattern



def modify_line_with_randomness(line, rules, instrument):
    print(f"Original line ({instrument}): {line}")  # Debug

    # Debug: Check applied rules for instrument
    #print(f"Applying general rules: {rules['general']}")
    for pattern, replacement in rules['general']:
        if re.search(pattern, line):
            print(f"Applying general rule: {pattern} -> {replacement}")  # Debug
            modified_line = re.sub(pattern, replacement, line)

    if instrument in rules['instrument_specific']:
        #print(f"Applying specific rules for {instrument}: {rules['instrument_specific'][instrument]}")
        for pattern, replacement in rules['instrument_specific'][instrument]:
            if re.search(pattern, line):
                print(f"Applying specific rule for {instrument}: {pattern} -> {replacement}")  # Debug
                modified_line = re.sub(pattern, replacement, line)

    modified_result = modified_line  #  old : modified_result = ''.join(modified_line[:len(line)])
    print(f"Modified line ({instrument}): {modified_result}\n")  # Debug

    return modified_result

# -------------- NEWLY ADDED FCT 

# Function to modify a pattern based on its complexity and TF
def modify_pattern_by_complexity(pattern, complexity_scores, tf_delta, resolution=16):
    """
    Modify the pattern based on its complexity and TF delta.
    
    :param pattern: The current pattern (dict of instrument lines).
    :param complexity_scores: Complexity scores for each line.
    :param tf_delta: The change in tension factor (negative to simplify, positive to complexify).
    :param resolution: Resolution of the pattern (default 16).
    :return: A modified pattern.
    """
    modified_pattern = pattern.copy()  # Create a copy of the pattern to modify

    # Sort lines by complexity score
    sorted_lines = sorted(complexity_scores.items(), key=lambda x: x[1])

    if tf_delta > 0:
        # Complexify the pattern: Focus on simplifying simpler lines
        for instrument, score in sorted_lines:
            if score < 0.5:  # Focus on lines with low complexity
                modified_pattern[instrument] = complexify_line(modified_pattern[instrument], resolution)
            if tf_delta > 0.5:  # Stronger TF delta means more complexification
                modified_pattern[instrument] = add_variation(modified_pattern[instrument], resolution)
    elif tf_delta < 0:
        # Simplify the pattern: Focus on reducing complexity on complex lines
        for instrument, score in sorted_lines:
            if score > 0.7:  # Focus on lines with high complexity
                modified_pattern[instrument] = simplify_line(modified_pattern[instrument])

    return modified_pattern

def complexify_line(line, resolution=16):
    """
    Adds complexity to a line by introducing more rhythmic variety or additional hits.
    :param line: The line to complexify.
    :param resolution: The resolution of the pattern (default 16).
    :return: A more complex version of the line.
    """
    # Example: Add more hits in random places (you could also introduce rhythmic variation)
    line_list = list(line)
    for i in range(resolution):
        if random.random() < 0.2:  # 20% chance to add a hit in a random position
            line_list[i] = 'X'
    return ''.join(line_list)

def simplify_line(line):
    """
    Simplifies a line by removing hits or making rhythms more basic.
    :param line: The line to simplify.
    :return: A simpler version of the line.
    """
    line_list = list(line)
    for i in range(len(line_list)):
        if random.random() < 0.3:  # 30% chance to remove a hit
            line_list[i] = '-'
    return ''.join(line_list)

def add_variation(line, resolution=16):
    """
    Adds rhythmic variation to a line.
    :param line: The line to modify.
    :param resolution: The resolution of the pattern (default 16).
    :return: A more varied version of the line.
    """
    # Example: Change the position of existing hits for variation
    line_list = list(line)
    for i in range(resolution):
        if line_list[i] == 'X' and random.random() < 0.4:
            new_pos = random.randint(0, resolution-1)
            line_list[new_pos] = 'X'
            line_list[i] = '-'
    return ''.join(line_list)

import random

def evolve_pattern(pattern, complexity_data, tf, rules=None):
    """
    Modifies the current pattern based on the tension factor (TF) and predefined rules.
    
    :param pattern: dict containing instrument patterns.
    :param complexity_data: dict containing complexity values per instrument.
    :param tf: float, tension factor (-1 to 1) dictating simplification or complexification.
    :param rules: dict, optional specific rules for modification.
    :return: dict, modified pattern.
    """
    evolved_pattern = pattern.copy()
    
    for instrument, line in pattern.items():
        current_complexity = complexity_data.get(instrument, 0)
        
        if rules and instrument in rules:
            # Apply rule-based modification
            evolved_pattern[instrument] = apply_rule_modification(line, rules[instrument])
        else:
            # Apply constrained random evolution
            evolved_pattern[instrument] = apply_random_modification(line, tf, current_complexity)
    
    return evolved_pattern

def apply_rule_modification(line, rule):
    """Applies a predefined rule to modify a pattern line."""
    # Implement rule-based modification logic here
    return rule  # Placeholder, modify based on actual rule format

def apply_random_modification(line, tf, complexity):
    """Applies a constrained random transformation to the pattern line."""
    new_line = list(line)
    probability = abs(tf) * (1 - complexity)  # More impact where complexity is lower
    
    for i in range(len(new_line)):
        if random.random() < probability:
            new_line[i] = 'X' if new_line[i] == '-' else '-'
    
    return ''.join(new_line)


