# Quick Reference - Brother QL-700 Label Printing

## Quick Start

### 1. Install (One-time setup)
**Windows:**
```
setup_windows.bat
```

**Linux/Mac:**
```
chmod +x setup_unix.sh
./setup_unix.sh
```

### 2. Test Print
```
python3 print_labels.py products.csv --test
```

### 3. Print All
```
python3 print_labels.py products.csv
```

## Common Commands

| Task | Command |
|------|---------|
| Test single label | `python3 print_labels.py products.csv --test` |
| Print all labels | `python3 print_labels.py products.csv` |
| Find printer | `brother_ql discover` |
| Use specific printer | `python3 print_labels.py products.csv --printer "usb://0x04f9:0x2042"` |
| Change label size | `python3 print_labels.py products.csv --label "62"` |

## Label Sizes for QL-700

| Code | Description |
|------|-------------|
| `62` | 62mm continuous (default) |
| `29` | 29mm continuous |
| `38` | 38mm continuous |
| `17x54` | 17x54mm die-cut |
| `29x90` | 29x90mm die-cut |
| `62x100` | 62x100mm die-cut |

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Can't find printer | Run `brother_ql discover` |
| Permission denied | Linux: `sudo usermod -a -G lp $USER` (then logout/login) |
| USB not detected | Check cable, try different USB port |
| QR code too small | Edit script: increase `qr_size` value |
| Text too large | Edit script: decrease font size |

## What You'll Need

- **Time:** 2-3 hours for 1,271 labels
- **Labels:** 3-4 rolls of 62mm continuous tape (DK-22205)
- **Power:** Keep printer plugged in
- **Space:** Clear area for label output

## File List

1. `products.csv` - Your product list
2. `print_labels.py` - Main printing script
3. `INSTALLATION_GUIDE.md` - Detailed instructions
4. `setup_windows.bat` - Windows setup script
5. `setup_unix.sh` - Linux/Mac setup script
6. This file - Quick reference

## Emergency Stop

Press `Ctrl+C` to stop printing at any time.
The script will ask if you want to continue after each error.

## Tips

✓ Always do a test print first
✓ Check label alignment every 50-100 labels
✓ Have backup label rolls ready
✓ Print in batches if needed (modify script)
✓ Keep USB cable secure during printing

## Support Resources

- Brother QL Python Library: https://github.com/pklaus/brother_ql
- QR Code Library: https://pypi.org/project/qrcode/
- PIL/Pillow Docs: https://pillow.readthedocs.io/
