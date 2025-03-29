

def analyze_line_complexity(line, resolution=16):
    """
    Analyzes a given line to assign a complexity score based on various factors like density,
    variation, and rhythmic structure.
    
    :param line: The pattern line to analyze (e.g., 'X---X--X-X---X-')
    :param resolution: The number of subdivisions per bar (default 16 for 16th notes)
    :return: A complexity score between 0 and 1.
    """
    # Step 1: Count number of hits ('X') in the line
    hits = line.count('X')
    
    # Step 2: Calculate note density (how many hits compared to resolution)
    density = hits / resolution
    
    # Step 3: Measure variation in hit placement (this is a rough approach, could be improved)
    # We look at how evenly the hits are distributed
    variations = len(set(line))  # Number of unique elements ('X' vs '-')
    
    # Step 4: Calculate rhythmic subdivisions (simplified version)
    subdivisions = 0
    for i in range(len(line)):
        if line[i] == 'X':
            if i % 2 == 0:
                subdivisions += 0.25  # For every 'X' on a half note
            elif i % 4 == 0:
                subdivisions += 0.5  # For every 'X' on a quarter note
            else:
                subdivisions += 1.0  # 16th or eighth notes
    
    # Normalize the final complexity score
    complexity_score = (density + variations * 0.1 + subdivisions * 0.05) / 2
    
    # The score should be between 0 and 1
    return min(1.0, complexity_score)

def analyze_pattern_complexity(pattern):
    complexity_scores = {}
    
    # Extract resolution from metadata
    resolution = pattern['metadata'].get('Resolution', 16)

    # Debugging: Print pattern structure
    #print(f"Debug: pattern={pattern}")

    # Ensure instruments exist
    if 'instruments' not in pattern:
        print("Debug: No instruments found in pattern.")
        return 0, {}

    for instrument, instrument_data in pattern['instruments'].items():
        # Ensure 'steps' exists for each instrument
        if 'steps' in instrument_data:
            line = instrument_data['steps']
            #print(f"Debug: instrument={instrument}, line={line}, type={type(line)}")
            complexity_scores[instrument] = analyze_line_complexity(line, resolution)
        else:
            print(f"Warning: 'steps' missing for instrument {instrument}")

    # Compute overall complexity
    pattern_complexity = sum(complexity_scores.values()) / max(len(complexity_scores), 1)

    return pattern_complexity, complexity_scores


