import sys
import os
import io

# Force UTF-8 for printing to console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add the project directory to sys.path
sys.path.append(r'c:\Users\siddh\OneDrive\Desktop\Braillie Converter')

from engine.translator import BrailleTranslator

def test_translation():
    translator = BrailleTranslator()
    
    test_cases = [
        ("abc", "English"),
        ("महाराष्ट्र", "Marathi"),
        ("हिंदी", "Hindi"),
        ("123", "Numbers"),
        ("नमस्ते", "Conjuncts"),
        ("Hello हिंदी 123", "Multilingual")
    ]
    
    for text, label in test_cases:
        braille = translator.translate(text)
        print(f"[{label}] '{text}' -> {braille}")

if __name__ == "__main__":
    test_translation()
