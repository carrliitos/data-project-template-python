import re

def extract_last_word(input_string):
    """
    Extracts the last word from the input string.

    Args:
    - input_string (str): The input string from which to extract the last word.

    Returns:
    - str or None: The last word from the input string, or None if no word is found.

    Example:
    >>> extract_last_word("C:\\Users\\benzon.salazar\\Documents\\Projects\\Routines\\routine_daily\\venv")
    'venv'
    >>> extract_last_word("C:\\Users\\benzon.salazar\\Documents\\Projects\\Routines\\routine_daily")
    'routine_daily'
    """
    match = re.search(r'\b(\w+)\b$', input_string)
    if match:
        return match.group(1)
    return None
