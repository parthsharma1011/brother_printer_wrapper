#!/usr/bin/env python3
"""
Automatic Label Printer for Brother QL-700
Prints product labels with QR codes from CSV file
"""

import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
import io

def create_label_image(product_name, label_width=696, label_height=271):
    """
    Create a label image with product name and QR code

    Args:
        product_name: Name of the product
        label_width: Width in pixels (696px for 62mm continuous roll)
        label_height: Height in pixels (271px for 29mm height)

    Returns:
        PIL Image object
    """
    # Create white background
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)

    # Generate QR code - sized for 62mm label
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=2,
    )
    qr.add_data(product_name)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Calculate QR code size and position
    qr_width, qr_height = qr_img.size
    qr_x = label_width - qr_width - 10
    qr_y = (label_height - qr_height) // 2

    # Paste QR code on the right side
    img.paste(qr_img, (qr_x, qr_y))

    # Add product name on the left side - BOLD and as large as possible
    # Try to find bold font
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_index = 1  # Index 1 is Helvetica Bold

    # Try different font sizes from largest to smallest
    font_sizes = [48, 44, 40, 36, 32, 28, 24, 20]
    max_width = qr_x - 20
    max_height = label_height - 20
    best_font = None
    best_lines = []

    for size in font_sizes:
        try:
            font = ImageFont.truetype(font_path, size, index=font_index)
        except:
            try:
                font = ImageFont.truetype(font_path, size)
            except:
                font = ImageFont.load_default()

        # Wrap text with this font size
        words = product_name.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Check if text fits vertically
        line_height = size + 8
        total_height = len(lines) * line_height

        if total_height <= max_height:
            best_font = font
            best_lines = lines
            break

    # If no font worked, use the smallest
    if best_font is None:
        try:
            best_font = ImageFont.truetype(font_path, font_sizes[-1], index=font_index)
        except:
            best_font = ImageFont.load_default()
        best_lines = lines

    # Draw text
    line_height = best_font.size + 8 if hasattr(best_font, 'size') else 28
    text_y = 10
    for line in best_lines:
        draw.text((10, text_y), line, fill='black', font=best_font)
        text_y += line_height

    return img

def print_label(printer_identifier, product_name, label_type='62', cut=True):
    """
    Print a single label

    Args:
        printer_identifier: Printer identifier (e.g., 'usb://0x04f9:0x2042')
        product_name: Product name to print
        label_type: Label size (default: '62' for 62mm continuous)
        cut: Whether to cut after printing (default: True)
    """
    # Create label image
    img = create_label_image(product_name)

    # Convert to Brother QL format
    qlr = BrotherQLRaster('QL-700')
    instructions = convert(
        qlr=qlr,
        images=[img],
        label=label_type,
        rotate='90',  # Rotate 90 degrees to print horizontally
        threshold=70.0,
        dither=False,
        compress=False,
        red=False,
        dpi_600=False,
        hq=True,
        cut=cut
    )

    # Send to printer
    send(instructions=instructions, printer_identifier=printer_identifier, backend_identifier='pyusb', blocking=True)

def print_all_products(csv_file, printer_identifier='usb://0x04f9:0x2042', label_type='62', no_cut=False):
    """
    Print labels for all products in CSV file

    Args:
        csv_file: Path to CSV file
        printer_identifier: Printer identifier
        label_type: Label size
        no_cut: If True, print continuously without cutting (default: False)
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = list(reader)

    print(f"Found {len(products)} products to print")
    if no_cut:
        print("⚠️  Continuous printing mode - labels will NOT be cut automatically")
        print("You can cut them manually later with scissors")

    for i, row in enumerate(products, 1):
        product_name = row['Product Name']
        print(f"Printing {i}/{len(products)}: {product_name}")

        try:
            print_label(printer_identifier, product_name, label_type, cut=not no_cut)
            print(f"  ✓ Printed successfully")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            # Ask if user wants to continue
            response = input("Continue? (y/n): ")
            if response.lower() != 'y':
                break

    print("\nPrinting complete!")
    if no_cut:
        print("Remember to cut your continuous label roll!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Print product labels with QR codes on Brother QL-700')
    parser.add_argument('csv_file', help='Path to CSV file with products')
    parser.add_argument('--printer', default='usb://0x04f9:0x2042',
                        help='Printer identifier (default: usb://0x04f9:0x2042)')
    parser.add_argument('--label', default='62',
                        help='Label type (default: 62 for 62mm continuous)')
    parser.add_argument('--test', action='store_true',
                        help='Print only the first product as a test')
    parser.add_argument('--no-cut', action='store_true',
                        help='Print continuously without cutting (cut manually later)')

    args = parser.parse_args()

    if args.test:
        with open(args.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            first_product = next(reader)['Product Name']
        print(f"Test printing: {first_product}")
        print_label(args.printer, first_product, args.label, cut=not args.no_cut)
        print("Test complete!")
    else:
        print_all_products(args.csv_file, args.printer, args.label, no_cut=args.no_cut)
