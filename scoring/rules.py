# Adjusted Rules with simplified behavior at TF 0.1

rules = {
    'complexify': {
        'mild': {
            'general': [
                 ("X---------------", "X-------X-------"),  # Kick to double hit
            ],
            'instrument_specific': {
                'BD': [
                ],
            }
        },
        'medium': {
            'general': [

            ],
            'instrument_specific': {
                'BD': [
                    ("X-------X-------", "X-------X---X---")
                ],
                'SD': [

                ],
                'HH': [

                ]
            }
        },
        'strong': {
            'general': [
            ],
            'instrument_specific': {
                'BD': [
                    ("X-------X---X---", "X---X---X---X---")
                ],
                'SD': [

                ],
                'HH': [

                ]
            }
        }
    },

    'simplify': {
        'mild': {
            'general': [

            ],
            'instrument_specific': {
                'BD': [

                ],
                'SD': [

                ],
                'HH': [

                ]
            }
        },
        'medium': {
            'general': [

            ],
            'instrument_specific': {
                'BD': [

                ],
                'SD': [

                ],
                'HH': [

                ]
            }
        },
        'strong': {
            'general': [

            ],
            'instrument_specific': {
                'BD': [

                ],
                'SD': [

                ],
                'HH': [

                ]
            }
        }
    }
}
