import argparse
import sys
import os
from engine.translator import BrailleTranslator
from io_handlers.input_handler import InputHandler
from io_handlers.output_handler import OutputHandler

def main():
    parser = argparse.ArgumentParser(description="Rule-Based Multilingual Braille Converter (Marathi, Hindi, English)")
    parser.add_argument("input", help="Text input or path to a PDF file")
    parser.add_argument("--output_pdf", help="Path to save the generated Braille PDF", default="braille_output.pdf")
    parser.add_argument("--output_txt", help="Path to save the Unicode Braille text", default="braille_output.txt")
    parser.add_argument("--output_docx", help="Path to save the Word document", default="braille_output.docx")
    parser.add_argument("--ocr", action="store_true", help="Attempt OCR if text extraction fails for PDF")

    args = parser.parse_args()

    # Step 1: Handle Input
    if os.path.exists(args.input):
        print(f"Reading file: {args.input}")
        input_text = InputHandler.read_file(args.input)
    else:
        # Treat as raw text input
        input_text = args.input

    if not input_text:
        print("Error: No input text or empty file.")
        sys.exit(1)

    print(f"Input text extracted (Length: {len(input_text)} chars).")

    # Step 2: Translation
    translator = BrailleTranslator()
    print("Translating to Braille...")
    braille_result = translator.translate(input_text)
    
    # Step 3: Handle Output
    output_handler = OutputHandler()
    
    # Save as Unicode text
    output_handler.save_unicode_text(braille_result, args.output_txt)
    print(f"Unicode Braille saved to: {args.output_txt}")

    # Generate PDF
    print(f"Generating Braille PDF: {args.output_pdf}...")
    output_handler.generate_braille_pdf(braille_result, args.output_pdf)
    
    # Generate DOCX
    print(f"Generating Word Document: {args.output_docx}...")
    output_handler.generate_docx(braille_result, args.output_docx)
    print("Process complete!")

if __name__ == "__main__":
    main()
