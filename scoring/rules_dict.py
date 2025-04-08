rules = {
    'complexify': {
        'mild': {
            'general': [
                ("X-------X-------", "X---X---X---X---"),  # Kick to double hit
            ],
        },
        'medium': {
            'general': [
                ("X---X---X---X---", "X---X-o-X---X-o-"),
            ],
        },
        'strong': {
            'general': [
                ("X---X-o-X---X-o-", "X-x-X-x-X-x-X-x-"),
            ],
        }
    },

    'simplify': {
        'mild': {
            'general': [
                ("X---X---X---X---", "X-------X-------"),  # Double hit to single hit
            ],
        },
        'medium': {
            'general': [
                ("X---X-x-X---X-x-", "X---X---X---X---"),  # Complexity reduced by removing some hits
            ],
        },
        'strong': {
            'general': [
                ("X-x-X-x-X-x-X-x-", "X-------X-------"),  # Remove more hits for strong simplification
            ],
        }
    }
}
