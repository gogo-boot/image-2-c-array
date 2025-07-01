# ESP32 Image to C Array Converter

This tool converts images to C array format suitable for ESP32 microcontrollers. It recursively scans a source directory and converts all supported image files while maintaining the directory structure in the output.

## Features

- **Recursive Directory Scanning**: Processes all images in subdirectories
- **Maintains Directory Structure**: Output mirrors the input directory structure
- **Multiple Image Formats**: Supports PNG, JPG, JPEG, BMP, GIF, TIFF
- **RGB565 Format**: Optimized for ESP32 displays
- **C Header Output**: Generates .h files ready to include in your ESP32 project

## Installation

1. Make sure you have Python 3.6+ installed

2. Create and activate a virtual environment (recommended):
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   # venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. When you're done, you can deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Usage

### Basic Usage
```bash
python image_converter.py <source_directory> <output_directory>
```

### Examples
```bash
# Convert all images in 'images' folder to 'output' folder
python image_converter.py images/ output/

# Convert with absolute paths
python image_converter.py /path/to/source/images /path/to/output/headers

# Enable verbose output
python image_converter.py images/ output/ --verbose
```

## Output Format

For each image file, the converter generates a C header file with:

- **Constants**: Width and height definitions
- **Data Array**: RGB565 pixel data as uint16_t array
- **Struct**: Convenient structure containing data pointer and dimensions

### Example Output

For an image named `logo.png`, the converter generates `logo.h`:

```c
/*
 * Generated from: logo.png
 * Image size: 64x32 pixels
 * Format: RGB565
 */

#pragma once
#include <stdint.h>

#define LOGO_WIDTH  64
#define LOGO_HEIGHT 32

const uint16_t logo_data[2048] = {
    0xF800, 0x07E0, 0x001F, // ... pixel data
};

typedef struct {
    const uint16_t* data;
    uint16_t width;
    uint16_t height;
} logo_t;

const logo_t logo = {
    .data = logo_data,
    .width = LOGO_WIDTH,
    .height = LOGO_HEIGHT
};
```

## Directory Structure Example

```
Source Directory:
images/
├── icons/
│   ├── home.png
│   └── settings.png
├── logos/
│   └── company_logo.jpg
└── splash.bmp

Output Directory:
output/
├── icons/
│   ├── home.h
│   └── settings.h
├── logos/
│   └── company_logo.h
└── splash.h
```

## ESP32 Integration

To use the generated headers in your ESP32 project:

1. Copy the generated .h files to your ESP32 project
2. Include the headers in your C/C++ files:
   ```c
   #include "logo.h"
   
   // Use the image data
   display_image(logo.data, logo.width, logo.height);
   ```

## RGB565 Format

The converter outputs images in RGB565 format, which is commonly used by ESP32 displays:
- 16 bits per pixel
- 5 bits for red (0-31)
- 6 bits for green (0-63) 
- 5 bits for blue (0-31)

This format provides good color depth while using half the memory of RGB888 format.

## Supported Image Formats

- PNG
- JPEG/JPG
- BMP
- GIF
- TIFF

The converter automatically handles format conversion and color space conversion to RGB.
