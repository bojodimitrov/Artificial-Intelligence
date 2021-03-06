"""
Returns patterns
"""

def get_symbol(number):
    """
    Returns symbol mapped to a number
    """
    symbols = ['\\', '/', '-', '|', ':', 'O', '*', '"']
    return symbols[number]


def get_pattern(symbol):
    """
    Returns patterns as matrixes
    """
    patterns = {
        '\\': ([1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1], [0, 0, 0]),
        '/': ([0, 0, 0, 1,
               0, 0, 1, 0,
               0, 1, 0, 0,
               1, 0, 0, 0], [0, 0, 1]),
        '-': ([0, 0, 0, 0,
               1, 1, 1, 1,
               0, 0, 0, 0,
               0, 0, 0, 0], [0, 1, 0]),
        '|': ([0, 1, 0, 0,
               0, 1, 0, 0,
               0, 1, 0, 0,
               0, 1, 0, 0], [0, 1, 1]),
        ':': ([0, 1, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 1, 0, 0], [1, 0, 0]),
        'O': ([0, 1, 1, 0,
               1, 0, 0, 1,
               1, 0, 0, 1,
               0, 1, 1, 0], [1, 0, 1]),
        '*': ([1, 0, 0, 1,
               0, 1, 1, 0,
               0, 1, 1, 0,
               1, 0, 0, 1], [1, 1, 0]),
        '"': ([0, 1, 1, 0,
               0, 1, 1, 0,
               0, 1, 1, 0,
               0, 0, 0, 0], [1, 1, 1])
    }
    return patterns[symbol]
