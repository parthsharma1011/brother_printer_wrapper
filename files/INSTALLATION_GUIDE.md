# Brother QL-700 Automatic Label Printing Guide

## Overview
This guide will help you automatically print labels with QR codes for all your products using the Brother QL-700 printer.

## Prerequisites
- Brother QL-700 printer connected via USB
- Python 3.6 or higher
- Linux, macOS, or Windows

## Installation Steps

### Step 1: Install Required Python Libraries

```bash
# Install the required packages
pip install brother_ql qrcode[pil] pillow

# Or use pip3 if you have both Python 2 and 3
pip3 install brother_ql qrcode[pil] pillow
```

### Step 2: Install USB Backend (Linux/macOS)

For Linux:
```bash
# Install pyusb
pip install pyusb

# Install libusb (required for USB communication)
# Ubuntu/Debian:
sudo apt-get install libusb-1.0-0

# Fedora/RHEL:
sudo dnf install libusb
```

For macOS:
```bash
# Install pyusb
pip install pyusb

# Install libusb via Homebrew
brew install libusb
```

For Windows:
```bash
# Install pyusb
pip install pyusb

# You may need to install Zadig to set up USB drivers
# Download from: https://zadig.akeo.ie/
```

### Step 3: Set Up USB Permissions (Linux Only)

```bash
# Find your printer
lsusb | grep Brother

# Add yourself to the lp group
sudo usermod -a -G lp $USER

# Or create a udev rule for the printer
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="2042", MODE="0666"' | sudo tee /etc/udev/rules.d/99-brother-ql.rules

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Log out and log back in for group changes to take effect
```

## Finding Your Printer

Run this command to discover your printer:

```bash
brother_ql discover
```

This will show output like:
```
usb://0x04f9:0x2042
```

Copy this identifier - you'll need it for printing.

## Usage

### Test Print (Recommended First Step)

Before printing all 1,271 products, do a test print:

```bash
python3 print_labels.py products.csv --test
```

This will print only the first product to verify everything works.

### Print All Products

Once the test is successful, print all products:

```bash
python3 print_labels.py products.csv
```

### Custom Options

```bash
# Use a different printer identifier
python3 print_labels.py products.csv --printer "usb://0x04f9:0x2042"

# Use a different label size
python3 print_labels.py products.csv --label "62"

# Common label sizes for QL-700:
# - "62" = 62mm continuous tape (most common)
# - "29" = 29mm continuous tape
# - "38" = 38mm continuous tape
# - "17x54" = 17x54mm die-cut labels
# - "29x90" = 29x90mm die-cut labels
```

## Label Design

The script creates labels with:
- **QR Code** on the left (200x200 pixels)
- **Product Name** on the right (wrapped to 3 lines if needed)
- **Size**: 62mm width (default)

Example layout:
```
┌──────────────────────────────────────┐
│  ████████  AEKSHEA INCENSE STICKS   │
│  ████████  MUSK 15G                  │
│  ████████                            │
│  ████████                            │
└──────────────────────────────────────┘
```

## Troubleshooting

### Problem: "No such device" or "Device not found"

**Solution:**
1. Check USB connection
2. Run `lsusb` (Linux/macOS) to verify the printer is connected
3. Try running with sudo: `sudo python3 print_labels.py products.csv --test`
4. Check USB permissions (see Step 3 above)

### Problem: "Permission denied" error

**Solution:**
- Linux: Add yourself to the `lp` group and create udev rules (see Step 3)
- Windows: Run Command Prompt as Administrator
- macOS: Check System Preferences > Security & Privacy

### Problem: QR code doesn't scan properly

**Solution:**
- The QR code size might be too small
- Edit `print_labels.py` and increase `qr_size` (line 37)
- Or reduce the QR code error correction level

### Problem: Text doesn't fit on label

**Solution:**
- Product names are automatically wrapped to 3 lines
- Very long names might still overflow
- You can edit the font size in the script (line 48-49)

### Problem: Printer not discovered

**Solution:**
```bash
# List USB devices
lsusb

# Should show something like:
# Bus 001 Device 005: ID 04f9:2042 Brother Industries, Ltd

# If not showing, check USB cable and connection
```

## Advanced Customization

### Modify Label Design

Edit the `create_label_image()` function in `print_labels.py`:

```python
# Change QR code size
qr_size = 250  # Larger QR code

# Change font size
font_large = ImageFont.truetype("...", 30)  # Bigger text

# Change label dimensions
label_width = 696   # Width in pixels
label_height = 271  # Height in pixels
```

### Create a Preview

Add this function to generate preview images without printing:

```python
def preview_label(product_name, output_file='preview.png'):
    img = create_label_image(product_name)
    img.save(output_file)
    print(f"Preview saved to {output_file}")
```

## Tips for Efficient Printing

1. **Use Die-Cut Labels** if you have many different sized products
2. **Continuous Tape** is more economical for same-size labels
3. **Test first** with a few products before running the full batch
4. **Check label alignment** after every 50-100 prints
5. **Have extra label rolls** ready - 1,271 labels is a lot!

## Estimated Time

- Per label: ~5-10 seconds (including cut time)
- Total for 1,271 products: ~2-3 hours
- Plan accordingly and ensure you have enough labels!

## Label Consumption

- Each label uses approximately 62mm of tape (plus cut waste)
- Total tape needed: ~80-100 meters for all products
- Standard DK-22205 continuous roll is 30.48m
- You'll need about 3-4 rolls

## Alternative: Batch Processing

If you want to print in batches:

```python
# Edit the script to add start/end parameters
python3 print_labels.py products.csv --start 1 --end 100
python3 print_labels.py products.csv --start 101 --end 200
# etc.
```

## Windows-Specific Instructions

For Windows users:

1. Install Python from python.org
2. Open Command Prompt as Administrator
3. Install packages:
   ```
   pip install brother_ql qrcode[pil] pillow pyusb
   ```
4. Find printer using `brother_ql discover`
5. Run script:
   ```
   python print_labels.py products.csv --test
   ```

## Support

If you encounter issues:
1. Check the Brother QL Python library docs: https://github.com/pklaus/brother_ql
2. Verify your printer model is QL-700
3. Ensure you're using the correct label type
4. Test with the brother_ql command line tools first

## Example QR Code Data

Each QR code contains the full product name, for example:
- "AEKSHEA INCENSE STICKS - MUSK 15G"
- "DABUR AMLA HAIR OIL 200ML"
- "BRITANNIA GOOD DAY CASHEW 216G"

You can scan these with any QR code scanner app to retrieve the product name.
