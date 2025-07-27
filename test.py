import fitz  # PyMuPDF
import json
import collections
import sys
import os
import logging
import re

logging.basicConfig(level=logging.INFO)

class PDFOutlineExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.font_sizes = collections.Counter()
        self.headings = []
        self.title = "Untitled Document"
        self.sorted_font_sizes = []

    def _analyze_fonts(self):
        """Collect font sizes from spans to estimate significance."""
        for page in self.doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block['type'] == 0:
                    for line in block['lines']:
                        for span in line['spans']:
                            size = round(span['size'], 1)
                            self.font_sizes[size] += 1
        self.sorted_font_sizes = sorted(self.font_sizes, reverse=True)
        logging.info(f"Detected font sizes (sorted): {self.sorted_font_sizes}")

    def _extract_title(self):
        """Use the largest, most centered text on page 1 as the title."""
        page = self.doc[0]
        blocks = page.get_text("dict")["blocks"]
        candidates = []

        for block in blocks:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    if not text:
                        continue
                    font_size = round(span['size'], 1)
                    center_x = (line['bbox'][0] + line['bbox'][2]) / 2
                    distance_from_center = abs(center_x - page.rect.width / 2)
                    candidates.append((font_size, distance_from_center, text))

        if candidates:
            candidates.sort(key=lambda x: (-x[0], x[1]))
            self.title = candidates[0][2]
            logging.info(f"Title extracted: {self.title}")

    def _is_valid_heading(self, text):
        """Basic cleanup to filter junk."""
        if not text or len(text) < 3:
            return False
        if text.startswith(("●", "•", "-", "*")):
            return False
        if len(text.split()) <= 3 and not text[0].isupper():
            return False
        if len(text.split()) > 25:
            return False
        if re.search(r"\.(\s|$)", text) and not re.match(r"^\(?\d{1,2}[\.\)]?\s+\w+", text):
            return False
        return True

    def _get_heading_level(self, font_size, is_bold):
        """Assign H1–H3 based on font size rank and boldness."""
        if not self.sorted_font_sizes:
            return "H1"
        for i, size in enumerate(self.sorted_font_sizes[:3]):
            if font_size >= size * 0.95 or (is_bold and font_size >= size * 0.85):
                return f"H{i+1}"
        return None

    def extract_outline(self):
        self._analyze_fonts()
        self._extract_title()

        for page_num, page in enumerate(self.doc):
            blocks = page.get_text("dict")["blocks"]
            blocks.sort(key=lambda b: b["bbox"][1])  # top-down

            for block in blocks:
                if block['type'] != 0:
                    continue

                lines = block['lines']
                if not lines:
                    continue

                merged_text = ""
                merged_fonts = []
                is_bold = False
                last_y = None

                for line in lines:
                    line_text = ""
                    line_fonts = []
                    line_bold = False
                    line_y = line["bbox"][1]

                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        font_size = round(span["size"], 1)
                        font_name = span["font"].lower()

                        line_fonts.append(font_size)
                        if "bold" in font_name or "black" in font_name:
                            line_bold = True

                        line_text += text + " "

                    if not line_text.strip():
                        continue

                    # Merge if line is close vertically
                    if last_y is None or abs(line_y - last_y) < 12:
                        merged_text += line_text + " "
                        merged_fonts.extend(line_fonts)
                        is_bold = is_bold or line_bold
                    else:
                        # Flush previous block
                        self._flush_block(merged_text, merged_fonts, is_bold, page_num)
                        # Start new block
                        merged_text = line_text + " "
                        merged_fonts = line_fonts
                        is_bold = line_bold

                    last_y = line_y

                # Final flush after loop
                self._flush_block(merged_text, merged_fonts, is_bold, page_num)

        return {
            "title": self.title,
            "outline": self.headings
        }

    def _flush_block(self, text, fonts, bold, page_num):
        text = text.strip()
        if not text or not fonts:
            return
        if not self._is_valid_heading(text):
            return
        avg_font = sum(fonts) / len(fonts)
        level = self._get_heading_level(avg_font, bold)
        if level:
            self.headings.append({
                "level": level,
                "text": text,
                "page": page_num + 1
            })

def main():
    if len(sys.argv) != 3:
        print("Usage: python pdf_outline_extractor_v2.py <input_pdf_path> <output_json_path>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    if not os.path.exists(input_pdf):
        print("File not found:", input_pdf)
        sys.exit(1)

    try:
        extractor = PDFOutlineExtractor(input_pdf)
        outline = extractor.extract_outline()

        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(outline, f, indent=2, ensure_ascii=False)

        print("✅ Outline extracted to", output_json)
    except Exception as e:
        print("❌ Error:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
