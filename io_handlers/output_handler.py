from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
from docx import Document
from docx.shared import Pt

class OutputHandler:
    def __init__(self):
        # Configuration for Braille cell layout (in points)
        self.dot_radius = 1.0 # Standard size for tactile Braille
        self.dot_spacing_h = 4.5 # Horizontal spacing between dots in a cell
        self.dot_spacing_v = 4.5 # Vertical spacing between dots in a cell
        self.cell_spacing_h = 10.0 # Spacing between cells
        self.line_spacing_v = 15.0 # Spacing between lines
        self.margin = 50.0

    def generate_braille_pdf(self, braille_text, output_path):
        """
        Generates a PDF by drawing Braille dots for each cell.
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        
        x_start = self.margin
        y_start = height - self.margin
        x = x_start
        y = y_start

        for char in braille_text:
            if char == '\n':
                x = x_start
                y -= self.line_spacing_v
                if y < self.margin:
                    c.showPage()
                    y = height - self.margin
                continue
            
            if char == ' ':
                x += self.cell_spacing_h
                if x > width - self.margin:
                    x = x_start
                    y -= self.line_spacing_v
                continue

            # Convert Unicode Braille to internal cell representation
            if '\u2800' <= char <= '\u28FF':
                code = ord(char) - 0x2800
                self._draw_braille_cell(c, x, y, code)
                x += self.cell_spacing_h
                if x > width - self.margin:
                    x = x_start
                    y -= self.line_spacing_v
                    if y < self.margin:
                        c.showPage()
                        y = height - self.margin
            else:
                # For non-Braille characters (like periods/punctuations not converted),
                # we just skip or draw as a blank cell.
                x += self.cell_spacing_h
                
        c.save()

    def _draw_braille_cell(self, canvas_obj, x, y, code):
        """
        Draws the 6-dot Braille cell based on the code.
        Code bits: 1=dot1, 2=dot2, 4=dot3, 8=dot4, 16=dot5, 32=dot6
        Layout:
        (1) (4)
        (2) (5)
        (3) (6)
        """
        # Dot positions relative to (x, y) - y is the top of the cell
        dot_positions = [
            (0, 0),                       # Dot 1: Top-Left
            (0, -self.dot_spacing_v),     # Dot 2: Mid-Left
            (0, -2 * self.dot_spacing_v), # Dot 3: Bottom-Left
            (self.dot_spacing_h, 0),      # Dot 4: Top-Right
            (self.dot_spacing_h, -self.dot_spacing_v), # Dot 5: Mid-Right
            (self.dot_spacing_h, -2 * self.dot_spacing_v) # Dot 6: Bottom-Right
        ]

        # Draw dots if bit is set
        for i in range(6):
            if (code >> i) & 1:
                # Solid circle for raised dot
                canvas_obj.circle(x + dot_positions[i][0], y + dot_positions[i][1], self.dot_radius, fill=1)
            else:
                # Optional: draw empty circles or nothing
                # canvas_obj.circle(x + dot_positions[i][0], y + dot_positions[i][1], 0.5, fill=0)
                pass

    def save_unicode_text(self, braille_text, output_path):
        """
        Saves the Unicode Braille text to a file.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(braille_text)

    def generate_docx(self, braille_text, output_path):
        """
        Generates a Word document (.docx) with Unicode Braille characters.
        """
        doc = Document()
        # Set a font that is likely to support Unicode Braille (e.g., Segoe UI Symbol or DejaVu)
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Segoe UI Symbol' # Common on Windows
        font.size = Pt(14)
        
        # Add text to document
        for line in braille_text.split('\n'):
            p = doc.add_paragraph(line)
        
        doc.save(output_path)
