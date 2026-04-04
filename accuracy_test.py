import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(r'c:\Users\siddh\OneDrive\Desktop\Braillie Converter')

from engine.translator import BrailleTranslator

translator = BrailleTranslator()

# ─────────────────────────────────────────────────────────
# Ground-truth test cases based on official Bharati Braille
# standard (NIEPVD, Govt. of India)
# ─────────────────────────────────────────────────────────
# Format: (input, expected_output, category, description)
tests = [
    # ── ENGLISH: Grade 1 Letters ──────────────────────────
    ("abc",      "⠁⠃⠉",      "EN-Letters",    "Lowercase abc"),
    ("xyz",      "⠭⠽⠵",      "EN-Letters",    "Lowercase xyz"),
    ("Hello",    "⠠⠓⠑⠇⠇⠕",  "EN-Capital",    "Capitalised Hello"),
    ("INDIA",    "⠠⠊⠠⠝⠠⠙⠠⠊⠠⠁", "EN-Capital", "All-caps INDIA"),

    # ── ENGLISH: Numbers ──────────────────────────────────
    ("123",      "⠼⠁⠃⠉",     "EN-Numbers",    "Digits 123"),
    ("456",      "⠼⠙⠑⠋",     "EN-Numbers",    "Digits 456"),
    ("2024",     "⠼⠃⠚⠃⠙",    "EN-Numbers",    "Year 2024"),

    # ── DEVANAGARI: Simple Vowels ─────────────────────────
    ("अ",        "⠁",        "DEV-Vowels",     "Vowel A"),
    ("आ",       "⠜",        "DEV-Vowels",     "Vowel AA"),
    ("इ",        "⠊",        "DEV-Vowels",     "Vowel I"),
    ("उ",        "⠥",        "DEV-Vowels",     "Vowel U"),
    ("ए",       "⠑",        "DEV-Vowels",     "Vowel E"),

    # ── DEVANAGARI: Simple Consonants ────────────────────
    ("क",        "⠅",        "DEV-Consonants", "Ka"),
    ("ख",       "⠨",        "DEV-Consonants", "Kha"),
    ("ग",        "⠛",        "DEV-Consonants", "Ga"),
    ("न",        "⠝",        "DEV-Consonants", "Na"),
    ("म",        "⠍",        "DEV-Consonants", "Ma"),
    ("र",        "⠗",        "DEV-Consonants", "Ra"),
    ("स",        "⠎",        "DEV-Consonants", "Sa"),

    # ── DEVANAGARI: Consonant + Matra ─────────────────────
    ("कि",      "⠅⠊",       "DEV-Matra",     "Ka + i matra"),
    ("की",      "⠅⠔",       "DEV-Matra",     "Ka + ii matra"),
    ("कु",      "⠅⠥",       "DEV-Matra",     "Ka + u matra"),
    ("के",      "⠅⠑",       "DEV-Matra",     "Ka + e matra"),
    ("का",      "⠅⠜",       "DEV-Matra",     "Ka + aa matra"),

    # ── DEVANAGARI: Signs ─────────────────────────────────
    ("संगम",    "⠎⠰⠛⠍",     "DEV-Signs",     "Anusvara (ं)"),
    ("नमः",     "⠝⠍⠣",      "DEV-Signs",     "Visarga (ः)"),

    # ── DEVANAGARI: Conjuncts (Rule-Based) ───────────────
    ("त्र",     "⠞⠗",       "DEV-Conjunct",  "Conjunct tra"),
    ("ज्ञ",     "⠚⠒",       "DEV-Conjunct",  "Conjunct jna"),

    # ── DEVANAGARI: Full Words ────────────────────────────
    ("नमस्ते",  "⠝⠍⠎⠞⠑",   "Words",         "Namaste"),
    ("भारत",    "⠘⠜⠗⠞",     "Words",         "Bharat"),
    ("हिंदी",   "⠓⠊⠰⠙⠔",   "Words",         "Hindi"),
    ("महाराष्ट्र", "⠍⠓⠜⠗⠜⠯⠞⠗", "Words",    "Maharashtra"),

    # ── PUNCTUATION ───────────────────────────────────────
    ("hello.",   "⠓⠑⠇⠇⠕⠲",  "Punctuation",   "English with period"),
    ("क्या?",   "⠅⠽⠢",      "Punctuation",   "Hindi with question mark"),

    # ── MULTILINGUAL ─────────────────────────────────────
    ("India भारत", "⠠⠊⠝⠙⠊⠁ ⠘⠜⠗⠞", "Mixed", "Mixed English-Hindi"),
]

# ─────────────────────────────────────────────────────────
# Run tests and compute accuracy
# ─────────────────────────────────────────────────────────
results = {}
pass_count = 0
fail_count = 0
total = len(tests)

for input_text, expected, category, desc in tests:
    got = translator.translate(input_text)
    passed = got == expected
    if passed:
        pass_count += 1
    else:
        fail_count += 1

    if category not in results:
        results[category] = {"pass": 0, "fail": 0, "cases": []}
    results[category]["pass" if passed else "fail"] += 1
    results[category]["cases"].append({
        "desc": desc, "input": input_text,
        "expected": expected, "got": got, "passed": passed
    })

# ─────────────────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────────────────
print("=" * 70)
print("  BRAILLE CONVERTER — ACCURACY REPORT")
print("=" * 70)
print(f"  Total Tests : {total}")
print(f"  Passed      : {pass_count}")
print(f"  Failed      : {fail_count}")
print(f"  Accuracy    : {pass_count/total*100:.1f}%")
print("=" * 70)

for cat, data in results.items():
    cat_total = data["pass"] + data["fail"]
    cat_acc = data["pass"] / cat_total * 100
    status = "✅" if cat_acc == 100 else ("⚠️" if cat_acc >= 50 else "❌")
    print(f"\n{status}  {cat:20s}  {data['pass']}/{cat_total}  ({cat_acc:.0f}%)")
    for c in data["cases"]:
        marker = "  ✓" if c["passed"] else "  ✗"
        if not c["passed"]:
            print(f"    {marker} [{c['desc']}]")
            print(f"         Input    : {c['input']}")
            print(f"         Expected : {c['expected']}")
            print(f"         Got      : {c['got']}")

print("\n" + "=" * 70)
