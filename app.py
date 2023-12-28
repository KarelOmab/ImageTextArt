from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import io
from base64 import b64encode

app = Flask(__name__)

def create_text_image(image_path, text, font_name, font_scalar):
    # Load the original image
    original_image = Image.open(image_path)

    # Apply orientation from EXIF data, if present
    original_image = ImageOps.exif_transpose(original_image)

    width, height = original_image.size

    if width > height:
        # Calculate font size based on image height and scalar value
        font_size = int(height * font_scalar)
    else:
        # Calculate font size based on image width and scalar value
        font_size = int(width * font_scalar)

    # Load the font
    try:
        font = ImageFont.truetype(font_name, font_size)
    except IOError:
        print(f"Could not load font '{font_name}'. Using default font.")
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
    new_image.save('output.png')
    return original_image, new_image

@app.route('/', methods=['GET', 'POST'])
def index():
    original_image_encoded = None
    generated_image_encoded = None

    if request.method == 'POST':
        # Process the form data and generate the image
        image_file = request.files['image']
        text = request.form['text']
        font_name = request.form['font_family']     
        font_scalar = float(request.form['font_scalar'])

        if image_file:
            image_path = os.path.join('uploads', image_file.filename)
            image_file.save(image_path)
            
            # Generate text image
            original_image, generated_image = create_text_image(image_path, text, font_name, font_scalar)
            original_image_encoded = encode_image(original_image)
            generated_image_encoded = encode_image(generated_image)

    return render_template('index.html', original_image=original_image_encoded, generated_image=generated_image_encoded)

def encode_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # Save as PNG
    img_byte_arr = img_byte_arr.getvalue()
    encoded_img = b64encode(img_byte_arr).decode('ascii')
    return f"data:image/png;base64,{encoded_img}"

if __name__ == '__main__':
    app.run(debug=True)
