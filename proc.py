#!/usr/bin/env python
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import ImageOps

from matplotlib import pyplot as plt 
from matplotlib import font_manager as fm
import os
from pathlib import Path
import sys
from datetime import datetime

def render(source_image, font, text, back_color, transparency):
    
    width, height = source_image.size

    canvas = Image.new(mode="RGBA", size=(width,height))
    
    canvas.paste(back_color, [0, 0, width, height]) #fill canvas with a background color

    idx = 0

    x, y = 0, 0
    asc, desc = font.getmetrics() #A tuple of the font ascent (the distance from the baseline to the highest outline point) and descent (the distance from the baseline to the lowest outline point, a negative value)
    asc -= 3 #offset

    while y < height:
        
        while x < width:
            c = text[idx]
            _,_,right,lower = font.getbbox(c)  # Returns four coordinates in the format (left, upper, right, lower)
            
            if (x + lower < width):
                r, g, b = source_image.getpixel((x, y))
                a = transparency
                
                ImageDraw.Draw(canvas).text(
                    (x, y),                #position
                    c,                     #character
                    fill=(r, g, b, a),     #font color
                    font=font              #font family
                )
                idx = (idx + 1) % len(text)

                x += right-1     #increment x
         
            else : break
        
        x = 0                   #reset x to left
        y += asc    #increment y

    return canvas



def plot_images(source_image, output_image):
    # create figure
    fig = plt.figure(figsize=(5, 5),facecolor='r')
    
    fig.add_subplot(1, 2, 1)
    plt.imshow(source_image)
    plt.axis('off')
    plt.title("Input")
    
    # showing image
    fig.add_subplot(1, 2, 2)
    plt.imshow(output_image)
    plt.axis('off')
    plt.title("Output")

    plt.show()

def wrap_html_img(path):
    return "<img id='im-out' src='{}' />".format(path)


def generate(input_path, text, fonts, font_size, back_color, save_output=True, show_plot=False):
    source_image = Image.open(input_path)
    source_image = ImageOps.exif_transpose(source_image)    #apply orientation rotations if present
    count = 0
    
    af = [f for f in fonts if ".ttf" in f]
    tot = len(af)
    for font in af:
        #print("Font: {}/{}".format(count, tot))
        f = ImageFont.truetype(font, font_size)
        #print("Processing Font Fam:{} using font-size:{}".format(f.getname(), i))
        result = render(source_image, f, text, back_color, transparency)

        if save_output and result:
            try :
                outfile_name = "File_{}_Fam_{}_Size_{}.png".format(input_path.stem, f.getname()[0], font_size)
                output_abs = "{}".format(os.path.join(output_path, outfile_name))
                result.save(output_abs)
                #os.chmod(output_abs, 0o777)
                print(os.path.join(output_dirname, outfile_name))
            except Exception as ex: 
                print(ex)

        if show_plot:
            plot_images(source_image, result)
            
                
        count += 1

    source_image.close()

def log(argv):
    sub_arg = argv[1::]
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    f = open(os.path.join(root_path, "logs", "log.txt"), "a")
    f.write("{};{}\n".format(now, ";".join(sub_arg)))   #write separate method to push this data also to database using python
    f.close()        
    
root_path = "/var/www/imagetextart/"
output_dirname = "output"
font_dirname = "font"
output_path = os.path.join(root_path, output_dirname)
fonts_dir = os.path.join(root_path, "font")
transparency = 256
min_font_size = 6
max_font_size = 128



#fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
fonts = [os.path.join(fonts_dir, "font.ttf")]
font_size = 30
show_plot = False
save_output = True

if (len(sys.argv) == 5):
    filename = sys.argv[1]
    input_path = Path(filename)
    text = sys.argv[2]
    font_size = sys.argv[3]
    back_color  = tuple(int(item) for item in sys.argv[4].split(','))

    log(sys.argv)

    font_size = int(font_size)

    if (font_size) < min_font_size:
        font_size = min_font_size
    elif (font_size > max_font_size):
        font_size = max_font_size

    generate(input_path, text, fonts, font_size, back_color, save_output, show_plot)
else:
    print("Invalid Arguments")