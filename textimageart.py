from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat #pip install Pillow==9.3.0
import io
from base64 import b64encode

class TextImageArt:
    def __init__(self, font_name, font_scalar):
        self.font_name = font_name
        self.font_scalar = font_scalar

    def create_text_image(self, image_path, text):
        # Load the original image
        original_image = Image.open(image_path)

        # Apply orientation from EXIF data, if present
        original_image = ImageOps.exif_transpose(original_image)

        width, height = original_image.size

        if width > height:
            # Calculate font size based on image height and scalar value
            font_size = int(height * self.font_scalar)
        else:
            # Calculate font size based on image width and scalar value
            font_size = int(width * self.font_scalar)

        # Load the font
        try:
            font = ImageFont.truetype(self.font_name, font_size)
        except IOError:
            print(f"Could not load font '{self.font_name}'. Using default font.")
            font = ImageFont.load_default()

        # Create a new blank image
        new_image = Image.new('RGB', (width, height), color=(64, 64, 64))

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
        #new_image.show()  # or new_image.save('output.jpg')
        #new_image.save('output.png')
        return original_image, new_image

    @staticmethod
    def encode_image(image):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_img = b64encode(img_byte_arr).decode('ascii')
        return f"data:image/png;base64,{encoded_img}"
