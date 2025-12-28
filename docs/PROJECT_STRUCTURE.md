# Project Structure

```
brother_printer_wrapper/
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
│
├── webapp/                     # Web Interface
│   ├── app.py                  # Flask application
│   ├── print_utils.py          # Core printing utilities
│   ├── requirements.txt        # Web app specific dependencies
│   ├── templates/
│   │   └── index.html          # Main web interface
│   ├── static/
│   │   ├── styles.css          # Modern CSS styling
│   │   └── main.js             # JavaScript functionality
│   └── defaults/
│       └── sample.csv          # Sample data for testing
│
├── scripts/                    # Command Line Tools
│   ├── print_labels.py         # CLI printing script
│   ├── setup_unix.sh           # Linux/macOS setup
│   └── setup_windows.bat       # Windows setup
│
└── docs/                       # Documentation (optional)
    └── PROJECT_STRUCTURE.md    # This file
```

## Key Features

### Web Interface (`webapp/`)
- Modern, responsive design
- CSV upload and column selection
- Live label preview
- Printer auto-detection
- Real-time progress tracking
- Comprehensive error handling

### Command Line Interface (`scripts/`)
- Batch printing from CSV
- Test mode for single labels
- Printer discovery
- Flexible range selection
- Cross-platform compatibility

### Core Utilities (`webapp/print_utils.py`)
- Label image generation
- QR code creation
- Font handling across OS
- Printer communication
- Error handling and logging

## Security & Privacy

- No sensitive information stored
- Local processing only
- Automatic file cleanup
- Input validation and sanitization
- Secure file handling

## Cross-Platform Support

- **Linux**: Full support with USB permissions setup
- **macOS**: Native font support, Homebrew integration
- **Windows**: Zadig driver instructions included

## Dependencies

- `brother_ql`: Brother printer communication
- `qrcode`: QR code generation
- `Pillow`: Image processing
- `Flask`: Web interface
- `pyusb`: USB device communication