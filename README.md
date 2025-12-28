# Brother QL-700 Label Printer Web Interface

A modern web-based interface for printing labels with QR codes using Brother QL-700 printers. Upload CSV files, preview labels, and batch print with an intuitive UI.

![Label Printer Interface](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- 🖨️ **Web Interface**: Modern, responsive UI for label printing
- 📊 **CSV Upload**: Upload product lists and select columns for labels
- 🔍 **Live Preview**: See exactly how labels will look before printing
- 📱 **QR Code Support**: Automatic QR code generation with product data
- 🔄 **Batch Processing**: Print labels in batches with progress tracking
- 🖥️ **Printer Detection**: Automatic USB printer discovery
- 📝 **Real-time Logs**: Monitor printing progress and errors

## Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- Brother QL-700 printer connected via USB
- Compatible OS: Linux, macOS, or Windows

### 2. Installation

Clone the repository:
```bash
git clone https://github.com/your-username/brother_printer_wrapper.git
cd brother_printer_wrapper
```

**Option A: Automatic Setup (Recommended)**

For Linux/macOS:
```bash
chmod +x scripts/setup_unix.sh
./scripts/setup_unix.sh
```

For Windows:
```bash
scripts/setup_windows.bat
```

**Option B: Manual Setup**

Install Python dependencies:
```bash
pip install -r requirements.txt
```

For Linux, install USB libraries:
```bash
sudo apt-get install libusb-1.0-0  # Ubuntu/Debian
# or
sudo dnf install libusb            # Fedora/RHEL
```

For macOS with Homebrew:
```bash
brew install libusb
```

### 3. Run the Application

**Web Interface (Recommended):**
```bash
cd webapp
python app.py
```
Then open http://localhost:5000 in your browser.

**Command Line:**
```bash
# Test print
python scripts/print_labels.py sample_data.csv --test

# Print all labels
python scripts/print_labels.py your_data.csv
```

## Usage Guide

### Web Interface

1. **Upload CSV**: Click "Upload" and select your CSV file with product data
2. **Select Columns**: Choose which columns to include on labels
3. **Configure Settings**: 
   - Toggle QR code on/off
   - Set batch size and range
4. **Preview**: Generate a preview to see how labels will look
5. **Detect Printer**: Click "Detect Printers" to find your Brother QL-700
6. **Print**: Click "Start Print" to begin batch printing

### CSV Format

Your CSV file should have a header row. Example:

```csv
Product Name,SKU,Price
"Premium Coffee Beans",SKU001,"$12.99"
"Organic Tea Leaves",SKU002,"$8.50"
```

### Command Line Options

```bash
# Basic usage
python scripts/print_labels.py data.csv

# Test single label
python scripts/print_labels.py data.csv --test

# Custom printer
python scripts/print_labels.py data.csv --printer "usb://0x04f9:0x2042"

# Print range
python scripts/print_labels_enhanced.py data.csv --start 1 --end 100

# Generate previews
python scripts/print_labels_enhanced.py data.csv --preview
```

## Label Specifications

- **Size**: 62mm continuous labels (default)
- **Layout**: Product text on left, QR code on right
- **QR Code**: Contains full product information
- **Font**: Bold, auto-sized to fit available space
- **Supported Sizes**: 29mm, 38mm, 62mm continuous; various die-cut sizes

## Troubleshooting

### Printer Not Found
```bash
# Check USB connection
lsusb | grep Brother

# Discover printers
brother_ql discover
```

### Permission Issues (Linux)
```bash
# Add user to printer group
sudo usermod -a -G lp $USER

# Create udev rule
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="2042", MODE="0666"' | sudo tee /etc/udev/rules.d/99-brother-ql.rules
sudo udevadm control --reload-rules
```

### Font Issues
The application automatically tries multiple font paths:
- macOS: `/System/Library/Fonts/Helvetica.ttc`
- Linux: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
- Windows: `C:\\Windows\\Fonts\\arialbd.ttf`

## Development

### Project Structure
```
brother_printer_wrapper/
├── webapp/                 # Web interface
│   ├── app.py             # Flask application
│   ├── templates/         # HTML templates
│   ├── static/           # CSS, JS, images
│   └── requirements.txt  # Web app dependencies
├── scripts/              # Command line tools
│   ├── print_labels.py   # Basic printing script
│   └── setup_*.sh        # Installation scripts
├── docs/                 # Documentation
└── README.md
```

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
cd webapp
python app.py
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request

## Security Notes

- The web interface runs locally and doesn't send data externally
- Uploaded CSV files are automatically deleted after printing
- File uploads are limited to 5MB and .csv files only
- No sensitive data is logged or stored permanently

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the `docs/` folder for detailed guides
- **Brother QL Library**: https://github.com/pklaus/brother_ql

## Acknowledgments

- Built with [brother_ql](https://github.com/pklaus/brother_ql) Python library
- QR code generation using [qrcode](https://pypi.org/project/qrcode/) library
- Web interface powered by Flask