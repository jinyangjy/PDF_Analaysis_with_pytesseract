import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = "tesseract"
path_to_poppler_exe = Path("/opt/homebrew/Cellar/poppler/23.12.0/bin")

out_directory = Path("~/Desktop").expanduser()

PDF_FILE = Path("~/Desktop/handmaids_tale.pdf").expanduser()

image_file_list = []

text_file = out_directory / "handmaids_tale.txt"

def main():
    with TemporaryDirectory() as tempdir:

        pdf_pages = convert_from_path(
            PDF_FILE,
            500,
            poppler_path=path_to_poppler_exe,
        )

        for page_enumeration, page in enumerate(pdf_pages, start = 1):
            filename = f"{tempdir}/{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

        with open(text_file, "a") as output_file:
            for image_file in image_file_list:
                text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                text = text.replace('-\n', '')
                output_file.write(text)

if __name__ == "__main__":
    main()
