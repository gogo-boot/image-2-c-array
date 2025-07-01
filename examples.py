#!/usr/bin/env python3
"""
Usage examples for the ESP32 Image Converter
"""

import os
import sys
from pathlib import Path

def show_usage():
    """Show usage examples"""
    print("ESP32 Image Converter - Usage Examples")
    print("=" * 40)
    print()
    
    print("1. Basic conversion:")
    print("   python image_converter.py source_folder/ output_folder/")
    print()
    
    print("2. Real-world examples:")
    print("   python image_converter.py assets/images/ src/generated/")
    print("   python image_converter.py ~/Pictures/icons/ esp32_project/include/images/")
    print()
    
    print("3. With verbose output:")
    print("   python image_converter.py images/ output/ --verbose")
    print()
    
    print("4. Convert current directory:")
    print("   python image_converter.py . output/")
    print()
    
    print("Supported image formats:")
    print("  - PNG (.png)")
    print("  - JPEG (.jpg, .jpeg)")
    print("  - BMP (.bmp)")
    print("  - GIF (.gif)")
    print("  - TIFF (.tiff)")
    print()
    
    print("Output format:")
    print("  - RGB565 format (16-bit per pixel)")
    print("  - C header files (.h)")
    print("  - Ready for ESP32 inclusion")
    print()
    
    print("Directory structure is preserved:")
    print("  Input:  images/icons/home.png")
    print("  Output: output/icons/home.h")
    print()

def show_esp32_integration():
    """Show how to integrate with ESP32 projects"""
    print("ESP32 Integration Example")
    print("=" * 25)
    print()
    
    print("1. Include the generated header in your ESP32 code:")
    print()
    print("```c")
    print('#include "test_icon.h"')
    print()
    print("void display_icon() {")
    print("    // Use the generated constants")
    print("    printf(\"Icon size: %dx%d\\n\", TEST_ICON_WIDTH, TEST_ICON_HEIGHT);")
    print("    ")
    print("    // Access pixel data")
    print("    for (int i = 0; i < TEST_ICON_WIDTH * TEST_ICON_HEIGHT; i++) {")
    print("        uint16_t pixel = test_icon_data[i];")
    print("        // Send pixel to display...")
    print("    }")
    print("    ")
    print("    // Or use the convenience struct")
    print("    draw_image(test_icon.data, test_icon.width, test_icon.height);")
    print("}")
    print("```")
    print()
    
    print("2. RGB565 format details:")
    print("   - 16 bits per pixel")
    print("   - Red: 5 bits (0-31)")
    print("   - Green: 6 bits (0-63)")
    print("   - Blue: 5 bits (0-31)")
    print("   - Memory efficient for embedded systems")
    print()
    
    print("3. Example display function:")
    print()
    print("```c")
    print("void draw_rgb565_image(const uint16_t* data, int width, int height, int x, int y) {")
    print("    for (int row = 0; row < height; row++) {")
    print("        for (int col = 0; col < width; col++) {")
    print("            uint16_t pixel = data[row * width + col];")
    print("            // Extract RGB components")
    print("            uint8_t r = (pixel >> 11) & 0x1F;")
    print("            uint8_t g = (pixel >> 5) & 0x3F;")
    print("            uint8_t b = pixel & 0x1F;")
    print("            // Draw pixel at (x + col, y + row)")
    print("            tft_draw_pixel(x + col, y + row, pixel);")
    print("        }")
    print("    }")
    print("}")
    print("```")
    print()

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_usage()
        print()
        show_esp32_integration()
    else:
        show_usage()

if __name__ == "__main__":
    main()
