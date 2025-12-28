# Final Label Settings - MAXIMUM READABILITY

## 📏 Current Font Settings

### Font Sizes (Auto-Selected)
- **Maximum**: 60pt BOLD (for short names)
- **Options**: 60pt → 56pt → 52pt → 48pt → 44pt → 40pt
- **Minimum**: 40pt BOLD (25% LARGER than before!)

### Layout
- **Max Lines**: 2 lines (allows for much larger fonts)
- **QR Code**: 180x180 pixels (fixed, RIGHT side)
- **Text Area**: ~481 pixels wide (maximized, LEFT side)
- **Font**: Helvetica Bold (index 1) or Arial Black

---

## 🎯 What This Means

| Product Name Length | Font Size Used | Lines | Visibility |
|---------------------|----------------|-------|------------|
| Very Short (1-3 words) | **60pt BOLD** | 1 | Extremely visible |
| Short (4-6 words) | **56pt BOLD** | 1-2 | Very visible |
| Medium (7-10 words) | **48-52pt BOLD** | 2 | Highly visible |
| Long (11+ words) | **40-44pt BOLD** | 2 | Still very visible |

---

## 📊 Size Comparison

### Previous Settings:
- Max: 48pt → Min: 32pt (3 lines)

### **NEW Settings:**
- Max: **60pt** → Min: **40pt** (2 lines)
- **25% larger minimum font**
- **Fewer lines = larger text**

---

## ✅ Benefits

1. **Much larger text** - 60pt is HUGE and readable from far away
2. **Always bold** - Thick, easy-to-read font weight
3. **Won't cut off** - Limited to 2 lines, so text auto-wraps properly
4. **Consistent QR code** - Always 180x180px
5. **Maximum space used** - Text starts at 10px from edge

---

## 🎨 Label Layout

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

## 🚀 Test Now

Generate previews to see the new LARGE text:

```bash
cd /Users/parthsharma/Desktop/brother_printer/files
./run_printer.sh preview
open previews/
```

The text should now be:
- ✅ **BOLD and thick**
- ✅ **Very large** (40-60pt)
- ✅ **Never cut off** (max 2 lines)
- ✅ **Highly readable** from distance

---

## 📝 Example Products

**Short name:** "MUSK 15G"
- Font: **60pt BOLD**
- Lines: 1
- Result: HUGE text, extremely readable

**Medium name:** "AEKSHEA INCENSE STICKS - MUSK 15G"
- Font: **48-52pt BOLD**
- Lines: 2
- Result: Very large text, highly readable

**Long name:** "AEKSHEAINCENSE STICKS CHANDAN/SANDALWOOD 15G"
- Font: **40-44pt BOLD**
- Lines: 2
- Result: Large text, still very readable

---

All text will be **BOLD, LARGE, and READABLE**! 🎉
