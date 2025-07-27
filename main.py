#!/usr/bin/env python3
"""
📄 PDF Outline Extractor - Entry Point

This script runs inside the Docker container and processes all PDF files
from the /app/input directory, generating structured JSON outlines into /app/output.

Designed for:
- CPU-only, offline execution
- Fast, fault-tolerant batch processing
"""

import os
import sys
import glob
import json
from test import PDFOutlineExtractor  # Core logic lives in test.py


def process_pdfs():
    """Batch-process all PDF files in the input directory."""
    
    input_dir = "/app/input"
    output_dir = "/app/output"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Discover all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    if not pdf_files:
        print("📂 No PDF files found in /app/input. Please add files to process.")
        return

    print(f"📁 Found {len(pdf_files)} PDF file(s) to process\n")

    # Loop through each PDF and extract its outline
    for pdf_path in pdf_files:
        try:
            filename = os.path.splitext(os.path.basename(pdf_path))[0]
            output_path = os.path.join(output_dir, f"{filename}.json")

            print(f"➡️  Processing: {os.path.basename(pdf_path)}")

            # Instantiate extractor and run extraction
            extractor = PDFOutlineExtractor(pdf_path)
            outline = extractor.extract_outline()

            # Save the extracted outline to JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)

            print(f"✅ Done! Output saved to: {output_path}\n")

        except Exception as e:
            print(f"❌ Error processing {pdf_path}: {str(e)}\n")
            # Continue with the next file
            continue

    print("✅ All files processed successfully.")


# Run the script when executed inside the container
if __name__ == "__main__":
    process_pdfs()
