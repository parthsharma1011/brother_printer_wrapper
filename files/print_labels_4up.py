#!/usr/bin/env python3
"""
Grid Multi-Product Label Printer for Brother QL-700
Arranges products in a grid (columns × rows) to save space
"""

import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

def create_single_product_cell(product_name, cell_width=174, cell_height=250):
    """
    Create a single product cell with VERTICAL TEXT on LEFT and QR code on RIGHT

    Args:
        product_name: Name of the product
        cell_width: Width in pixels (~174px for 4 columns)
        cell_height: Height in pixels (250px for landscape label)

    Returns:
        PIL Image object
    """
    # Create white background for this cell
    img = Image.new('RGB', (cell_width, cell_height), 'white')
    draw = ImageDraw.Draw(img)

    # Bold font
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_index = 1  # Helvetica Bold

    # QR code on RIGHT side - smaller for 4-up layout
    qr_size = 100  # Smaller QR for 4 products
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
    )
    qr.add_data(product_name)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_size, qr_size))

    # Position QR on RIGHT side
    qr_x = cell_width - qr_size - 5
    qr_y = (cell_height - qr_size) // 2
    img.paste(qr_img, (qr_x, qr_y))

    # Create VERTICAL TEXT on LEFT side with wrapping
    # Try font sizes for vertical text
    font_sizes = [18, 16, 14, 12, 10]
    text_area_height = cell_height - 20  # Available height for text
    text_area_width = qr_x - 15  # Width available for text (when rotated, this is the height)

    best_font = None
    best_lines = []
    max_lines = 3  # Maximum number of wrapped lines

    for size in font_sizes:
        try:
            font = ImageFont.truetype(font_path, size, index=font_index)
        except:
            font = ImageFont.load_default()

        # Wrap text into multiple lines
        words = product_name.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]

            # Check if line fits in available height (when rotated)
            if line_width <= text_area_height:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Word too long, add anyway

        if current_line:
            lines.append(' '.join(current_line))

        # Check if all lines fit in available width (when rotated, this is horizontal space)
        if len(lines) <= max_lines:
            # Calculate total width needed for all lines
            bbox = draw.textbbox((0, 0), "Ay", font=font)
            line_height = (bbox[3] - bbox[1]) + 4
            total_width = len(lines) * line_height

            if total_width <= text_area_width:
                best_font = font
                best_lines = lines[:max_lines]
                break

    # Use smallest font if nothing fits
    if best_font is None:
        try:
            best_font = ImageFont.truetype(font_path, font_sizes[-1], index=font_index)
        except:
            best_font = ImageFont.load_default()
        best_lines = lines[:max_lines] if lines else [product_name]

    # Create text image with wrapped lines
    bbox = draw.textbbox((0, 0), "Ay", font=best_font)
    line_height = (bbox[3] - bbox[1]) + 4

    # Calculate dimensions for multi-line text
    max_line_width = 0
    for line in best_lines:
        bbox = draw.textbbox((0, 0), line, font=best_font)
        line_width = bbox[2] - bbox[0]
        max_line_width = max(max_line_width, line_width)

    # Create horizontal text image first
    text_img_width = max_line_width + 10
    text_img_height = (len(best_lines) * line_height) + 10
    text_img = Image.new('RGB', (text_img_width, text_img_height), 'white')
    text_draw = ImageDraw.Draw(text_img)

    # Draw each line
    y_pos = 5
    for line in best_lines:
        text_draw.text((5, y_pos), line, fill='black', font=best_font)
        y_pos += line_height

    # Rotate text 90 degrees counter-clockwise (reads bottom to top)
    text_img = text_img.rotate(90, expand=True)

    # Position rotated text on LEFT side
    text_x = 5
    text_y = (cell_height - text_img.height) // 2
    img.paste(text_img, (text_x, text_y))

    return img

def create_grid_label(products, label_width=696, columns=4, rows=1):
    """
    Create a label with products arranged HORIZONTALLY
    Landscape orientation: 4 products side by side (vertical text + QR)

    Args:
        products: List of product names
        label_width: Total width (696px for 62mm)
        columns: Number of columns (default: 4)
        rows: Number of rows (default: 1)

    Returns:
        PIL Image object
    """
    gap = 2  # Small gap between cells
    cell_width = (label_width - (columns - 1) * gap) // columns  # ~174px per column
    cell_height = 250  # Landscape label height
    label_height = cell_height

    # Create main label canvas
    label = Image.new('RGB', (label_width, label_height), 'white')

    # Place products horizontally
    for idx, product_name in enumerate(products):
        if idx >= columns:
            break  # Don't exceed 4 products per label

        x_position = idx * (cell_width + gap)
        y_position = 0

        cell = create_single_product_cell(product_name, cell_width, cell_height)
        label.paste(cell, (x_position, y_position))

        # Draw vertical separator lines between products
        if idx < columns - 1:
            draw = ImageDraw.Draw(label)
            line_x = x_position + cell_width + gap // 2
            draw.line([(line_x, 0), (line_x, cell_height)], fill='lightgray', width=1)

    return label

def print_grid_label(printer_identifier, products, label_type='62', cut=True, columns=4, rows=1):
    """
    Print a horizontal 4-up label with vertical text and QR codes

    Args:
        printer_identifier: Printer identifier
        products: List of product names (up to 4)
        label_type: Label size (default: '62' for 62mm continuous)
        cut: Whether to cut after printing
        columns: Number of columns (default: 4)
        rows: Number of rows (default: 1)
    """
    # Create grid label image
    img = create_grid_label(products, columns=columns, rows=rows)

    # Convert to Brother QL format
    qlr = BrotherQLRaster('QL-700')
    instructions = convert(
        qlr=qlr,
        images=[img],
        label=label_type,
        rotate='90',  # Landscape orientation (rotate 90 degrees)
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

def print_all_products_grid(csv_file, printer_identifier='usb://0x04f9:0x2042', label_type='62', no_cut=False, columns=4, rows=1):
    """
    Print all products in horizontal 4-up format (4 products per label)

    Args:
        csv_file: Path to CSV file
        printer_identifier: Printer identifier
        label_type: Label size
        no_cut: If True, print continuously without cutting
        columns: Number of columns per label (default: 4)
        rows: Number of rows per label (default: 1)
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = [row['Product Name'] for row in reader]

    products_per_label = columns * rows
    total_products = len(products)
    total_labels = (total_products + products_per_label - 1) // products_per_label  # Round up

    print(f"Found {total_products} products")
    print(f"Will print {total_labels} labels ({columns}×{rows} = {products_per_label} products per label)")

    if no_cut:
        print("⚠️  Continuous printing mode - labels will NOT be cut automatically")

    label_num = 0
    for i in range(0, total_products, products_per_label):
        batch = products[i:i+products_per_label]
        label_num += 1

        print(f"\nLabel {label_num}/{total_labels}: {len(batch)} products")
        for j, product in enumerate(batch, 1):
            print(f"  [{j}] {product}")

        try:
            print_grid_label(printer_identifier, batch, label_type, cut=not no_cut, columns=columns, rows=rows)
            print(f"  ✓ Printed successfully")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            response = input("  Continue? (y/n): ")
            if response.lower() != 'y':
                break

    print(f"\nPrinting complete!")
    print(f"Total: {label_num} labels printed ({sum([len(products[i:i+products_per_label]) for i in range(0, total_products, products_per_label)])} products)")
    if no_cut:
        print("Remember to cut your continuous label roll!")

def print_all_products_batch(csv_file, printer_identifier='usb://0x04f9:0x2042', label_type='62',
                            batch_size=20, columns=4, rows=1, no_resume=False):
    """
    Print all products in batches with resume functionality
    Cuts after each batch for easy handling

    Args:
        csv_file: Path to CSV file
        printer_identifier: Printer identifier
        label_type: Label size
        batch_size: Number of products per batch (default: 20)
        columns: Number of columns per label (default: 4)
        rows: Number of rows per label (default: 1)
        no_resume: If True, force fresh start (default: False)
    """
    import json
    import os
    import time
    from datetime import datetime

    # Validate batch_size is multiple of products_per_label
    products_per_label = columns * rows
    if batch_size % products_per_label != 0:
        print(f"⚠️  Warning: batch_size ({batch_size}) is not a multiple of products_per_label ({products_per_label})")
        print(f"Adjusting batch_size to {(batch_size // products_per_label) * products_per_label}")
        batch_size = (batch_size // products_per_label) * products_per_label

    # Load all products
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = [row['Product Name'] for row in reader]

    total_products = len(products)
    total_batches = (total_products + batch_size - 1) // batch_size
    labels_per_batch = batch_size // products_per_label

    # Progress file setup
    csv_basename = os.path.basename(csv_file).replace('.csv', '')
    progress_file = f"{csv_basename}_progress.json"

    # Check for existing progress
    start_batch = 0
    if os.path.exists(progress_file) and not no_resume:
        try:
            with open(progress_file, 'r') as f:
                progress = json.load(f)

            last_batch = progress.get('last_completed_batch', -1)
            last_product = progress.get('last_product_index', -1)
            saved_time = progress.get('timestamp', 'unknown')

            start_product = (last_batch + 1) * batch_size
            end_product = min(start_product + batch_size, total_products)

            print("\n" + "="*60)
            print("📋 RESUME AVAILABLE")
            print("="*60)
            print(f"Last session: {saved_time}")
            print(f"Last completed batch: {last_batch + 1}/{total_batches}")
            print(f"Last product printed: {last_product + 1}/{total_products}")
            print(f"Next batch: {last_batch + 2} (products {start_product + 1}-{end_product})")
            print("="*60)

            response = input("\nResume from this position? [y/N]: ").strip().lower()
            if response == 'y':
                start_batch = last_batch + 1
                print(f"✓ Resuming from batch {start_batch + 1}")
            else:
                print("✓ Starting fresh from beginning")
                start_batch = 0
        except Exception as e:
            print(f"⚠️  Could not load progress file: {e}")
            print("Starting fresh from beginning")
            start_batch = 0

    # Display job summary
    print("\n" + "="*60)
    print("🖨️  BATCH PRINTING JOB")
    print("="*60)
    print(f"Total products: {total_products}")
    print(f"Batch size: {batch_size} products")
    print(f"Labels per batch: {labels_per_batch} labels")
    print(f"Total batches: {total_batches}")
    print(f"Starting from: Batch {start_batch + 1}")
    print(f"�� Progress will be saved to: {progress_file}")
    print("="*60)
    print()

    # Confirm start
    if start_batch == 0:
        response = input("Start printing? [y/N]: ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return

    # Print batches
    success_batches = 0
    error_count = 0
    start_time = time.time()

    for batch_num in range(start_batch, total_batches):
        batch_start_idx = batch_num * batch_size
        batch_end_idx = min(batch_start_idx + batch_size, total_products)
        batch_products = products[batch_start_idx:batch_end_idx]

        print("\n" + "="*60)
        print(f"📦 BATCH {batch_num + 1}/{total_batches}")
        print("="*60)
        print(f"Products: {batch_start_idx + 1} to {batch_end_idx} ({len(batch_products)} products)")
        print(f"Labels in this batch: {(len(batch_products) + products_per_label - 1) // products_per_label}")
        print("="*60)

        # Print labels in this batch (continuous, no cut between labels)
        label_num_in_batch = 0
        for i in range(0, len(batch_products), products_per_label):
            label_products = batch_products[i:i+products_per_label]
            label_num_in_batch += 1

            product_indices = f"{batch_start_idx + i + 1}-{batch_start_idx + i + len(label_products)}"
            print(f"\n  Label {label_num_in_batch}: Products {product_indices}")
            for j, p in enumerate(label_products, 1):
                print(f"    [{j}] {p}")

            try:
                # Print without cutting (except last label of batch)
                is_last_label = (i + products_per_label >= len(batch_products))
                cut_after = is_last_label  # Only cut after last label of batch

                print_grid_label(printer_identifier, label_products, label_type,
                               cut=cut_after, columns=columns, rows=rows)
                print(f"    ✓ Printed successfully" + (" & CUT" if cut_after else ""))

            except Exception as e:
                error_count += 1
                print(f"    ✗ Error: {e}")
                response = input("    Continue with next label? (y/n): ")
                if response.lower() != 'y':
                    print("\n⚠️  Printing stopped by user")
                    print(f"Progress saved. You can resume from batch {batch_num + 1}")
                    return

        # Batch completed successfully
        success_batches += 1

        # Save progress after successful batch
        progress_data = {
            'last_completed_batch': batch_num,
            'last_product_index': batch_end_idx - 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_batches': total_batches,
            'batch_size': batch_size
        }

        try:
            with open(progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
            print(f"\n  ✓ Batch {batch_num + 1} completed and saved")
        except Exception as e:
            print(f"\n  ⚠️  Could not save progress: {e}")

        # Show progress
        elapsed = time.time() - start_time
        remaining_batches = total_batches - (batch_num + 1)
        if success_batches > 0:
            avg_time_per_batch = elapsed / success_batches
            est_remaining = avg_time_per_batch * remaining_batches
            print(f"  Progress: {batch_num + 1}/{total_batches} batches ({((batch_num + 1) / total_batches * 100):.1f}%)")
            print(f"  Estimated time remaining: {est_remaining / 60:.1f} minutes")

    # All batches complete!
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("🎉 PRINTING COMPLETE!")
    print("="*60)
    print(f"Total batches printed: {success_batches}")
    print(f"Total products printed: {total_products}")
    print(f"Total labels printed: {(total_products + products_per_label - 1) // products_per_label}")
    print(f"Time elapsed: {elapsed / 60:.1f} minutes")
    if success_batches > 0:
        print(f"Average time per batch: {elapsed / success_batches:.1f} seconds")
    print("="*60)

    # Delete progress file on successful completion
    try:
        if os.path.exists(progress_file):
            os.remove(progress_file)
            print(f"✓ Progress file deleted (job complete)")
    except Exception as e:
        print(f"⚠️  Could not delete progress file: {e}")

def generate_preview(csv_file, output_file='preview_4up.png', num_labels=3, columns=4, rows=1):
    """
    Generate preview images of multiple labels without printing

    Args:
        csv_file: Path to CSV file
        output_file: Output filename for preview
        num_labels: Number of labels to preview (default: 3)
        columns: Number of columns per label
        rows: Number of rows per label
    """
    import os

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_products = [row['Product Name'] for row in reader]

    products_per_label = columns * rows
    total_products_needed = num_labels * products_per_label

    if total_products_needed > len(all_products):
        num_labels = len(all_products) // products_per_label
        print(f"Not enough products for {num_labels} labels, generating {num_labels} instead")

    print(f"Generating preview of {num_labels} labels ({products_per_label} products each)...")

    # Create individual label images
    label_images = []
    for label_idx in range(num_labels):
        start_idx = label_idx * products_per_label
        batch = all_products[start_idx:start_idx + products_per_label]

        print(f"\nLabel {label_idx + 1}:")
        for i, p in enumerate(batch, 1):
            print(f"  [{i}] {p}")

        label_img = create_grid_label(batch, columns=columns, rows=rows)
        label_images.append(label_img)

    # Stack labels vertically for preview
    total_height = sum(img.height for img in label_images) + (len(label_images) - 1) * 20  # 20px gap
    preview_width = label_images[0].width

    preview = Image.new('RGB', (preview_width, total_height), 'white')

    y_offset = 0
    for img in label_images:
        preview.paste(img, (0, y_offset))
        y_offset += img.height + 20  # Add gap between labels

    preview.save(output_file)
    print(f"\n✓ Preview saved: {output_file}")
    print(f"Dimensions: {preview.width}x{preview.height}px")
    print(f"Open it to review before printing!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Print grid product labels on Brother QL-700')
    parser.add_argument('csv_file', help='Path to CSV file with products')
    parser.add_argument('--printer', default='usb://0x04f9:0x2042',
                        help='Printer identifier (default: usb://0x04f9:0x2042)')
    parser.add_argument('--label', default='62',
                        help='Label type (default: 62 for 62mm continuous)')
    parser.add_argument('--test', action='store_true',
                        help='Print first products as a test in grid format')
    parser.add_argument('--preview', action='store_true',
                        help='Generate preview images without printing')
    parser.add_argument('--preview-labels', type=int, default=3,
                        help='Number of labels to preview (default: 3)')
    parser.add_argument('--no-cut', action='store_true',
                        help='Print continuously without cutting')
    parser.add_argument('--columns', type=int, default=4,
                        help='Number of columns per label (default: 4 for horizontal layout)')
    parser.add_argument('--rows', type=int, default=1,
                        help='Number of rows per label (default: 1)')
    parser.add_argument('--batch', action='store_true',
                        help='Print all products in batches with cuts after each batch')
    parser.add_argument('--batch-size', type=int, default=20,
                        help='Number of products per batch (default: 20, must be multiple of columns×rows)')
    parser.add_argument('--no-resume', action='store_true',
                        help='Start from beginning, ignore saved progress')

    args = parser.parse_args()

    products_per_label = args.columns * args.rows

    if args.preview:
        # Generate preview only
        generate_preview(args.csv_file, num_labels=args.preview_labels, columns=args.columns, rows=args.rows)
    elif args.test:
        with open(args.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            test_products = [next(reader)['Product Name'] for _ in range(products_per_label)]
        print(f"Test printing {len(test_products)} products ({args.columns}×{args.rows} grid):")
        for i, p in enumerate(test_products, 1):
            print(f"  {i}. {p}")
        print_grid_label(args.printer, test_products, args.label, cut=True, columns=args.columns, rows=args.rows)
        print("✓ Test complete!")
    elif args.batch:
        # Batch printing with resume functionality
        print_all_products_batch(args.csv_file, args.printer, args.label,
                                batch_size=args.batch_size, columns=args.columns,
                                rows=args.rows, no_resume=args.no_resume)
    else:
        print_all_products_grid(args.csv_file, args.printer, args.label, no_cut=args.no_cut, columns=args.columns, rows=args.rows)
