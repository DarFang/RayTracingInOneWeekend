#!/usr/bin/env python3
"""
Convert PPM to PNG for easy viewing
"""
import sys
from PIL import Image
import numpy as np

def read_ppm(ppm_file):
    """Read PPM file and return image data"""
    # Try different encodings to handle Windows BOM issues
    encodings = ['utf-8', 'utf-16', 'utf-16le', 'utf-16be']
    
    for encoding in encodings:
        try:
            with open(ppm_file, 'r', encoding=encoding) as f:
                # Read header
                magic = f.readline().strip()
                if magic != 'P3':
                    continue  # Try next encoding
                
                # Read dimensions
                width, height = map(int, f.readline().split())
                
                # Read max value
                max_val = int(f.readline().strip())
                
                # Read pixel data
                pixels = []
                for line in f:
                    pixels.extend(map(int, line.split()))
                
                # Convert to image
                img_array = np.array(pixels).reshape(height, width, 3)
                return Image.fromarray(img_array.astype(np.uint8))
                
        except (UnicodeError, ValueError) as e:
            continue
    
    raise ValueError(f"Could not read PPM file with any encoding. File may be corrupted.")

def ppm_to_png(ppm_file, png_file=None):
    """Convert PPM file to PNG"""
    if png_file is None:
        png_file = ppm_file.replace('.ppm', '.png')
    
    try:
        img = read_ppm(ppm_file)
        img.save(png_file)
        print(f"✅ Converted {ppm_file} to {png_file}")
        print(f"📏 Image size: {img.size[0]}x{img.size[1]} pixels")
        return True
    except Exception as e:
        print(f"❌ Error converting {ppm_file}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ppm_to_png.py <ppm_file> [png_file]")
        print("Example: python ppm_to_png.py image.ppm")
        sys.exit(1)
    
    ppm_file = sys.argv[1]
    png_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = ppm_to_png(ppm_file, png_file)
    sys.exit(0 if success else 1) 