def analyze_pattern_complexity(pattern):
    """
    Analyzes the rhythmic complexity of a drum pattern.

    :param pattern: dict with 'instruments' containing dicts with 'steps' strings
    :return: tuple of (overall complexity, dict of complexity per instrument)
    """
    active_hits = {'x', 'X', 'o', 'O'}
    complexity_per_instrument = {}
    total = 0
    count = 0

    for instrument, data in pattern['instruments'].items():
        line = data.get('steps', '')
        if not line:
            complexity = 0
        else:
            complexity = sum(1 for c in line if c in active_hits) / len(line)
        complexity_per_instrument[instrument] = complexity
        total += complexity
        count += 1

    overall_complexity = total / count if count > 0 else 0
    return overall_complexity, complexity_per_instrument
