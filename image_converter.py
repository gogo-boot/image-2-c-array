#!/usr/bin/env python3
"""
ESP32 Image to C Array Converter

This script converts images to C array format suitable for ESP32 microcontrollers.
It recursively scans a source directory and converts all supported image files
while maintaining the directory structure in the output.

Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF
Output format: C header files with RGB565 format arrays
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import numpy as np


class ImageConverter:
    """Converts images to C array format for ESP32"""
    
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}
    
    def __init__(self, source_dir, output_dir):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def rgb888_to_rgb565(self, r, g, b):
        """Convert RGB888 to RGB565 format"""
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    
    def image_to_c_array(self, image_path):
        """Convert a single image to C array format"""
        try:
            # Open and convert image to RGB
            with Image.open(image_path) as img:
                # Convert to RGB if not already
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                width, height = img.size
                
                # Convert to numpy array
                img_array = np.array(img)
                
                # Generate variable name from filename
                var_name = Path(image_path).stem.replace('-', '_').replace(' ', '_')
                # Ensure valid C identifier
                if not var_name[0].isalpha() and var_name[0] != '_':
                    var_name = f"img_{var_name}"
                
                # Start building the C file content
                c_content = []
                c_content.append("/*")
                c_content.append(f" * Generated from: {Path(image_path).name}")
                c_content.append(f" * Image size: {width}x{height} pixels")
                c_content.append(f" * Format: RGB565")
                c_content.append(" */")
                c_content.append("")
                c_content.append("#pragma once")
                c_content.append("#include <stdint.h>")
                c_content.append("")
                c_content.append(f"#define {var_name.upper()}_WIDTH  {width}")
                c_content.append(f"#define {var_name.upper()}_HEIGHT {height}")
                c_content.append("")
                c_content.append(f"const uint16_t {var_name}_data[{width * height}] = {{")
                
                # Convert pixels to RGB565 and format as C array
                pixels = []
                for y in range(height):
                    row_pixels = []
                    for x in range(width):
                        r, g, b = img_array[y, x]
                        rgb565 = self.rgb888_to_rgb565(r, g, b)
                        row_pixels.append(f"0x{rgb565:04X}")
                    
                    # Add row with proper formatting
                    if y < height - 1:
                        pixels.append("    " + ", ".join(row_pixels) + ",")
                    else:
                        pixels.append("    " + ", ".join(row_pixels))
                
                c_content.extend(pixels)
                c_content.append("};")
                c_content.append("")
                
                # Add structure for easy access
                c_content.append(f"typedef struct {{")
                c_content.append(f"    const uint16_t* data;")
                c_content.append(f"    uint16_t width;")
                c_content.append(f"    uint16_t height;")
                c_content.append(f"}} {var_name}_t;")
                c_content.append("")
                c_content.append(f"const {var_name}_t {var_name} = {{")
                c_content.append(f"    .data = {var_name}_data,")
                c_content.append(f"    .width = {var_name.upper()}_WIDTH,")
                c_content.append(f"    .height = {var_name.upper()}_HEIGHT")
                c_content.append("};")
                
                return "\n".join(c_content)
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def convert_image_file(self, image_path, relative_path):
        """Convert a single image file and save the C header"""
        try:
            print(f"Converting: {relative_path}")
            
            # Generate C array content
            c_content = self.image_to_c_array(image_path)
            if c_content is None:
                return False
            
            # Create output path with .h extension
            output_file = self.output_dir / relative_path.with_suffix('.h')
            
            # Create output directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write C header file
            with open(output_file, 'w') as f:
                f.write(c_content)
            
            print(f"  -> Generated: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error converting {image_path}: {e}")
            return False
    
    def scan_and_convert(self):
        """Recursively scan source directory and convert all images"""
        converted_count = 0
        error_count = 0
        
        print(f"Scanning source directory: {self.source_dir}")
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Walk through all files in source directory
        for root, dirs, files in os.walk(self.source_dir):
            root_path = Path(root)
            
            for file in files:
                file_path = root_path / file
                
                # Check if file is a supported image format
                if file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                    # Calculate relative path from source directory
                    relative_path = file_path.relative_to(self.source_dir)
                    
                    if self.convert_image_file(file_path, relative_path):
                        converted_count += 1
                    else:
                        error_count += 1
        
        print()
        print(f"Conversion complete!")
        print(f"  Images converted: {converted_count}")
        print(f"  Errors: {error_count}")
        
        return converted_count, error_count


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Convert images to C arrays for ESP32",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python image_converter.py images/ output/
  python image_converter.py /path/to/images /path/to/output
        """
    )
    
    parser.add_argument(
        'source_dir',
        help='Source directory containing images to convert'
    )
    
    parser.add_argument(
        'output_dir',
        help='Output directory for generated C header files'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        # Create converter instance
        converter = ImageConverter(args.source_dir, args.output_dir)
        
        # Perform conversion
        converted, errors = converter.scan_and_convert()
        
        # Exit with error code if there were errors
        if errors > 0:
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
