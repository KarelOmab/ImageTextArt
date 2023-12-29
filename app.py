from flask import Flask, render_template, request
from textimageart import TextImageArt
import os

app = Flask(__name__)

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
            text_image_art = TextImageArt(font_name, font_scalar)
            original_image, generated_image = text_image_art.create_text_image(image_path, text)

            # Encode images to display in HTML
            original_image_encoded = text_image_art.encode_image(original_image)
            generated_image_encoded = text_image_art.encode_image(generated_image)

    return render_template('index.html', original_image=original_image_encoded, generated_image=generated_image_encoded)

if __name__ == '__main__':
    app.run(debug=True)
