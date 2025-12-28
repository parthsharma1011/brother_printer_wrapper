#!/usr/bin/env python3
"""
Enhanced Label Printer for Brother QL-700
Prints product labels with QR codes from CSV file
Includes batch processing, preview generation, and more options
"""

import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
import os
import time

def create_label_image(product_name, label_width=696, label_height=271, qr_size=180, font_size=None):
    """
    Create a label image with product name and QR code

    Args:
        product_name: Name of the product
        label_width: Width in pixels (62mm = 696px at 300dpi)
        label_height: Height in pixels (29mm = 271px at 300dpi)
        qr_size: Size of QR code in pixels (default: 180, fixed)
        font_size: Font size for product name (optional, auto-sizes if None)

    Returns:
        PIL Image object
    """
    # Create white background
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)

    # Generate QR code - FIXED SIZE for consistency
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(product_name)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # QR code FIXED size on RIGHT side
    qr_size = min(qr_size, label_height - 20)
    qr_img = qr_img.resize((qr_size, qr_size))

    # Paste QR code on the RIGHT side
    qr_x = label_width - qr_size - 10
    qr_y = (label_height - qr_size) // 2
    img.paste(qr_img, (qr_x, qr_y))

    # Find BOLD font path for better readability
    font_path = None
    font_index = 0  # For TTC files with multiple fonts

    # Try bold fonts in order of preference
    bold_font_options = [
        ("/System/Library/Fonts/Helvetica.ttc", 1),  # macOS Helvetica Bold (index 1)
        ("/System/Library/Fonts/Arial Black.ttf", 0),  # macOS Arial Black
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0),  # Linux bold
        ("C:\\Windows\\Fonts\\arialbd.ttf", 0),  # Windows bold
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),  # macOS alternate
        ("/System/Library/Fonts/Helvetica.ttc", 0),  # macOS Helvetica regular as fallback
    ]

    for path, index in bold_font_options:
        try:
            ImageFont.truetype(path, 24, index=index)
            font_path = path
            font_index = index
            break
        except:
            continue

    # Text area is LEFT side (before QR code)
    text_x = 10  # Start closer to edge for maximum space
    text_area_width = qr_x - 25  # Maximum space for text
    max_lines = 3  # Up to 3 lines for better text fitting

    # Auto-size font if not specified - Original readable sizes
    if font_size is None:
        font_sizes = [32, 28, 24, 20, 18]  # Original sizes
    else:
        font_sizes = [font_size]  # Use specified size

    best_font = None
    best_lines = []

    # Find the best font size that fits
    for size in font_sizes:
        if font_path:
            try:
                font = ImageFont.truetype(font_path, size, index=font_index)
            except:
                font = ImageFont.load_default()
        else:
            font = ImageFont.load_default()

        # Wrap text with this font size
        words = product_name.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= text_area_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, add it anyway
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        # Check if text fits within max_lines
        if len(lines) <= max_lines:
            best_font = font
            best_lines = lines
            break

    # If no font worked, use the smallest
    if best_font is None:
        if font_path:
            try:
                best_font = ImageFont.truetype(font_path, font_sizes[-1], index=font_index)
            except:
                best_font = ImageFont.load_default()
        else:
            best_font = ImageFont.load_default()
        best_lines = best_lines[:max_lines] if best_lines else lines[:max_lines]

    # Limit to max_lines
    best_lines = best_lines[:max_lines]

    # Calculate line height based on font with better spacing
    bbox = draw.textbbox((0, 0), "Ay", font=best_font)
    line_height = (bbox[3] - bbox[1]) + 12  # More spacing between lines

    # Draw text centered vertically
    total_text_height = len(best_lines) * line_height
    text_y = (label_height - total_text_height) // 2

    for i, line in enumerate(best_lines):
        draw.text((text_x, text_y + i * line_height), line, fill='black', font=best_font)

    return img

def print_label(printer_identifier, product_name, label_type='62', cut=True, **kwargs):
    """
    Print a single label

    Args:
        printer_identifier: Printer identifier
        product_name: Product name to print
        label_type: Label size
        cut: Whether to cut after printing (default: True)
        **kwargs: Additional parameters for label creation
    """
    # Create label image
    img = create_label_image(product_name, **kwargs)

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

def generate_previews(csv_file, output_dir='previews', max_previews=10):
    """
    Generate preview images of labels without printing
    
    Args:
        csv_file: Path to CSV file
        output_dir: Directory to save previews
        max_previews: Maximum number of previews to generate
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = list(reader)[:max_previews]
    
    print(f"Generating {len(products)} preview images...")
    
    for i, row in enumerate(products, 1):
        product_name = row['Product Name']
        img = create_label_image(product_name)
        filename = os.path.join(output_dir, f"preview_{i:03d}.png")
        img.save(filename)
        print(f"  {i}/{len(products)}: {filename}")
    
    print(f"\nPreviews saved to '{output_dir}/' directory")

def print_products(csv_file, printer_identifier='usb://0x04f9:0x2042',
                  label_type='62', start=None, end=None,
                  delay=0, no_cut=False, **kwargs):
    """
    Print labels for products in CSV file

    Args:
        csv_file: Path to CSV file
        printer_identifier: Printer identifier
        label_type: Label size
        start: Starting index (1-based)
        end: Ending index (1-based)
        delay: Delay between prints in seconds
        no_cut: If True, print continuously without cutting (default: False)
        **kwargs: Additional parameters for label creation
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = list(reader)

    # Apply range filtering
    if start is not None or end is not None:
        start_idx = (start - 1) if start else 0
        end_idx = end if end else len(products)
        products = products[start_idx:end_idx]
        print(f"Printing products {start_idx + 1} to {end_idx} ({len(products)} total)")
    else:
        print(f"Printing all {len(products)} products")

    if no_cut:
        print("⚠️  Continuous printing mode - labels will NOT be cut automatically")
        print("You can cut them manually later with scissors")

    success_count = 0
    error_count = 0
    start_time = time.time()

    for i, row in enumerate(products, 1):
        product_name = row['Product Name']
        actual_number = (start - 1 + i) if start else i

        print(f"\n[{actual_number}/{len(products) if not start else end}] {product_name}")

        try:
            print_label(printer_identifier, product_name, label_type, cut=not no_cut, **kwargs)
            success_count += 1
            print("  ✓ Printed successfully")

            # Add delay if specified
            if delay > 0 and i < len(products):
                print(f"  Waiting {delay} seconds...")
                time.sleep(delay)

        except Exception as e:
            error_count += 1
            print(f"  ✗ Error: {e}")
            response = input("  Continue? (y/n): ")
            if response.lower() != 'y':
                break

    # Print summary
    elapsed = time.time() - start_time
    print("\n" + "="*50)
    print("PRINTING SUMMARY")
    print("="*50)
    print(f"Total processed: {success_count + error_count}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Time elapsed: {elapsed/60:.1f} minutes")
    if success_count > 0:
        print(f"Average time per label: {elapsed/success_count:.1f} seconds")
    print("="*50)
    if no_cut:
        print("Remember to cut your continuous label roll!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Print product labels with QR codes on Brother QL-700',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Print first product as test
  %(prog)s products.csv --test
  
  # Print all products
  %(prog)s products.csv
  
  # Print products 1-100
  %(prog)s products.csv --start 1 --end 100
  
  # Generate preview images
  %(prog)s products.csv --preview
  
  # Custom QR code size and font
  %(prog)s products.csv --qr-size 250 --font-size 28
        """
    )
    
    parser.add_argument('csv_file', help='Path to CSV file with products')
    parser.add_argument('--printer', default='usb://0x04f9:0x2042', 
                        help='Printer identifier (default: usb://0x04f9:0x2042)')
    parser.add_argument('--label', default='62', 
                        help='Label type (default: 62 for 62mm continuous)')
    parser.add_argument('--test', action='store_true',
                        help='Print only the first product as a test')
    parser.add_argument('--preview', action='store_true',
                        help='Generate preview images without printing')
    parser.add_argument('--start', type=int,
                        help='Start at product number (1-based index)')
    parser.add_argument('--end', type=int,
                        help='End at product number (1-based index)')
    parser.add_argument('--delay', type=float, default=0,
                        help='Delay between prints in seconds')
    parser.add_argument('--qr-size', type=int, default=200,
                        help='QR code size in pixels (default: 200)')
    parser.add_argument('--font-size', type=int, default=24,
                        help='Font size for product name (default: 24)')
    parser.add_argument('--preview-count', type=int, default=10,
                        help='Number of previews to generate (default: 10)')
    parser.add_argument('--no-cut', action='store_true',
                        help='Print continuously without cutting (cut manually later)')

    args = parser.parse_args()

    # Generate previews
    if args.preview:
        generate_previews(args.csv_file, max_previews=args.preview_count)

    # Test print
    elif args.test:
        with open(args.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            first_product = next(reader)['Product Name']
        print(f"Test printing: {first_product}")
        print_label(args.printer, first_product, args.label, cut=not args.no_cut,
                   qr_size=args.qr_size, font_size=args.font_size)
        print("✓ Test complete!")

    # Normal printing
    else:
        print_products(args.csv_file, args.printer, args.label,
                      start=args.start, end=args.end, delay=args.delay, no_cut=args.no_cut,
                      qr_size=args.qr_size, font_size=args.font_size)
