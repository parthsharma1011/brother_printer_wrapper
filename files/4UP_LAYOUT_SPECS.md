# 4-Up Horizontal Label Layout - Complete Specifications

## ✅ Final Layout Configuration
**Date**: 2025-12-26
**Status**: FROZEN - Perfect working configuration

---

## 📐 Label Dimensions

### Overall Label
- **Label Width**: 696px (62mm at 300dpi)
- **Label Height**: 250px (landscape orientation)
- **Products per Label**: 4 (horizontal layout)
- **Orientation**: Landscape (rotate='90' in printer settings)

### Individual Cell (Per Product)
- **Cell Width**: 174px (~230px / 4 products)
- **Cell Height**: 250px
- **Gap Between Cells**: 2px
- **Separator Lines**: 1px lightgray vertical lines between products

---

## 🔤 Font Settings

### Font Configuration
- **Font Family**: Helvetica Bold
- **Font Path**: `/System/Library/Fonts/Helvetica.ttc`
- **Font Index**: 1 (Helvetica Bold variant in TTC file)

### Font Sizes (Auto-sizing)
Tries in order (uses largest that fits):
1. **18pt** (largest, preferred)
2. **16pt**
3. **14pt**
4. **12pt**
5. **10pt** (minimum fallback)

### Text Wrapping
- **Maximum Lines**: 3 lines
- **Line Spacing**: 4px between lines
- **Text Area Height**: 230px (cell_height - 20px)
- **Text Area Width**: 54px (when rotated, qr_x - 15px)

---

## 📝 Text Layout

### Orientation
- **Text Direction**: Vertical (rotated 90° counter-clockwise)
- **Reading Direction**: Bottom to Top
- **Position**: LEFT side of each cell
- **Horizontal Offset**: 5px from left edge
- **Vertical Centering**: Yes (centered in cell height)

### Wrapping Algorithm
```python
# Words wrap to fit within available height (when rotated)
# Each line must fit within: cell_height - 20px = 230px
# Multiple lines stack horizontally (when rotated)
# Maximum 3 lines to fit within available width
```

---

## 🔲 QR Code Settings

### QR Code Configuration
- **Size**: 100x100 pixels (fixed)
- **QR Version**: 1 (auto-sizing)
- **Error Correction**: ERROR_CORRECT_L (low, ~7%)
- **Box Size**: 3 pixels per module
- **Border**: 1 module
- **Colors**: Black on White

### QR Code Position
- **Location**: RIGHT side of each cell
- **Horizontal Offset**: 5px from right edge (cell_width - qr_size - 5)
- **Vertical Centering**: Yes (centered in cell height)

---

## 🎨 Color Scheme

- **Background**: White (`'white'`)
- **Text**: Black (`'black'`)
- **QR Code**: Black on White
- **Separator Lines**: Light Gray (`'lightgray'`)

---

## 📊 Tape Savings

### Efficiency Comparison
- **Old Method**: 1,271 products = 1,271 labels
- **New Method**: 1,271 products = ~318 labels
- **Savings**: **75% reduction** in label tape usage
- **Labels per Roll**: Significantly more products per roll

---

## 🖨️ Printer Settings

### Brother QL-700 Configuration
```python
printer_identifier = 'usb://0x04f9:0x2042'
label_type = '62'  # 62mm continuous tape
rotate = '90'  # Landscape orientation
threshold = 70.0
dither = False
compress = False
red = False
dpi_600 = False
hq = True  # High quality mode
cut = True/False  # Depends on mode
```

### Print Modes
- **Test Mode**: Auto-cut enabled (cut=True)
- **Production Mode**: Continuous printing (cut=False, no_cut=True)

---

## 📁 File Structure

### Main Script
**File**: `print_labels_4up.py`

### Key Functions

#### `create_single_product_cell(product_name, cell_width=174, cell_height=250)`
Creates individual product cell with vertical text and QR code.

**Parameters**:
- `product_name`: Product name string
- `cell_width`: 174px (calculated from label_width / 4)
- `cell_height`: 250px (landscape)

**Returns**: PIL Image object (174x250px)

#### `create_grid_label(products, label_width=696, columns=4, rows=1)`
Creates complete label with 4 products arranged horizontally.

**Parameters**:
- `products`: List of up to 4 product names
- `label_width`: 696px (62mm)
- `columns`: 4 (horizontal layout)
- `rows`: 1 (single row)

**Returns**: PIL Image object (696x250px)

#### `print_grid_label(printer_identifier, products, label_type='62', cut=True, columns=4, rows=1)`
Prints the grid label to Brother QL-700 printer.

#### `generate_preview(csv_file, output_file='preview_4up.png', num_labels=3, columns=4, rows=1)`
Generates preview image without printing.

---

## 💻 Command Line Usage

### Generate Preview (No Printer)
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
/Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --preview --preview-labels 5
```

### Test Print (First 4 Products)
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --test
```

### Print All Products (Continuous)
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --no-cut
```

### Print All Products (With Auto-Cut)
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv
```

### Batch Printing (Recommended for Production)
Print all products in batches of 20 with cuts after each batch:
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --batch
```

**Features:**
- Cuts only after each batch (not individual labels)
- Resume functionality if interrupted
- Progress saved to `products_progress.json`
- Default: 20 products per batch (5 labels)

### Batch Printing with Custom Batch Size
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --batch --batch-size 40
```

### Resume from Last Batch
If interrupted, simply run the same command again:
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --batch
```
Script will detect saved progress and offer to resume.

### Start Fresh (Ignore Saved Progress)
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --batch --no-resume
```

### Custom Column Count
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --columns 3 --test
```

---

## 🔧 Technical Implementation Details

### Text Rendering Process
1. **Calculate Available Space**:
   - Height: `cell_height - 20px = 230px`
   - Width: `qr_x - 15px = 54px`

2. **Try Font Sizes** (18pt → 10pt):
   - For each size, wrap text into lines
   - Check if each line fits in available height
   - Check if total lines (≤3) fit in available width

3. **Create Text Image**:
   - Draw wrapped lines horizontally
   - Rotate 90° counter-clockwise
   - Paste at left side of cell

4. **Result**:
   - Vertical text reading bottom-to-top
   - Up to 3 wrapped lines
   - Maximum readable font size

### QR Code Generation
```python
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=3,
    border=1,
)
qr.add_data(product_name)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img = qr_img.resize((100, 100))
```

---

## 📋 Example Output

### Sample Label (Text Representation)
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ A               │ A               │ A               │ A               │
│ E               │ E               │ E               │ E               │
│ K  ████████     │ K  ████████     │ K  ████████     │ K  ████████     │
│ S  ████████     │ S  ████████     │ S  ████████     │ S  ████████     │
│ H  ████████     │ H  ████████     │ H  ████████     │ H  ████████     │
│ E  ████████     │ E  ████████     │ E  ████████     │ E  ████████     │
│ A  ████████     │ A  ████████     │ A  ████████     │ A  ████████     │
│                 │                 │                 │                 │
│ I  S            │ I  S            │ I  S            │ I  S            │
│ N  T            │ N  T            │ N  T            │ N  T            │
│ C  I            │ C  I            │ C  I            │ C  I            │
│ E  C            │ E  C            │ E  C            │ E  C            │
│ N  K            │ N  K            │ N  K            │ N  K            │
│ S  S            │ S  S            │ S  S            │ S  S            │
│ E                │ E                │ E                │ E                │
│                 │                 │                 │                 │
│ S  -            │ S  -            │ S  -            │ S  -            │
│ T  M            │ T  O            │ T  Y            │ T  C            │
│ I  U            │ I  U            │ I  O            │ I  H            │
│ C  S            │ C  D            │ C  G            │ C  A            │
│ K  K            │ K  H            │ K  A            │ K  N            │
│ S                │ S                │ S                │ S                │
│                 │                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
  Product 1         Product 2         Product 3         Product 4
```

---

## 🎯 Key Success Factors

### What Makes This Layout Work
1. ✅ **Text Wrapping**: Prevents truncation, all text visible
2. ✅ **Font Auto-Sizing**: Maximizes readability while fitting text
3. ✅ **Vertical Orientation**: Space-efficient, matches user's example
4. ✅ **Fixed QR Size**: Consistent scanning experience
5. ✅ **4 Products Per Label**: Optimal balance of density and readability
6. ✅ **Bold Font**: Enhanced readability on small labels
7. ✅ **Landscape Orientation**: Maximizes horizontal space utilization

### Critical Settings (DO NOT CHANGE)
- Cell width: 174px (perfect division of 696px)
- Cell height: 250px (optimal for vertical text + QR)
- QR size: 100px (scannable but not too large)
- Font sizes: 18-10pt range (readable when vertical)
- Max lines: 3 (fits within available width when rotated)
- Gap: 2px (minimal but visible separation)

---

## 🔒 Version Control

**Version**: 1.0 FINAL
**Last Modified**: 2025-12-26
**Status**: FROZEN - PRODUCTION READY
**Python Version**: 3.x
**Required Libraries**:
- Pillow == 9.5.0 (CRITICAL: Do not upgrade)
- qrcode
- brother_ql == 0.9.4

---

## 📝 Notes

- This configuration has been tested and approved by the user
- All text wraps properly without truncation
- QR codes are scannable at 100x100px
- Layout matches user's original example image
- 75% tape savings confirmed
- Font is bold and readable when rotated vertically

**DO NOT MODIFY** these settings without thorough testing, as they represent the optimal configuration for this specific use case.
