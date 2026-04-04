import pdfplumber
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

class InputHandler:
    @staticmethod
    def extract_text_from_pdf(file_path):
        """
        Extracts searchable text from a PDF file using pdfplumber.
        """
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
            return ""

    @staticmethod
    def ocr_pdf(file_path, language='hin+mar+eng'):
        """
        Extracts text from a (scanned) PDF using OCR.
        Requires Tesseract OCR and pdf2image or similar.
        Note: Simplest way is to convert pages to images first.
        """
        # This is a simplified version (would need pdf2image)
        if not pytesseract:
            raise ImportError("pytesseract is not installed.")
        
        # In a real implementation, we would use pdf2image.
        # For now, we assume searchable PDF works or provide a stub.
        return f"[OCR Stub: Would process {file_path} with {language}]"

    @staticmethod
    def read_file(file_path):
        """
        Generic file reader (Text or PDF).
        """
        if file_path.lower().endswith('.pdf'):
            text = InputHandler.extract_text_from_pdf(file_path)
            if not text.strip():
                # Try OCR if no text found?
                return InputHandler.ocr_pdf(file_path)
            return text
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
