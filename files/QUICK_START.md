# Quick Start Guide - Brother QL-700 Label Printer

## ✅ Status: Ready to Print!

Your printer is **connected and detected**. Everything is set up correctly.

**IMPORTANT**: The Pillow library has been downgraded to version 9.5.0 to fix compatibility issues with brother_ql.

## 🚀 Quick Commands

### 1️⃣ Generate Previews First (No printer needed)
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
python3 print_labels_enhanced.py products.csv --preview --preview-count 10
```
This creates preview images in the `previews/` folder so you can see what your labels will look like.

### 2️⃣ Print a Test Label
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
sudo python3 print_labels.py products.csv --test
```
Enter your Mac password when prompted. This will print **only the first product** as a test.

### 3️⃣ Print a Small Batch (e.g., first 10 products)
```bash
sudo python3 print_labels_enhanced.py products.csv --start 1 --end 10
```

### 4️⃣ Print All Products
```bash
sudo python3 print_labels.py products.csv
```
⚠️ This will print all 1,200+ products and take 2-3 hours!

---

## 🎯 Using the Helper Script

Make it executable first (one-time):
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
chmod +x run_printer.sh
```

Then use simple commands:
```bash
./run_printer.sh test           # Test print one label
./run_printer.sh preview        # Generate preview images
./run_printer.sh batch 1 50     # Print products 1-50
./run_printer.sh all            # Print all products
```

---

## ⚠️ Important Notes

1. **You need to use `sudo`** on macOS to access the USB printer (you'll be asked for your password)
2. **Always test first** before printing hundreds of labels
3. **Check your label tape** - Make sure you have enough (you'll need 3-4 rolls for all products)
4. **Preview before printing** - Use the `--preview` option to see what labels will look like

---

## 🎨 What Your Labels Look Like

Each label has:
- **Text on the left**: Product name (up to 4 lines)
- **QR code on the right**: Contains the full product name
- **Size**: 62mm wide (standard continuous tape)

Example layout:
```
┌──────────────────────────────────────┐
│ AEKSHEA INCENSE          ████████    │
│ STICKS - MUSK 15G        ████████    │
│                          ████████    │
│                          ████████    │
└──────────────────────────────────────┐
```

---

## 📊 Your Products

You have **1,271+ products** in your CSV file, including:
- AEKSHEA INCENSE STICKS - MUSK 15G
- AEKSHEA INCENSE STICKS - OUDH 15G
- HEM PRECIOUS varieties
- NAG CHAMPA varieties
- And many more...

---

## 🔧 Customization Options

### Change QR Code Size
```bash
sudo python3 print_labels_enhanced.py products.csv --test --qr-size 250
```

### Change Font Size
```bash
sudo python3 print_labels_enhanced.py products.csv --test --font-size 30
```

### Add Delay Between Prints
```bash
sudo python3 print_labels_enhanced.py products.csv --delay 2
```
This adds a 2-second delay between each print.

### Print Specific Range
```bash
sudo python3 print_labels_enhanced.py products.csv --start 100 --end 200
```

---

## 📝 Next Steps

**Right now, do this:**

1. **Generate previews to see what your labels will look like:**
   ```bash
   cd /Users/parthsharma/Desktop/brother_printer/files
   python3 print_labels_enhanced.py products.csv --preview --preview-count 5
   open previews/
   ```

2. **If previews look good, print a test label:**
   ```bash
   sudo python3 print_labels.py products.csv --test
   ```

3. **Once you're happy with the test, start printing batches:**
   ```bash
   sudo python3 print_labels_enhanced.py products.csv --start 1 --end 50
   ```

---

## 🆘 Having Issues?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help.

Common fixes:
- Make sure printer is on and connected via USB
- Use `sudo` for all print commands
- Generate previews first to verify label design
- Test with one label before printing all

---

## 📁 Files Overview

- `print_labels.py` - Simple printer script
- `print_labels_enhanced.py` - Advanced script with more options
- `run_printer.sh` - Easy-to-use helper script
- `products.csv` - Your 1,271+ products
- `previews/` - Preview images folder (auto-created)
- `INSTALLATION_GUIDE.md` - Detailed installation instructions
- `TROUBLESHOOTING.md` - Problem-solving guide

---

**You're all set! Start with the preview command above.** 🚀
