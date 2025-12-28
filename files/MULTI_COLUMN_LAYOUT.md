# Multi-Column Label Layout - Brother QL-700

## ✅ Layout Description

The new layout arranges products **HORIZONTALLY side-by-side** on each label, matching your printed example.

### Layout Structure:
```
┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│   ████████   │   ████████   │   ████████   │
│   ████████   │   ████████   │   ████████   │
│   QR CODE    │   QR CODE    │   QR CODE    │
│   ████████   │   ████████   │   ████████   │
│              │              │              │
│      A       │      A       │      A       │
│      E       │      E       │      E       │
│      K       │      K       │      K       │
│      S       │      S       │      S       │
│      H       │      H       │      H       │
│      E       │      E       │      E       │
│      A       │      A       │      A       │
│              │              │              │
│      M       │      O       │      Y       │
│      U       │      U       │      O       │
│      S       │      D       │      G       │
│      K       │      H       │      A       │
│              │              │              │
└──────────────┴──────────────┴──────────────┘
  Product 1      Product 2      Product 3
```

## 📐 Specifications

- **Products per label**: 3 (default) or 6 (smaller)
- **QR code**: Top of each column, centered
- **Text**: Below QR code, rotated 90° (reads from bottom to top)
- **Font**: Helvetica Bold
- **Separators**: Thin vertical lines between columns

## 🚀 Commands

### Test with 3 products per label (Recommended):
```bash
cd /Users/parthsharma/Desktop/brother_printer/files
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --test
```

### Test with 6 products per label (more compact):
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --test --per-label 6
```

### Print all with 3 per label:
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --no-cut
```

### Print all with 6 per label:
```bash
sudo /Users/parthsharma/anaconda3/bin/python3 print_labels_4up.py products.csv --no-cut --per-label 6
```

## 📊 Tape Savings

**With 3 products per label:**
- 1,271 products ÷ 3 = ~424 labels
- Saves ~67% of label tape

**With 6 products per label:**
- 1,271 products ÷ 6 = ~212 labels
- Saves ~83% of label tape

## ⚠️ Important Notes

1. **Text orientation**: Text prints vertically (bottom to top) like in your example
2. **QR codes**: Positioned at the top of each column
3. **Column count**: Use 3 for larger text/QR, 6 for maximum space savings
4. **Continuous printing**: Use `--no-cut` to avoid jamming
