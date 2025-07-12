from PIL import Image, ImageDraw
import os

def crop_image_square(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    min_side = min(img.size)
    left = (img.width - min_side) // 2
    top = (img.height - min_side) // 2
    cropped = img.crop((left, top, left + min_side, top + min_side))
    cropped.save(output_path)

def crop_image_circle(image_path, output_path):
    square = Image.open(image_path).convert("RGBA")
    size = square.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result = Image.new('RGBA', size)
    result.paste(square, (0, 0), mask)
    result.save(output_path)
