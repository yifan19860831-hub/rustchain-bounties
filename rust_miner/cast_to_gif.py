#!/usr/bin/env python3
"""
Convert asciinema .cast file to GIF
"""

import json
import sys
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def parse_cast(cast_file):
    """Parse asciinema .cast file"""
    frames = []
    with open(cast_file, 'r', encoding='utf-8') as f:
        # Skip header
        header = json.loads(f.readline())
        width = header.get('width', 120)
        height = header.get('height', 40)
        
        # Read frames
        for line in f:
            frame = json.loads(line)
            frames.append(frame)
    
    return header, frames

def create_terminal_image(width, height, text, bg_color=(0, 0, 0), fg_color=(255, 255, 255)):
    """Create a terminal-like image with text"""
    # Use a monospace font
    font_size = 14
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate image size
    char_width = font_size * 0.6
    char_height = font_size * 1.2
    img_width = int(width * char_width) + 40
    img_height = int(height * char_height) + 40
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw text
    x, y = 20, 20
    for line in text.split('\n'):
        draw.text((x, y), line, font=font, fill=fg_color)
        y += int(char_height)
    
    return img

def cast_to_gif(cast_file, output_file, max_frames=100):
    """Convert .cast to GIF"""
    header, frames = parse_cast(cast_file)
    
    print(f"Converting {cast_file} to {output_file}")
    print(f"Terminal size: {header['width']}x{header['height']}")
    print(f"Total frames: {len(frames)}")
    
    # Accumulate text and create frames at intervals
    images = []
    current_text = ""
    last_timestamp = 0
    frame_count = 0
    
    # Sample frames to avoid too many
    sample_interval = max(1, len(frames) // max_frames)
    
    for i, (timestamp, event_type, data) in enumerate(frames):
        if event_type == 'o':  # Output event
            current_text += data
            
            if i % sample_interval == 0 or i == len(frames) - 1:
                img = create_terminal_image(
                    header['width'], 
                    header['height'], 
                    current_text[-500:]  # Last 500 chars to fit
                )
                images.append(img)
                frame_count += 1
    
    if images:
        # Save as GIF
        images[0].save(
            output_file,
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0
        )
        print(f"GIF created with {len(images)} frames")
    else:
        print("No frames to create GIF")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python cast_to_gif.py <input.cast> <output.gif>")
        sys.exit(1)
    
    cast_to_gif(sys.argv[1], sys.argv[2])
