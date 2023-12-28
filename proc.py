from PIL import Image, ImageDraw, ImageFont, ImageOps
import sys

def create_text_image(image_path, text, font_name, font_scalar):
    # Load the original image
    original_image = Image.open(image_path)

    # Apply orientation from EXIF data, if present
    original_image = ImageOps.exif_transpose(original_image)

    width, height = original_image.size

    # Calculate font size based on image height and scalar value
    font_size = int(height * font_scalar)

    # Load the font
    try:
        font = ImageFont.truetype(font_name, font_size)
    except IOError:
        print(f"Could not load font '{font_name}'. Using default font.")
        font = ImageFont.load_default()

    # Create a new blank image
    new_image = Image.new('RGB', (width, height), color=(0, 0, 0))

    # Prepare drawing context
    draw = ImageDraw.Draw(new_image)

    # Calculate text size
    char_width, char_height = draw.textsize("A", font=font)

    # Calculate the total number of iterations for progress tracking
    cols = (width + char_width - 1) // char_width
    rows = (height + char_height - 1) // char_height
    total_iterations = cols * rows
    current_iteration = 0

    # Write text on the new image
    idx = 0
    for y in range(0, height, char_height):
        for x in range(0, width, char_width):
            char = text[idx % len(text)]
            color = original_image.getpixel((x, y))
            draw.text((x, y), char, font=font, fill=color)
            idx += 1

            # Update and print progress
            current_iteration += 1
            progress = (current_iteration / total_iterations) * 100
            print(f"Progress: {progress:.2f}% complete", end='\r')

    # Save or display the resulting image
    new_image.show()  # or new_image.save('output.jpg')

# Example usage
if len(sys.argv) == 5:
    create_text_image(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]))
else:
    print("Usage: script.py image_path text font_name font_scalar")
