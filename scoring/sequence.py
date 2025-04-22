# REMINDER : 
# 'A0' is the mandatory BLANK pattern (with no notes), to be used to end score and avoid TF 
# 'A1' means a single pattern play 
# 'A1x3' means pattern multiplier,
# '+1' or '-3' means +0.1 or minus 0.3 to TF (never to be at the end of the score, always use A0 after the last) 
# 'stoch(0.3)', 'rand(0.5)', mode_name(param) ... are MODES changes : name + param

#pattern_sequence = ['W1', 'W1'] # used with 6/8 
# main_sequence = ['A0', '+2', 'A0','+2','A0', '+2','A0', '+2', 'A0', '-8'] # used with test pattern
# main_sequence = ['A2', 'A2'] # simple loop of 2x4 mes

# basic pattern with constant TF raise & decay 
# main_sequence = ['A1', '+2', 'A1', '+2', 'A1', '+2', 'A1' ,'+2', 'A1', '-2', 'A1', '-2', 'A1' ,'-2', 'A1', '-4'] # used with test pattern

# main sequence with TF changes 
# main_sequence = ['A1', '+2', 'A1','+2','A1', '-6','F1', '+2'] # used with test pattern

# main sequence WITHOUT TF changes 
# main_sequence = ['A1', '+0', 'A1','+0','A1', '+0','F1', '-0'] # used with test pattern

# with progressive moves
# main_sequence = ['A1x2', '+9', 'A1x2', '-6', 'A1x2' , '-3' , 'A0'] # used with test pattern

#   TF value :            -3            +3            0               +3            0              +3
# main_sequence = ['A1x2', '-3', 'A1x2', '+6', 'A1x2' , '-3', 'A1x2' , '+3', 'A1x2', '-3', 'A1x2' , '+3', 'A1x2' ] # used with test pattern

# strong moves 
# main_sequence = ['A1x2', '+9', 'A1x2', '-9', '-9' , 'A1x2' , '+9', 'A1x2'] # used with test pattern

# play all pattern sequence of one type 
# main_sequence = ['A3x4','A4x4','A5x4','A6x4','A7x4', 'A8x4','A9x4','A10x4'] # simple loop of 2x4 mes
# main_sequence = ['B1x4','B2x4','B3x4','B4x4','B5x4', 'B6x4','B7x4','B8x4','B9x4','B10x4']

# exemple with mode changes 
#main_sequence = ['stoch(0.4)', 'B5' , 'rand(0.7)', '+1' , 'rules(0.9)', 'A0']
#main_sequence = ['stoch(0.4)', '+7' , 'A1' , '-7' , 'A0']
main_sequence = [ 'A1' ]