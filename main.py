#!/usr/bin/env python

import os
from datetime import datetime
from PIL import Image
from fpdf import FPDF

INPUT_DIR = 'images'
ALLOWED_FILES =['.png', '.jpg', '.jpeg', '.bmp']
OUTPUT_DIR = 'output'
PDF_NAME = f"{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.pdf"

PAGE_WIDTH, PAGE_HEIGHT = 210, 297 # standard A4 in mm
MARGIN = 0
SPACING = 0

GRID_ROWS, GRID_COLS = 3, 3
CELL_WIDTH, CELL_HEIGHT = 63, 88 # standard mtg card in mm

DPI = 300

# check whether the layout fits on the page
def validate_layout():
    total_width = (GRID_COLS * CELL_WIDTH) + ((GRID_COLS - 1) * SPACING) + 2 * MARGIN
    total_height = (GRID_ROWS * CELL_HEIGHT) + ((GRID_ROWS - 1) * SPACING) + 2 * MARGIN

    if total_width > PAGE_WIDTH or total_height > PAGE_HEIGHT:
        raise ValueError(f'Grid layout ({total_width}mm x {total_height}mm) exceeds page size ({PAGE_WIDTH}mm x {PAGE_HEIGHT}mm).')

def mm_to_px(mm, dpi=DPI):
    mm_to_inch = 1 / 25.4
    return int(mm * mm_to_inch * dpi)

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def main():
    validate_layout()

    image_files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR)
                    if f.lower().endswith(ALLOWED_FILES)]

    pdf = FPDF('P', 'mm', 'A4')

    px_width = mm_to_px(CELL_WIDTH)
    px_height = mm_to_px(CELL_HEIGHT)

    for image_chunk in chunk_list(image_files, GRID_ROWS * GRID_COLS):
        pdf.add_page()

        for index, img_path in enumerate(image_chunk):
            row, col = divmod(index, GRID_COLS)
            x = MARGIN + col * (CELL_WIDTH + SPACING)
            y = MARGIN + row * (CELL_HEIGHT + SPACING)

            img = Image.open(img_path)
            img.thumbnail((px_width, px_height), Image.LANCZOS)

            temp_path = f'temp_{index}.png'
            img.save(temp_path, dpi=(DPI, DPI))

            pdf.image(temp_path, x, y, w=CELL_WIDTH, h=CELL_HEIGHT)

            os.remove(temp_path)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf.output(os.path.join(OUTPUT_DIR, PDF_NAME))

if __name__ == '__main__':
	main()