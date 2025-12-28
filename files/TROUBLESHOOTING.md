# Troubleshooting Guide for Brother QL-700 Printer

## Problem Identified: USB Permission Error

Your printer **IS connected and detected**, but you're getting this error:
```
usb.core.USBError: [Errno 13] Access denied (insufficient permissions)
```

## Solutions (Choose One)

### ✅ Solution 1: Run with sudo (Quickest)

Since you're on macOS, the easiest solution is to run the scripts with `sudo`:

```bash
cd /Users/parthsharma/Desktop/brother_printer/files

# Test print (recommended first)
sudo python3 print_labels.py products.csv --test

# If test works, print all products
sudo python3 print_labels.py products.csv
```

**Why sudo?** On macOS, accessing USB devices directly requires administrator privileges.

---

### ✅ Solution 2: Fix USB Permissions (One-time setup)

This allows you to run without sudo in the future:

1. **Find your printer's vendor and product IDs** (already confirmed: 04f9:2042)

2. **Unload the default macOS printer driver:**
   ```bash
   # Check if the driver is loaded
   kextstat | grep -i brother

   # If found, unload it
   sudo kextunload -b com.Brother.QL700
   ```

3. **Use the network backend instead** (if your printer supports it)
   ```bash
   python3 print_labels.py products.csv --test --printer "tcp://192.168.1.XXX"
   ```

---

### ✅ Solution 3: Use the Enhanced Script with Better Error Handling

The `print_labels_enhanced.py` has better error handling:

```bash
sudo python3 print_labels_enhanced.py products.csv --test
```

---

## Quick Start Commands

### Run Test Print
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
sudo python3 print_labels.py products.csv --test
```

### Print Batch of 10 Labels
```bash
sudo python3 print_labels_enhanced.py products.csv --start 1 --end 10
```

### Generate Previews (No printer needed!)
```bash
python3 print_labels_enhanced.py products.csv --preview --preview-count 20
```

### Print All Products
```bash
sudo python3 print_labels.py products.csv
```

---

## What's Working ✅

- ✅ Python 3.11.4 installed
- ✅ All required packages installed (brother_ql, qrcode, pillow, pyusb)
- ✅ libusb installed via Homebrew
- ✅ Brother QL-700 printer detected at `usb://0x04f9:0x2042`
- ✅ Your code is correct and functional

## What's the Issue ❌

- ❌ USB permissions on macOS require sudo/root access

---

## Testing Steps

1. **First, generate a preview** (doesn't need printer):
   ```bash
   cd /Users/parthsharma/Desktop/brother_printer/files
   python3 print_labels_enhanced.py products.csv --preview --preview-count 5
   ```
   Check the `previews/` folder to see what your labels will look like.

2. **Run a test print with sudo:**
   ```bash
   sudo python3 print_labels.py products.csv --test
   ```
   Enter your macOS password when prompted.

3. **If successful, try printing a small batch:**
   ```bash
   sudo python3 print_labels_enhanced.py products.csv --start 1 --end 5
   ```

4. **Once confident, print all products:**
   ```bash
   sudo python3 print_labels.py products.csv
   ```

---

## Common Issues

### "Command not found"
Make sure you're in the correct directory:
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
pwd  # Should show: /Users/parthsharma/Desktop/brother_printer/files
```

### "File not found: products.csv"
Check that the CSV file exists:
```bash
ls -la products.csv
head -5 products.csv
```

### "Printer not responding"
1. Check printer is powered on
2. Check USB cable is connected
3. Try unplugging and replugging the USB cable
4. Rediscover the printer:
   ```bash
   python3 -c "from brother_ql.backends.helpers import discover; print(list(discover('pyusb')))"
   ```

### Labels print blank
1. Check that you have the correct label tape installed
2. Try adjusting the threshold in the code (line 118 in print_labels.py)
3. Generate a preview first to verify the image is created correctly

---

## Using the Helper Script

Make the script executable:
```bash
chmod +x run_printer.sh
```

Then use it (note: you'll still need sudo):
```bash
sudo ./run_printer.sh test          # Test print
sudo ./run_printer.sh batch 1 10    # Print products 1-10
sudo ./run_printer.sh preview       # Generate previews
sudo ./run_printer.sh all           # Print all products
```

---

## Next Steps

**Right now, try this:**
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
sudo python3 print_labels.py products.csv --test
```

This should print your first label! If it works, you're all set to start printing.
