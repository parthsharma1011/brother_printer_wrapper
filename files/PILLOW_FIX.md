# Pillow Compatibility Fix

## ✅ Problem Solved

The Brother QL printer scripts were failing with this error:
```
AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'
```

## 🔧 What Was Fixed

**Root Cause**: Pillow 11.3.0 removed the `ANTIALIAS` attribute, but the brother_ql library (version 0.9.4) still uses it.

**Solution**: Downgraded Pillow from version 11.3.0 to 9.5.0, which still has the `ANTIALIAS` attribute.

**Command Used**:
```bash
pip install Pillow==9.5.0
```

## ✅ Current Status

- **Pillow version**: 9.5.0 (compatible)
- **brother_ql version**: 0.9.4
- **Scripts**: Ready to use

## 🚀 Next Steps - Test Your Printer

Now you can run your test print! Follow these steps:

### 1. Test Print (Recommended First)
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
./run_printer.sh test
```

You'll be prompted for your macOS password (for USB access). This will print **one label** to verify:
- Text is BOLD and LARGE (40-60pt)
- Text is printing HORIZONTALLY (not vertically)
- QR code is on the right side
- Text is readable

### 2. If Test Looks Good - Batch Print
```bash
./run_printer.sh batch 1 300
```

This prints products 1-300 in **continuous mode** (no cutting between labels).

### 3. Print All Products (1,271+)
```bash
./run_printer.sh all-no-cut
```

This will print all products continuously. Takes 2-3 hours.

---

## 📋 What You Should See Now

When you run the test print, you should see:

1. **Large, bold text** on the left side (40-60pt BOLD font)
2. **QR code** on the right side (180x180 pixels, fixed size)
3. **Horizontal printing** (rotated 90 degrees)
4. **No cutting** in batch mode (continuous roll)

Example label layout:
```
┌────────────────────────────────────────────────┐
│                                                │
│ VERY LARGE TEXT           ████████████████    │
│ CONTINUES HERE            ████████████████    │
│                           ████████████████    │
│                           ████████████████    │
│                                                │
└────────────────────────────────────────────────┘
   (40-60pt BOLD)              (180x180px QR)
```

---

## ⚠️ Important Notes

1. **Use sudo**: All print commands require your password on macOS
2. **Test first**: Always print one label before running batches
3. **Continuous printing**: Batch commands use `--no-cut` to avoid jamming
4. **Manual cutting**: You'll cut labels manually with scissors after printing

---

## 🎯 All Fixed Issues

✅ USB permission errors (fixed with sudo)
✅ Python module imports (fixed with conda Python path)
✅ Continuous printing (added --no-cut flag)
✅ Bold font rendering (using Helvetica Bold, TTC index 1)
✅ Font sizes too small (increased to 40-60pt)
✅ Vertical text printing (changed rotation from 0° to 90°)
✅ Pillow compatibility (downgraded to 9.5.0)

---

## 📝 Commands Summary

| Command | Description |
|---------|-------------|
| `./run_printer.sh test` | Print one label (test) |
| `./run_printer.sh preview` | Generate preview images (no printer) |
| `./run_printer.sh batch 1 100` | Print products 1-100 (no cutting) |
| `./run_printer.sh batch-cut 1 50` | Print products 1-50 (with cutting) |
| `./run_printer.sh all-no-cut` | Print all products (no cutting) |

---

**You're ready to print! Run the test command now.** 🚀
