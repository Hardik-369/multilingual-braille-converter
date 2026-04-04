from engine.mappings import (
    DEVANAGARI_VOWELS, DEVANAGARI_MATRAS, DEVANAGARI_CONSONANTS,
    DEVANAGARI_SIGNS, ENGLISH_LETTERS, DIGITS, NUMBER_SIGN, CAPITAL_SIGN, PUNCTUATION, CONJUNCTS
)

class BrailleTranslator:
    def __init__(self):
        pass

    def detect_script(self, char):
        """
        Detects if a character is Devanagari, English, Digit, or Other.
        """
        if '\u0900' <= char <= '\u097F':
            return 'devanagari'
        if char.lower() in ENGLISH_LETTERS:
            return 'english'
        if char in DIGITS:
            return 'digit'
        return 'other'

    def translate(self, text):
        """
        Translates text to Unicode Braille using Greedy Pattern Matching.
        Parsing Order: Conjunct -> Matra -> Consonant
        Special Rule: Skip Halant (noise character).
        """
        result = []
        i = 0
        in_number_mode = False

        # Sort conjuncts by length descending to match longest pattern first
        sorted_conjuncts = sorted(CONJUNCTS.keys(), key=len, reverse=True)

        while i < len(text):
            char = text[i]
            
            # Step 1: Check for Conjuncts (Greedy Match)
            matched_conjunct = False
            for conj in sorted_conjuncts:
                if text.startswith(conj, i):
                    result.append(CONJUNCTS[conj])
                    i += len(conj)
                    matched_conjunct = True
                    break
            
            if matched_conjunct:
                in_number_mode = False
                continue

            script = self.detect_script(char)

            # Step 2: Handle Noise (Halant)
            if char == '्':
                # Skip halant per user request
                i += 1
                continue

            # Step 3: Handle Number Mode
            if script == 'digit':
                if not in_number_mode:
                    result.append(NUMBER_SIGN)
                    in_number_mode = True
                result.append(DIGITS[char])
                i += 1
                continue
            else:
                in_number_mode = False

            # Step 4: Handle Devanagari (Matras and Consonants)
            if script == 'devanagari':
                # Check for Nukta rule: (prefix dot 5)
                if i + 1 < len(text) and text[i+1] == '़':
                    result.append(DEVANAGARI_SIGNS['़'])
                    if char in DEVANAGARI_CONSONANTS:
                        result.append(DEVANAGARI_CONSONANTS[char])
                    i += 2
                    continue

                if char in DEVANAGARI_MATRAS:
                    result.append(DEVANAGARI_MATRAS[char])
                elif char in DEVANAGARI_VOWELS:
                    result.append(DEVANAGARI_VOWELS[char])
                elif char in DEVANAGARI_CONSONANTS:
                    result.append(DEVANAGARI_CONSONANTS[char])
                elif char in DEVANAGARI_SIGNS:
                    result.append(DEVANAGARI_SIGNS[char])
                i += 1
            
            # Step 5: Handle English
            elif script == 'english':
                if char.isupper():
                    result.append(CAPITAL_SIGN)
                result.append(ENGLISH_LETTERS[char.lower()])
                i += 1
            
            # Step 6: Handle Punctuation/Space
            else:
                if char in PUNCTUATION:
                    result.append(PUNCTUATION[char])
                elif char == '\n':
                    result.append('\n')
                i += 1

        return "".join(result)
