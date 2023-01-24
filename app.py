from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    if request.method == 'POST':
        # Get the input values from the form
        image_file = request.files['image']
        text = request.form['text']
        font = request.form['font']
        font_size = int(request.form['font_size'])
        color = tuple(map(int, request.form['color'].split(',')))
        position = tuple(map(int, request.form['position'].split(',')))

        # Check if the image file is valid
        if not image_file:
            error = "Error: No image file selected."
        if not image_file.filename.endswith('.JPG'):
            error = "Error: Only jpg files are supported."

        # Check if the text is valid
        if not text:
            error = "Error: text is empty."

        # Check if the font is valid
        if not os.path.exists(font):
            error = f"Error: {font} does not exist."

        # Check if the font size is valid
        if font_size <= 0:
            error = "Error: font size is not valid."

        # Check if the color is valid
        if len(color) != 3:
            error = "Error: color is not valid."

        # Check if the position is valid
        if len(position) != 2:
            error = "Error: position is not valid."

        # Draw text on the image
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font, font_size)
        text_width, text_height = draw.textsize(text, font)
        text_x, text_y = position
        draw.text((text_x, text_y), text, font=font, fill=color)
        image.save(os.path.join(app.root_path, 'static', 'image_with_text.jpg'))
        return render_template('index.html', error=error)
    else:
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(port=3000)
