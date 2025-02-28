"""
PDF to Image Converter

This script converts each page of a PDF file into individual image files (PNG).
It handles dependency installation, argument parsing, and error handling.

Configuration:
    - Input PDF file path (-i or --input)
    - Output directory path (-o or --output)

Dependencies:
    - PyMuPDF (fitz)

Usage:
    python pdf_to_images.py -i <input_pdf_path> -o <output_directory_path>

Example:
    python pdf_to_images.py -i "my_document.pdf" -o "output_images"
"""

import argparse
import os
import subprocess
import sys

# --- Dependency Management ---
try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) is not installed. Would you like to install it now? (y/n)")
    response = input().lower()
    if response == 'y':
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymupdf'])
            import fitz  # Attempt to import again after installation
            print("PyMuPDF installed successfully.")
        except subprocess.CalledProcessError:
            print("Error: Failed to install PyMuPDF. Please install it manually.")
            sys.exit(1)  # Exit due to installation failure
        except ImportError:
            print("Error: Installation seems to have failed. Please install PyMuPDF manually.")
            sys.exit(1)
    else:
        print("PyMuPDF installation skipped. Please install it manually to run this script.")
        sys.exit(1)

# --- Configuration ---
DEFAULT_DPI = 300  # Sensible default DPI for image output

# --- Function: PDF to Images ---
def pdf_to_images(input_pdf, output_dir, dpi=DEFAULT_DPI):
    """
    Converts each page of a PDF file to individual PNG image files.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_dir (str): Path to the output directory.
        dpi (int): Dots per inch (DPI) for the output images.
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the PDF document
        try:
            doc = fitz.open(input_pdf)
        except fitz.FileDataError:
            print(f"Error: '{input_pdf}' is not a valid PDF file.")
            return
        except Exception as e:
            print(f"Error opening '{input_pdf}': {e}")
            return

        # Check if the PDF is empty
        if doc.is_empty:
            print(f"Error: '{input_pdf}' is an empty document.")
            doc.close()
            return

        # Convert each page to an image
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Calculate the scaling matrix for desired DPI
            matrix = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=matrix)
            # Create output filename with zero-padded page number
            output_path = os.path.join(output_dir, f"page_{page_num + 1:04d}.png")
            # Save the image
            pix.save(output_path, "png")

        # Close the PDF document
        doc.close()
        print(f"PDF '{input_pdf}' converted to images in '{output_dir}'")

    except Exception as e:
        print(f"Error: {e}")

# --- Argument Parsing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF pages to images.")
    parser.add_argument("-i", "--input", required=True, help="Input PDF file path.")
    parser.add_argument("-o", "--output", required=True, help="Output directory path.")
    args = parser.parse_args()

    # Call the conversion function
    pdf_to_images(args.input, args.output)