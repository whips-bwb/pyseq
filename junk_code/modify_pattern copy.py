
import random
import re
import scoring.rules_dict

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
            rule_set = scoring.rules_dict.rules[rule_type]
           

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




