import re

import re

# Simple and quick pattern import without any checks
def quick_import_patterns(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    patterns = {}
    pattern_lines = []
    pattern_metadata = {}
    pattern_reference = None

    for line in lines:
        line = line.strip()
        
        if not line:
            # If we hit a blank line, process the current pattern
            if pattern_lines:
                pattern_metadata = parse_headers(pattern_lines)
                if pattern_metadata:
                    pattern_reference = pattern_metadata.get('Reference')
                    # Parse instrument lines with the valid metadata
                    instruments = parse_instruments(pattern_lines[len(metadata_to_lines(pattern_metadata)):], pattern_metadata)
                    pattern = {
                        'metadata': pattern_metadata, 
                        'instruments': instruments
                    }
                    if pattern_reference:
                        patterns[pattern_reference] = pattern
                pattern_lines = []  # Reset for the next pattern
        else:
            pattern_lines.append(line)
    
    # Process the last pattern in the file
    if pattern_lines:
        pattern_metadata = parse_headers(pattern_lines)
        if pattern_metadata:
            pattern_reference = pattern_metadata.get('Reference')
            instruments = parse_instruments(pattern_lines[len(metadata_to_lines(pattern_metadata)):], pattern_metadata)
            pattern = {
                'metadata': pattern_metadata, 
                'instruments': instruments
            }
            if pattern_reference:
                patterns[pattern_reference] = pattern
    
    return patterns


# Function to parse the headers for metadata
def parse_headers(lines):
    metadata = {}
    for line in lines:
        if line.startswith("#"):
            line = line[1:].strip()
            if ":" not in line:
                continue
            field_name, value = line.split(":", 1)
            field_name = field_name.strip()
            value = value.strip()
            metadata[field_name] = int(value) if field_name in ["Bars", "Resolution"] else value
    return metadata


# Convert metadata back into a list of formatted lines (for indexing)
def metadata_to_lines(metadata):
    return [f"# {key}: {value}" for key, value in metadata.items()]


# Function to parse the instrument parts for playback, excluding probs
def parse_instruments(lines, metadata):
    instruments = {}
    lines_iter = iter(lines)

    for line in lines_iter:
        if ":" not in line:
            continue

        instrument_name, steps = line.split(":", 1)
        instrument_name = instrument_name.strip()
        steps = steps.strip()

        # Count all played steps (X, x, O, o)
        step_count = sum(1 for char in steps if char in ('X', 'x', 'O', 'o'))

        # We no longer need to extract or parse probs
        # Simply store the steps in the instrument data
        instruments[instrument_name] = {
            'steps': steps
        }
    
    return instruments

"""
# Example Usage
filename = './scoring/4_4_patterns.txt'

# Quick import patterns
patterns = quick_import_patterns(filename)
for pattern_ref, pattern in patterns.items():
    print(f"Pattern {pattern_ref}: {pattern['metadata']}")
    for instrument_name, instrument_data in pattern['instruments'].items():
        print(f"  {instrument_name}: {instrument_data['steps']}")
        print(f"    Probs: {instrument_data['probs']}")
"""