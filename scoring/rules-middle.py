rules = {
    'complexify': {
        'general': [
            ("---", "-x-"),  # Introduce a hit inside a silent segment
            ("-x-", "x-x"),  # Add an offbeat hit
            ("x-x", "X-x"),  # Accentuate one hit
            ("-O-", "O-O"),  # Duplicate an alternate sound
            ("x-", "xo"),  # Introduce an alternate hit
            ("-x", "xX"),  # Add an accent
            ("-O", "oO"),  # Make alternate hit more dynamic
            ("O-", "O-x"),  # Slightly fill the space
            ("xO", "XO"),  # Strengthen alternating patterns
            ("--X--", "-xX-")  # Introduce a ghost note
        ],
        'instrument_specific': {
            'BD': [
                ("---", "-x-"),  # Add a soft kick
                ("-x-", "X--"),  # Make it more dynamic
                ("-X", "XX"),  # Double strong kicks occasionally
                ("x-", "xo"),  # Introduce variation
                ("O-", "O-X")  # Accent the alternate kick
            ],
            'SD': [
                ("-x-", "x-x"),  # Create a ghost note
                ("x-x", "X-x"),  # Add an accent
                ("--X--", "-xX-"),  # Introduce subtle groove
                ("O-", "O-x"),  # Make alt hits more rhythmic
                ("xO", "XO")  # Strengthen alternating feel
            ],
            'HH': [
                ("x-x", "X-x"),  # Accentuate groove
                ("-O-", "O-O"),  # Open hi-hat more often
                ("O-", "O-x"),  # Subtle shift in articulation
                ("x-", "xo"),  # Add open hi-hat texture
                ("xO", "XO")  # Reinforce dynamics
            ]
        }
    },
    'simplify': {
        'general': [
            ("X-x", "x-x"),  # Reduce accents
            ("x-x", "x--"),  # Remove offbeat hits
            ("O-O", "-O-"),  # Make alt hits less frequent
            ("XO", "xO"),  # Reduce strong articulation
            ("oO", "-O"),  # Subtle simplification
            ("X-X", "X--"),  # Space out strong notes
            ("-xX-", "--X--"),  # Remove light hits
            ("O-x", "O--"),  # Reduce busy fills
            ("xO", "x-"),  # Decrease alternation
            ("X-", "x-")  # Lower accent strength
        ],
        'instrument_specific': {
            'BD': [
                ("X--", "x--"),  # Reduce strong kicks
                ("XX", "X-"),  # Simplify double kicks
                ("-x-", "---"),  # Create breathing room
                ("O-X", "O-"),  # Keep alternates subtle
                ("xo", "x-")  # Remove variations
            ],
            'SD': [
                ("X-x", "x-x"),  # Reduce accents
                ("x-x", "x--"),  # Simplify ghost notes
                ("-xX-", "--X--"),  # Space out hits
                ("O-x", "O--"),  # Less busy alternate hits
                ("XO", "xO")  # Smooth out dynamics
            ],
            'HH': [
                ("X-x", "x-x"),  # Reduce intensity
                ("O-O", "-O-"),  # Make open hits less frequent
                ("O-x", "O--"),  # Reduce busy articulations
                ("xo", "x-") , # Remove unnecessary variations
                ("XO", "xO")  # Tone down accents
            ]
        }
    }
}
