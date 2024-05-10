def format_value(v):
    """
    Receives a value and returns it formatted
    in dots and coma (1.000.000,00).
    """
    return f'{v:_.2f}'.replace('.', ',').replace('_', '.')
