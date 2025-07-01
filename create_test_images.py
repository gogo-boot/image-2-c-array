#!/usr/bin/env python3
"""
Example script to test the image converter with a generated test image
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

def create_test_images():
    """Create some test images for demonstration"""
    
    # Create example directory structure
    base_dir = Path("example")
    
    # Create subdirectories
    (base_dir / "icons").mkdir(parents=True, exist_ok=True)
    (base_dir / "logos").mkdir(parents=True, exist_ok=True)
    (base_dir / "backgrounds").mkdir(parents=True, exist_ok=True)
    
    # Create a simple test icon
    img = Image.new('RGB', (32, 32), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, 24, 24], fill='blue', outline='black')
    img.save(base_dir / "icons" / "test_icon.png")
    print("Created: example/icons/test_icon.png")
    
    # Create a simple logo
    img = Image.new('RGB', (64, 32), color='red')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "LOGO", fill='white')
    img.save(base_dir / "logos" / "company_logo.png")
    print("Created: example/logos/company_logo.png")
    
    # Create a gradient background
    img = Image.new('RGB', (128, 64), color='black')
    draw = ImageDraw.Draw(img)
    for i in range(128):
        color = int(255 * i / 128)
        draw.line([(i, 0), (i, 64)], fill=(color, color // 2, 255 - color))
    img.save(base_dir / "backgrounds" / "gradient.png")
    print("Created: example/backgrounds/gradient.png")
    
    # Create a simple pattern
    img = Image.new('RGB', (16, 16), color='white')
    draw = ImageDraw.Draw(img)
    for x in range(0, 16, 2):
        for y in range(0, 16, 2):
            if (x + y) % 4 == 0:
                draw.rectangle([x, y, x+1, y+1], fill='black')
    img.save(base_dir / "pattern.png")
    print("Created: example/pattern.png")
    
    print("\nTest images created! Now run:")
    print("python image_converter.py example/ output/")

if __name__ == "__main__":
    create_test_images()
