#!/bin/bash
# Easy printer control script

PRINTER_ID="usb://0x04f9:0x2042"
CSV_FILE="products.csv"
PYTHON_PATH="/Users/parthsharma/anaconda3/bin/python3"

case "$1" in
    "test")
        echo "Running test print..."
        echo "⚠️  This requires sudo/admin privileges on macOS"
        sudo "$PYTHON_PATH" print_labels.py "$CSV_FILE" --test --printer "$PRINTER_ID"
        ;;
    "all")
        echo "Printing all 1,271+ labels..."
        echo "This will take 2-3 hours. Press Ctrl+C to stop anytime."
        read -p "Continue? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "⚠️  This requires sudo/admin privileges on macOS"
            sudo "$PYTHON_PATH" print_labels.py "$CSV_FILE" --printer "$PRINTER_ID"
        fi
        ;;
    "all-no-cut")
        echo "Printing all 1,271+ labels in CONTINUOUS mode (no cutting)..."
        echo "This will take 2-3 hours. Press Ctrl+C to stop anytime."
        echo "⚠️  Labels will print continuously - you'll cut them manually later"
        read -p "Continue? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "⚠️  This requires sudo/admin privileges on macOS"
            sudo "$PYTHON_PATH" print_labels.py "$CSV_FILE" --printer "$PRINTER_ID" --no-cut
        fi
        ;;
    "batch")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: ./run_printer.sh batch START_NUM END_NUM"
            echo "Example: ./run_printer.sh batch 1 100"
            exit 1
        fi
        echo "Printing products $2 to $3..."
        echo "⚠️  This requires sudo/admin privileges on macOS"
        sudo "$PYTHON_PATH" print_labels_enhanced.py "$CSV_FILE" --start "$2" --end "$3" --printer "$PRINTER_ID" --no-cut
        ;;
    "batch-cut")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: ./run_printer.sh batch-cut START_NUM END_NUM"
            echo "Example: ./run_printer.sh batch-cut 1 100"
            exit 1
        fi
        echo "Printing products $2 to $3 with auto-cut..."
        echo "⚠️  This requires sudo/admin privileges on macOS"
        sudo "$PYTHON_PATH" print_labels_enhanced.py "$CSV_FILE" --start "$2" --end "$3" --printer "$PRINTER_ID"
        ;;
    "preview")
        echo "Generating preview images (no printer needed)..."
        "$PYTHON_PATH" print_labels_enhanced.py "$CSV_FILE" --preview
        ;;
    *)
        echo "Brother QL-700 Label Printer Control"
        echo "Usage: $0 {test|all|all-no-cut|batch|batch-cut|preview}"
        echo ""
        echo "Commands:"
        echo "  test        - Print one test label"
        echo "  all         - Print all labels with auto-cut (takes 2-3 hours)"
        echo "  all-no-cut  - Print all labels continuously without cutting"
        echo "  batch       - Print range WITHOUT cutting: $0 batch 1 100"
        echo "  batch-cut   - Print range WITH auto-cut: $0 batch-cut 1 100"
        echo "  preview     - Generate preview images"
        echo ""
        echo "Examples:"
        echo "  $0 test"
        echo "  $0 batch 1 300         # No cutting (recommended)"
        echo "  $0 batch-cut 1 50      # With cutting"
        echo "  $0 all-no-cut"
        ;;
esac