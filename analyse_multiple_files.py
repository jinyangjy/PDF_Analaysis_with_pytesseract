import platform
import os
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = "tesseract"
path_to_poppler_exe = Path("/opt/homebrew/Cellar/poppler/23.12.0/bin")

out_directory = Path("~/Desktop/text_analyzer_ouput").expanduser()

pdf_directory = Path("~/Desktop/test_files").expanduser()

def convert_pdf_to_images(pdf_file, tempdir):
    PDF_FILES = pdf_directory / pdf_file
    image_file_list = []

    pdf_pages = convert_from_path(
        PDF_FILES,
        500,
        poppler_path = path_to_poppler_exe,
    )

    for page_enumeration, page in enumerate(pdf_pages, start = 1):
        filename = f"{tempdir}/{page_enumeration:03}.jpg"
        page.save(filename, "JPEG")
        image_file_list.append(filename)

    return image_file_list

def write_images_to_text_file(image_file_list, text_file):
    output_file = open(text_file, "a")

    for image_file in image_file_list:
        if Path(image_file).exists():
            image = Image.open(image_file)
            text = pytesseract.image_to_string(image)
            text = text.replace('-\n', '')
            output_file.write(text)
        else:
            print(f"File {image_file} not found.")

    output_file.close()

def process_pdf_files():
    pdf_files = []
    for f in os.listdir(pdf_directory):
        if f.endswith('.pdf'):
            pdf_files.append(f)

    for pdf_file in pdf_files:
        text_file = out_directory / f"{pdf_file.rstrip('.pdf')}.txt"

        tempdir = TemporaryDirectory()

        image_file_list = convert_pdf_to_images(pdf_file, tempdir.name)

        if not out_directory.exists():
            out_directory.mkdir(parents = True, exist_ok = True)

        write_images_to_text_file(image_file_list, text_file)

        tempdir.cleanup()

if __name__ == "__main__":
    process_pdf_files()
