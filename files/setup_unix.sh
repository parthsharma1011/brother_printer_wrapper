#!/bin/bash
# Automatic Label Printer Setup for Brother QL-700 (Linux/macOS)

echo "============================================"
echo "Brother QL-700 Label Printer Setup"
echo "============================================"
echo ""

echo "Step 1: Installing required Python packages..."
pip3 install brother_ql qrcode[pil] pillow pyusb
echo ""

# Check OS for specific instructions
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Step 2: Linux-specific setup..."
    echo "Installing libusb..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y libusb-1.0-0
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y libusb
    fi
    
    echo ""
    echo "Setting up USB permissions..."
    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="2042", MODE="0666"' | sudo tee /etc/udev/rules.d/99-brother-ql.rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    
    echo ""
    echo "Adding user to lp group..."
    sudo usermod -a -G lp $USER
    
    echo ""
    echo "⚠️  You may need to log out and log back in for permissions to take effect."
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Step 2: macOS-specific setup..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install it from https://brew.sh"
    else
        echo "Installing libusb..."
        brew install libusb
    fi
fi

echo ""
echo "Step 3: Discovering printer..."
echo ""
brother_ql discover
echo ""

echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To print a test label, run:"
echo "  python3 print_labels.py products.csv --test"
echo ""
echo "To print all labels, run:"
echo "  python3 print_labels.py products.csv"
echo ""

# Make the Python script executable
chmod +x print_labels.py

echo "✓ print_labels.py is now executable"
echo ""
