import numpy as np
from skimage import exposure
import base64
from PIL import Image, ImageOps, ImageChops
from io import BytesIO


def data_uri_to_image(uri):
    encoded_data = uri.split(',')[1]
    image = base64.b64decode(encoded_data)
    return Image.open(BytesIO(image))


def replace_transparent_background(image):
    
    image_arr = np.array(image)

    has_no_alpha = len(image_arr.shape) < 3 or image_arr.shape[2] < 4
    if has_no_alpha:
        return image

    alpha1 = 0
    r2, g2, b2, alpha2 = 255, 255, 255, 255

    red, green, blue, alpha = image_arr[:, :, 0], image_arr[:, :, 1], image_arr[:, :, 2], image_arr[:, :, 3]
    mask = (alpha == alpha1)
    image_arr[:, :, :4][mask] = [r2, g2, b2, alpha2]

    return Image.fromarray(image_arr)


def trim_borders(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    
    return image


def pad_image(image):
    return ImageOps.expand(image, border=30, fill='#fff')


def resize_image(image):
    return image.resize((8, 8))


def invert_colors(image):
    return ImageOps.invert(image)


def scale_down_intensity(image):
    image_arr = np.array(image)
    image_arr = exposure.rescale_intensity(image_arr, out_range=(0, 16))
    return Image.fromarray(image_arr)

def to_grayscale(image):
    return image.convert('L')


def process_image(image_path):
    # Open the image directly from the file path
    image = Image.open(image_path)

    # Check if the image is empty (no content)
    is_empty = not image.getbbox()
    if is_empty:
        return None

    # Process the image with existing steps
    image = replace_transparent_background(image)
    image = trim_borders(image)
    image = pad_image(image)
    image = to_grayscale(image)
    image = invert_colors(image)
    image = resize_image(image)
    image = scale_down_intensity(image)

    return np.array([np.array(image).flatten()])


