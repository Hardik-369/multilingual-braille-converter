<div align="center">

```
⠃⠗⠁⠊⠇⠇⠑   ⠉⠕⠝⠧⠑⠗⠞⠑⠗
```

# ⠃ Multilingual Braille Converter

### *A production-grade, rule-based Braille conversion engine for Marathi, Hindi, and English — built without Liblouis.*

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Standard](https://img.shields.io/badge/Standard-Bharati%20Braille%20(NIEPVD)-4A90D9?style=for-the-badge)](https://niepvd.nic.in/)
[![Accuracy](https://img.shields.io/badge/Accuracy-94.3%25-2ea44f?style=for-the-badge)](#-accuracy-benchmark)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

<br>

> **"Making information accessible is not a feature — it is a right."**
>
> This engine converts text and scanned documents into tactile-ready **Unicode Braille** and exports to **PDF** and **Microsoft Word** — all powered by a handcrafted, zero-dependency rule engine compliant with the *Standard Bharati Braille Code* (Government of India, NIEPVD).

<br>

---

</div>

## 📌 Table of Contents

1. [Why This Project?](#-why-this-project)
2. [Features at a Glance](#-features-at-a-glance)
3. [Live Demo (Streamlit)](#-live-demo-streamlit)
4. [System Architecture](#-system-architecture)
5. [Project Structure](#-project-structure)
6. [Braille Rules Implemented](#-braille-rules-implemented)
7. [Accuracy Benchmark](#-accuracy-benchmark)
8. [Installation](#-installation)
9. [Usage](#-usage)
10. [API Reference](#-api-reference)
11. [Supported Characters](#-supported-characters)
12. [Roadmap](#-roadmap)
13. [Contributing](#-contributing)
14. [License](#-license)

---

## 🧠 Why This Project?

Over **40 million** people in India live with visual impairments. Despite Braille being the primary literacy medium for this population, **99% of digital content** is inaccessible to them.

Existing tools either:
- Rely on **Liblouis** (a black-box, hard-to-extend Western library), or
- Support only single-language documents

This project takes a different approach:

| Approach | Liblouis-based tools | **This Engine** |
|---|---|---|
| Dependency | External binary | Zero — pure Python |
| Language Support | English-first | Marathi, Hindi, English |
| Halant/Conjunct handling | Table-driven | Transparent rule code |
| Output formats | PDF only | **TXT + PDF + DOCX** |
| Customisable | No | ✅ Fully open |
| Accuracy | ~96% | **94.3% (rule-only)** |

---

## ✨ Features at a Glance

<table>
<tr>
<td width="50%">

### 🔤 Language Support
- **Hindi** (Devanagari) — full vowel/consonant grid
- **Marathi** — including ळ, conjuncts like ष्ट्र
- **English** — Grade 1, capitalisation sign
- **Mixed** documents — script switches at character level

</td>
<td width="50%">

### ⠿ Braille Engine
- All 11 Devanagari vowels
- 35 consonants + special forms (क्ष, ज्ञ)
- Matras (vowel signs) as independent cells
- Anusvara (ं), Visarga (ः), Chandrabindu (ँ), Nukta (़)
- Danda (।) and Double Danda (॥)

</td>
</tr>
<tr>
<td>

### 📥 Input Flexibility
- Direct text entry (any Unicode)
- Digital PDF extraction (`pdfplumber`)
- Scanned PDF via OCR stub (`pytesseract`)
- Plain `.txt` file upload

</td>
<td>

### 📤 Export Formats
- **Unicode Braille** `.txt` — copy/paste or emboss
- **Tactile PDF** — dots rendered as physical circles
- **Microsoft Word** `.docx` — with Segoe UI Symbol font

</td>
</tr>
</table>

---

## 🖥️ Live Demo (Streamlit)

```bash
streamlit run app.py
```

The web interface opens at `http://localhost:8501`.

| Feature | Description |
|---|---|
| **Live Translation** | Braille updates in real-time as you type |
| **Stats Bar** | Shows input character count, Braille cell count, word count |
| **File Upload** | Drag-and-drop PDF or TXT — text extracted automatically |
| **One-click Export** | Download `.txt`, `.pdf`, or `.docx` with a single click |
| **Dark Mode UI** | Premium glassmorphism aesthetic with gradient typography |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MULTILINGUAL BRAILLE CONVERTER                   │
│                     ─────────────────────────────                    │
│                                                                       │
│   📥 INPUT LAYER                                                      │
│   ┌──────────────┐    ┌──────────────┐    ┌───────────────┐          │
│   │  Text Input  │    │  PDF (Text)  │    │  PDF (Scan)   │          │
│   │  (Any Lang)  │    │  pdfplumber  │    │  pytesseract  │          │
│   └──────┬───────┘    └──────┬───────┘    └──────┬────────┘          │
│          └──────────────────┬┘                   │                   │
│                             ▼                    │                   │
│                    ┌────────────────┐            │                   │
│                    │ Raw Unicode    │◄───────────┘                   │
│                    │ Text Stream    │                                 │
│                    └───────┬────────┘                                 │
│                            │                                          │
│   ⚙️  ENGINE LAYER          │                                          │
│   ┌────────────────────────▼──────────────────────────┐              │
│   │               BrailleTranslator                    │              │
│   │  ┌─────────────────────────────────────────────┐  │              │
│   │  │  Script Detector (Unicode range U+0900–097F)│  │              │
│   │  └────────────┬────────────────────────────────┘  │              │
│   │               │                                    │              │
│   │  ┌────────────▼────────────┐  ┌────────────────┐  │              │
│   │  │  Devanagari Processor   │  │English Processor│  │              │
│   │  │  • Greedy conjunct scan │  │  • Grade 1     │  │              │
│   │  │  • Matra → cell append  │  │  • Capital Sign│  │              │
│   │  │  • Skip halant noise    │  │  • Number Sign │  │              │
│   │  │  • Anusvara / Visarga   │  └────────────────┘  │              │
│   │  └─────────────────────────┘                       │              │
│   └────────────────────────┬──────────────────────────┘              │
│                             │                                          │
│   📦 MAPPINGS LAYER         │                                          │
│   ┌─────────────────────────▼──────────────────────────┐             │
│   │  mappings.py  —  All dot patterns (hand-coded)      │             │
│   │  • DEVANAGARI_VOWELS   • DEVANAGARI_CONSONANTS     │             │
│   │  • DEVANAGARI_MATRAS   • DEVANAGARI_SIGNS          │             │
│   │  • ENGLISH_LETTERS     • DIGITS                    │             │
│   │  • CONJUNCTS           • PUNCTUATION               │             │
│   └─────────────────────────┬──────────────────────────┘             │
│                             │                                          │
│   📤 OUTPUT LAYER           ▼                                          │
│   ┌──────────────┐   ┌──────────────┐   ┌─────────────────┐          │
│   │ Unicode .txt │   │ PDF (dots)   │   │ Word (.docx)    │          │
│   │ UTF-8 export │   │ ReportLab    │   │ python-docx     │          │
│   └──────────────┘   └──────────────┘   └─────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
braille-converter/
│
├── 📄 app.py                    # Streamlit web application
├── 📄 main.py                   # CLI entry point
├── 📄 accuracy_test.py          # 35-case ground-truth accuracy suite
├── 📄 test_converter.py         # Quick smoke tests
│
├── 📁 engine/                   # Core translation engine
│   ├── 📄 __init__.py
│   ├── 📄 mappings.py           # All Braille dot-pattern dictionaries
│   └── 📄 translator.py         # Script detection + rule application
│
├── 📁 io_handlers/              # I/O abstraction layer
│   ├── 📄 __init__.py
│   ├── 📄 input_handler.py      # PDF & text file reading
│   └── 📄 output_handler.py     # PDF, DOCX, TXT generation
│
└── 📄 README.md
```

---

## 📚 Braille Rules Implemented

### 1. Script Detection
Character-level Unicode range checks — no language model required.

```python
if '\u0900' <= char <= '\u097F':  # → Devanagari
elif char.lower() in ENGLISH_LETTERS:  # → English
elif char in DIGITS:  # → Numeric
```

### 2. Parsing Priority (Greedy by Length)

```
Conjunct (longest match first) → Matra → Vowel → Consonant → Sign
```

This prevents partial matches — `ष्ट्र` (4 Unicode codepoints) is matched before `ष` alone.

### 3. Halant (`्`) Handling

Per Bharati Braille standard, the halant is used only as a conjunct separator in print. In Braille, it is converted to **no output** (skipped) when already absorbed by a conjunct rule.

```python
if char == '्':
    i += 1  # Skip — absorbed or noise
    continue
```

### 4. Conjunct Rules

These specific sequences are mapped to contracted Braille forms:

| Devanagari | Unicode Sequence | Braille | Dot Pattern |
|---|---|---|---|
| ष्ट्र | `\u0937\u094D\u091F\u094D\u0930` | ⠯⠞⠗ | `ष + ट + र` |
| त्र | `\u0924\u094D\u0930` | ⠞⠗ | `त + र` |
| ज्ञ | `\u091C\u094D\u091E` | ⠚⠒ | `ज + colon` |
| क्ष | `\u0915\u094D\u0937` | direct cell | standard |

### 5. Matra Linearisation

Unlike print Devanagari where matras are diacritics *attached* to consonants, Bharati Braille linearises them as **independent cells appearing after the consonant**:

```
Print:   क  +  ि  (ki — matra above/before)
Braille: ⠅ ⠊    (sequential cells)
```

### 6. Capitalisation (English Grade 1)

```
Uppercase letter → prefix CAPITAL_SIGN (dot 6, ⠠) + letter cell
```

### 7. Number Mode

```
First digit → prefix NUMBER_SIGN (dots 3-4-5-6, ⠼) + digit cells
```

---

## 🎯 Accuracy Benchmark

Tested against **35 ground-truth cases** derived from the official *Standard Bharati Braille Codes* (NIEPVD, Government of India).

```
══════════════════════════════════════════════════════════════════════
  BRAILLE CONVERTER — ACCURACY REPORT
══════════════════════════════════════════════════════════════════════
  Total Tests : 35
  Passed      : 33
  Failed      : 2
  Accuracy    : 94.3%
══════════════════════════════════════════════════════════════════════

  ✅  English Letters       2/2   (100%)
  ✅  English Capitalisation  2/2   (100%)
  ✅  English Numbers       3/3   (100%)
  ✅  Devanagari Vowels     5/5   (100%)
  ✅  Devanagari Consonants 7/7   (100%)
  ✅  Matras (vowel signs)  5/5   (100%)
  ✅  Conjuncts (ष्ट्र, त्र, ज्ञ)  2/2  (100%)
  ✅  Full Words            4/4   (100%)
  ✅  Multilingual Mixed    1/1   (100%)
  ⚠️  DEV Signs             1/2   (50%)   — Visarga dot fix in progress
  ⚠️  Punctuation           1/2   (50%)   — Hindi ? edge case
══════════════════════════════════════════════════════════════════════
```

> Run the benchmark yourself:
> ```bash
> python accuracy_test.py
> ```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multilingual-braille-converter.git
cd multilingual-braille-converter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```
streamlit
pdfplumber
reportlab
python-docx
pytesseract
pillow
```

### 3. (Optional) Install Tesseract for OCR

For scanned PDFs, install Tesseract with Devanagari language data:

- **Windows**: [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) → select `hin` and `mar` language packs
- **Ubuntu**: `sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar`
- **macOS**: `brew install tesseract`

---

## 🚀 Usage

### Web Application (Recommended)

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

**Workflow:**
1. Choose **Manual Text** or **Upload PDF / TXT**
2. Type or upload your content
3. See live Unicode Braille output + character stats
4. Download as `.txt`, `.pdf`, or `.docx`

---

### Command Line Interface

```bash
# Convert a string
python main.py "महाराष्ट्र त्र ज्ञ"

# Convert a PDF
python main.py my_document.pdf

# Specify custom output paths
python main.py my_document.pdf \
  --output_txt  my_braille.txt   \
  --output_pdf  my_braille.pdf   \
  --output_docx my_braille.docx
```

---

### Python API

```python
from engine.translator import BrailleTranslator
from io_handlers.output_handler import OutputHandler

translator = BrailleTranslator()
handler    = OutputHandler()

# Translate any text (multilingual)
braille = translator.translate("Hello हिंदी 2024")
print(braille)  # → ⠠⠓⠑⠇⠇⠕ ⠓⠊⠰⠙⠔ ⠼⠃⠚⠃⠙

# Export to Word
handler.generate_docx(braille, "output.docx")

# Export to Braille PDF
handler.generate_braille_pdf(braille, "output.pdf")
```

---

## 📖 API Reference

### `BrailleTranslator`

```python
class BrailleTranslator:
    def translate(text: str) -> str
        """Converts multilingual text to Unicode Braille string."""

    def detect_script(char: str) -> Literal['devanagari', 'english', 'digit', 'other']
        """Returns the script of a single character."""
```

### `OutputHandler`

```python
class OutputHandler:
    def generate_braille_pdf(braille_text: str, output_path: str) -> None
        """Renders Braille dots as circles in a PDF page."""

    def generate_docx(braille_text: str, output_path: str) -> None
        """Creates a Word document with Unicode Braille and Segoe UI Symbol font."""

    def save_unicode_text(braille_text: str, output_path: str) -> None
        """Saves raw Unicode Braille to a UTF-8 text file."""
```

### `InputHandler`

```python
class InputHandler:
    @staticmethod
    def read_file(file_path: str) -> str
        """Auto-detects PDF or TXT and returns extracted text."""

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str
        """Extracts searchable text using pdfplumber."""

    @staticmethod
    def ocr_pdf(file_path: str, language: str = 'hin+mar+eng') -> str
        """OCR fallback for scanned PDFs via pytesseract."""
```

---

## 🗂️ Supported Characters

<details>
<summary><strong>Devanagari Vowels (11)</strong></summary>

| Character | Name | Braille |
|---|---|---|
| अ | A | ⠁ |
| आ | AA | ⠜ |
| इ | I | ⠊ |
| ई | II | ⠔ |
| उ | U | ⠥ |
| ऊ | UU | ⠳ |
| ऋ | RI | ⠻ |
| ए | E | ⠑ |
| ऐ | AI | ⠌ |
| ओ | O | ⠕ |
| औ | AU | ⠪ |

</details>

<details>
<summary><strong>Devanagari Consonants (35)</strong></summary>

All standard consonants including क, ख, ग, घ, ङ, च, छ, ज, झ, ञ, ट, ठ, ड, ढ, ण, त, थ, द, ध, न, प, फ, ब, भ, म, य, र, ल, व, श, ष, स, ह, ळ and compound forms क्ष, ज्ञ.

</details>

<details>
<summary><strong>English (Grade 1)</strong></summary>

All 26 letters (a–z), uppercase with capital sign prefix (⠠), digits 0–9 with number sign prefix (⠼).

</details>

<details>
<summary><strong>Special Signs</strong></summary>

| Character | Description | Braille |
|---|---|---|
| ं | Anusvara | ⠰ |
| ः | Visarga | ⠣ |
| ँ | Chandrabindu | ⠄ |
| ़ | Nukta | ⠐ |
| । | Danda | ⠲ |
| ॥ | Double Danda | ⠲⠲ |

</details>

---

## 🛣️ Roadmap

- [x] Rule-based Bharati Braille engine (Marathi, Hindi, English)
- [x] Greedy conjunct matching with explicit conjunct dictionary
- [x] Halant noise suppression
- [x] Streamlit web application with dark-mode UI
- [x] PDF, DOCX, TXT export
- [x] 94.3% accuracy on 35-case benchmark
- [ ] Fix Visarga dot pattern edge case
- [ ] Hindi punctuation disambiguation (`?` after Devanagari)
- [ ] Grade 2 English contractions
- [ ] Punjabi (Gurmukhī) script support
- [ ] Tamil Braille support
- [ ] Embossable BRF (Braille Ready Format) export
- [ ] Reverse Braille → Text transcription
- [ ] REST API / FastAPI deployment

---

## 🤝 Contributing

Contributions are warmly welcomed — especially from accessibility researchers, Braille transcriptionists, and linguists.

```bash
git clone https://github.com/YOUR_USERNAME/multilingual-braille-converter.git
cd multilingual-braille-converter
pip install -r requirements.txt

# Create your feature branch
git checkout -b feat/punjabi-braille

# Run accuracy tests before submitting a PR
python accuracy_test.py
```

**Priority areas:**
- Adding new conjunct rules to `engine/mappings.py`
- Improving OCR pipeline for regional scripts
- Expanding the ground-truth accuracy test suite

Please open an **Issue** before submitting a large PR so we can discuss the approach.

---

## 🔬 Research References

1. *Standard Bharati Braille Codes with Unicode Mapping Chart* — NIEPVD, Ministry of Social Justice and Empowerment, Govt. of India
2. *Bharati Braille* — Wikipedia, [https://en.wikipedia.org/wiki/Bharati_Braille](https://en.wikipedia.org/wiki/Bharati_Braille)
3. *Devanagari Unicode Block* — Unicode Standard 15.0, U+0900–U+097F
4. *Grade 1 Braille* — Unified English Braille (UEB) Code Book, ICEB 2013

---

## 📜 License

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

**Built with ❤️ for 40 million visually impaired people across India**

*If this project helped you, please consider starring ⭐ the repository.*

```
⠃⠗⠁⠊⠇⠇⠑  ⠊⠎  ⠝⠕⠞  ⠁  ⠇⠁⠝⠛⠥⠁⠛⠑
⠊⠞  ⠊⠎  ⠁  ⠃⠗⠊⠙⠛⠑  ⠞⠕  ⠅⠝⠕⠺⠇⠑⠙⠛⠑
```
*(Braille is not a language. It is a bridge to knowledge.)*

</div>
