import re

# Parse the file into a dictionary of patterns, identified by the reference
def parse_patterns(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    patterns = {}
    pattern_lines = []
    pattern_metadata = {}
    pattern_reference = None

    for line in lines:
        line = line.strip()
        
        if not line:
            if pattern_lines:
                pattern_metadata = check_headers(pattern_lines)
                if pattern_metadata:
                    pattern_reference = pattern_metadata.get('Reference')
                    pattern = {
                        'metadata': pattern_metadata, 
                        'instruments': parse_instruments(pattern_lines[1:], pattern_metadata)
                    }
                    if pattern_reference:
                        patterns[pattern_reference] = pattern
                pattern_lines = []
        else:
            pattern_lines.append(line)
    
    if pattern_lines:
        pattern_metadata = check_headers(pattern_lines)
        if pattern_metadata:
            pattern_reference = pattern_metadata.get('Reference')
            pattern = {
                'metadata': pattern_metadata, 
                'instruments': parse_instruments(pattern_lines[1:], pattern_metadata)
            }
            if pattern_reference:
                patterns[pattern_reference] = pattern
    
    return patterns

# Check headers and return metadata
def check_headers(lines):
    metadata = {}
    expected_fields = ["Reference", "Name", "Signature", "Bars", "Resolution"]
    
    for line in lines:
        if line.startswith("#"):
            line = line[1:].strip()
            if ":" not in line:
                continue
            field_name, value = line.split(":", 1)
            field_name = field_name.strip()
            value = value.strip()

            if field_name not in expected_fields:
                continue  

            if field_name == "Reference" or field_name == "Name":
                if not re.match(r'^[A-Za-z0-9]+$', value):
                    return None
                metadata[field_name] = value
            
            elif field_name == "Signature":
                match = re.match(r'^(\d+)\/(\d+)$', value)
                if not match:
                    return None
                metadata[field_name] = value
            
            elif field_name == "Bars":
                if not value.isdigit():
                    return None
                metadata[field_name] = int(value)
            
            elif field_name == "Resolution":
                if value not in ["8", "16"]:
                    return None
                metadata[field_name] = int(value)

    return metadata

# Parse the instrument parts of a pattern into a dictionary
def parse_instruments(lines, metadata):
    instruments = {}
    signature = metadata["Signature"]
    resolution = metadata["Resolution"]
    bars = metadata["Bars"]
    
    expected_steps = (resolution / int(signature.split("/")[1])) * int(signature.split("/")[0]) * bars
    
    line_iter = iter(lines)
    
    for line in line_iter:
        if ":" not in line:
            continue

        instrument_name, steps = line.split(":", 1)
        instrument_name = instrument_name.strip()
        steps = steps.strip()

        if not re.match(r'^[A-Za-z0-9]+$', instrument_name):
            continue

        step_count = len(steps)
        
        error = None
        if step_count != expected_steps:
            error = f"Expected {expected_steps} steps, but found {step_count} steps."
        
        instruments[instrument_name] = {
            'steps': steps,
            'error': error
        }
    
    return instruments

# Check for errors after parsing the patterns
def check_for_errors(patterns):
    errors = []
    
    for pattern_ref, pattern in patterns.items():
        metadata = pattern['metadata']
        instruments = pattern['instruments']

        for field in ["Reference", "Name", "Signature", "Bars", "Resolution"]:
            if field not in metadata:
                errors.append(f"Missing field '{field}' in metadata for pattern '{pattern_ref}'.")
        
        for instrument_name, instrument_data in instruments.items():
            if instrument_data['error']:
                errors.append(f"Pattern '{pattern_ref}', Instrument '{instrument_name}' error: {instrument_data['error']}")
    
    return errors

# Function to colorize and print patterns with error highlights
def print_colored_patterns(patterns):
    for pattern_ref, pattern in patterns.items():
        metadata = pattern['metadata']
        instruments = pattern['instruments']
        
        print(f"\033[33mPattern Reference: {pattern_ref}")
        print(f"  Name: {metadata.get('Name', 'N/A')}")
        print(f"  Signature: {metadata.get('Signature', 'N/A')}")
        print(f"  Bars: {metadata.get('Bars', 'N/A')}")
        print(f"  Resolution: {metadata.get('Resolution', 'N/A')}")
        print(f"  Instruments:")

        for instrument_name, instrument_data in instruments.items():
            steps = instrument_data['steps']
            error = instrument_data['error']

            # Print the instrument part (keeping color formatting)
            if error:
                print(f"\033[31m  {instrument_name}: {steps} - Error: {error}\033[0m")  # Red for error
            else:
                print(f"\033[32m  {instrument_name}: {steps}\033[0m")  # Green for no error

        print("\n" + "-"*40 + "\033[0m")  # Reset color

# Main function to parse the file and check for errors
def check_pattern(filename):
    patterns = parse_patterns(filename)
    print_colored_patterns(patterns)
    
    errors = check_for_errors(patterns)
    return [f"\n \033[31m {errors} \033[0m\n"] if errors else ["\n \033[32m All patterns are valid!\033[0m\n"]

# Example Usage
filename = './scoring/4_4_patterns.txt'

result = check_pattern(filename)
for line in result:
    print(line)

