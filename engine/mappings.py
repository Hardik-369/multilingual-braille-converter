# Unicode Braille range: U+2800 to U+28FF

def dots_to_unicode(dots):
    """
    Converts dot numbers (e.g., [1, 2, 4]) to a Unicode Braille character.
    Dots are 1-indexed.
    """
    if not dots:
        return '⠀' # Empty cell U+2800
    res = 0
    for dot in dots:
        res += 1 << (dot - 1)
    return chr(0x2800 + res)

# DEVANAGARI MAPPINGS (Bharati Braille)
DEVANAGARI_VOWELS = {
    'अ': dots_to_unicode([1]),
    'आ': dots_to_unicode([3, 4, 5]),
    'इ': dots_to_unicode([2, 4]),
    'ई': dots_to_unicode([3, 5]),
    'उ': dots_to_unicode([1, 3, 6]),
    'ऊ': dots_to_unicode([1, 2, 5, 6]),
    'ऋ': dots_to_unicode([1, 2, 3, 5, 6]),
    'ए': dots_to_unicode([1, 5]),
    'ऐ': dots_to_unicode([3, 4]),
    'ओ': dots_to_unicode([1, 3, 5]),
    'औ': dots_to_unicode([2, 4, 6]),
}

DEVANAGARI_MATRAS = {
    'ा': dots_to_unicode([3, 4, 5]),
    'ि': dots_to_unicode([2, 4]),
    'ी': dots_to_unicode([3, 5]),
    'ु': dots_to_unicode([1, 3, 6]),
    'ू': dots_to_unicode([1, 2, 5, 6]),
    'ृ': dots_to_unicode([1, 2, 3, 5, 6]),
    'े': dots_to_unicode([1, 5]),
    'ै': dots_to_unicode([3, 4]),
    'ो': dots_to_unicode([1, 3, 5]),
    'ौ': dots_to_unicode([2, 4, 6]),
}

DEVANAGARI_CONSONANTS = {
    'क': dots_to_unicode([1, 3]),
    'ख': dots_to_unicode([4, 6]),
    'ग': dots_to_unicode([1, 2, 4, 5]),
    'घ': dots_to_unicode([1, 2, 6]),
    'ङ': dots_to_unicode([3, 4, 6]),
    'च': dots_to_unicode([1, 4]),
    'छ': dots_to_unicode([1, 6]),
    'ज': dots_to_unicode([2, 4, 5]),
    'झ': dots_to_unicode([3, 5, 6]),
    'ञ': dots_to_unicode([2, 5]),
    'ट': dots_to_unicode([2, 3, 4, 5, 6]),
    'ठ': dots_to_unicode([2, 4, 5, 6]),
    'ड': dots_to_unicode([1, 2, 4, 6]),
    'ढ': dots_to_unicode([1, 2, 3, 4, 5, 6]),
    'ण': dots_to_unicode([3, 4, 5, 6]),
    'त': dots_to_unicode([2, 3, 4, 5]),
    'थ': dots_to_unicode([1, 4, 5, 6]),
    'द': dots_to_unicode([1, 4, 5]),
    'ध': dots_to_unicode([2, 3, 4, 6]),
    'न': dots_to_unicode([1, 3, 4, 5]),
    'प': dots_to_unicode([1, 2, 3, 4]),
    'फ': dots_to_unicode([2, 3, 5]),
    'ब': dots_to_unicode([1, 2]),
    'भ': dots_to_unicode([4, 5]),
    'म': dots_to_unicode([1, 3, 4]),
    'य': dots_to_unicode([1, 3, 4, 5, 6]),
    'र': dots_to_unicode([1, 2, 3, 5]),
    'ल': dots_to_unicode([1, 2, 3]),
    'व': dots_to_unicode([1, 2, 3, 6]),
    'श': dots_to_unicode([1, 4, 6]),
    'ष': dots_to_unicode([1, 2, 3, 4, 6]),
    'स': dots_to_unicode([2, 3, 4]),
    'ह': dots_to_unicode([1, 2, 5]),
    'ळ': dots_to_unicode([4, 5, 6]),
    'क्ष': dots_to_unicode([1, 2, 3, 4, 5]),
    'ज्ञ': dots_to_unicode([1, 5, 6]),
}

DEVANAGARI_SIGNS = {
    'ँ': dots_to_unicode([3]),      # Chandrabindu
    'ं': dots_to_unicode([5, 6]),   # Anusvara
    'ः': dots_to_unicode([6]),      # Visarga
    '्': dots_to_unicode([4]),      # Halant
    '़': dots_to_unicode([5]),      # Nukta
    'ऽ': dots_to_unicode([2, 3]),   # Avagraha
}

# ENGLISH MAPPINGS (Grade 1)
ENGLISH_LETTERS = {
    'a': dots_to_unicode([1]),
    'b': dots_to_unicode([1, 2]),
    'c': dots_to_unicode([1, 4]),
    'd': dots_to_unicode([1, 4, 5]),
    'e': dots_to_unicode([1, 5]),
    'f': dots_to_unicode([1, 2, 4]),
    'g': dots_to_unicode([1, 2, 4, 5]),
    'h': dots_to_unicode([1, 2, 5]),
    'i': dots_to_unicode([2, 4]),
    'j': dots_to_unicode([2, 4, 5]),
    'k': dots_to_unicode([1, 3]),
    'l': dots_to_unicode([1, 2, 3]),
    'm': dots_to_unicode([1, 3, 4]),
    'n': dots_to_unicode([1, 3, 4, 5]),
    'o': dots_to_unicode([1, 3, 5]),
    'p': dots_to_unicode([1, 2, 3, 4]),
    'q': dots_to_unicode([1, 2, 3, 4, 5]),
    'r': dots_to_unicode([1, 2, 3, 5]),
    's': dots_to_unicode([2, 3, 4]),
    't': dots_to_unicode([2, 3, 4, 5]),
    'u': dots_to_unicode([1, 3, 6]),
    'v': dots_to_unicode([1, 2, 3, 6]),
    'w': dots_to_unicode([2, 4, 5, 6]),
    'x': dots_to_unicode([1, 3, 4, 6]),
    'y': dots_to_unicode([1, 3, 4, 5, 6]),
    'z': dots_to_unicode([1, 3, 5, 6]),
}

# COMMON SYMBOLS
NUMBER_SIGN = dots_to_unicode([3, 4, 5, 6])
CAPITAL_SIGN = dots_to_unicode([6])

PUNCTUATION = {
    '.': dots_to_unicode([2, 5, 6]),
    ',': dots_to_unicode([2]),
    ';': dots_to_unicode([2, 3]),
    ':': dots_to_unicode([2, 5]),
    '!': dots_to_unicode([2, 3, 5]),
    '?': dots_to_unicode([2, 3, 6]),
    '-': dots_to_unicode([3, 6]),
    '(': dots_to_unicode([2, 3, 5, 6]),
    ')': dots_to_unicode([2, 3, 5, 6]),
    '\"': dots_to_unicode([2, 3, 6]),
    '\'': dots_to_unicode([3]),
    '।': dots_to_unicode([2, 5, 6]), # Devanagari Danda
    '॥': dots_to_unicode([2, 5, 6]) + dots_to_unicode([2, 5, 6]), # Double Danda
    ' ': ' ',
}

# SPECIFIC CONJUNCTS (Greedy Priority)
# Matches Unicode sequences to manual Braille translations
CONJUNCTS = {
    "ष्ट्र": DEVANAGARI_CONSONANTS['ष'] + DEVANAGARI_CONSONANTS['त'] + DEVANAGARI_CONSONANTS['र'], # User requested ⠯⠞⠗ (ष + त + र)
    "त्र": DEVANAGARI_CONSONANTS['त'] + DEVANAGARI_CONSONANTS['र'], # User requested ⠞⠗ (त + र)
    "ज्ञ": DEVANAGARI_CONSONANTS['ज'] + dots_to_unicode([2, 5]), # User requested ⠚⠒ (ज + colon)
    "क्ष": DEVANAGARI_CONSONANTS['क्ष'], # Standard क्ष
}

DIGITS = {
    '1': dots_to_unicode([1]),
    '2': dots_to_unicode([1, 2]),
    '3': dots_to_unicode([1, 4]),
    '4': dots_to_unicode([1, 4, 5]),
    '5': dots_to_unicode([1, 5]),
    '6': dots_to_unicode([1, 2, 4]),
    '7': dots_to_unicode([1, 2, 4, 5]),
    '8': dots_to_unicode([1, 2, 5]),
    '9': dots_to_unicode([2, 4]),
    '0': dots_to_unicode([2, 4, 5]),
}
