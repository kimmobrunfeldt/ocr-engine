"""
Primitive OCR.
"""

import glob
import PIL
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

normalized_size = (50, 50)


def correct_pixels_ratio(image1, image2):
    total_pixels = 0
    correct_pixels = 0
    pix1 = image1.load()
    pix2 = image2.load()
    image1.getbbox

    for y in xrange(image1.size[0]):
        for x in xrange(image1.size[1]):
            total_pixels += 1
            if pix1[x, y][:3] == (0, 0, 0) and \
               pix1[x, y][:3] == pix2[x, y][:3]:
                correct_pixels += 1

    return float(correct_pixels) / total_pixels


def blacken(pixel, pix, x, y):
    """Converts pixels that are 'colorful enough' to black."""
    if pixel[0] < 240 and pixel[1] < 240 and pixel[2] < 240:
        # Color the pixel as black
        pix[x, y] = (0, 0, 0, 255)
    else:
        # Color as white
        pix[x, y] = (255, 255, 255, 255)


def white_to_alpha(pixel, pix, x, y):
    if pixel == (255, 255, 255, 255):
        pix[x, y] = (255, 255, 255, 0)


def pixel_transform(im, trans_func):
    pix = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            pixel = pix[x, y]
            trans_func(pixel, pix, x, y)


def normalize_image(im):
    """Normalizes image so it can be compared to others."""
    new_im = im.resize(normalized_size)
    pixel_transform(new_im, blacken)
    return new_im


def main():
    im = Image.open('3.png')
    new_im = normalize_image(im)
    new_im.save('9_new.png')

    for path in glob.glob('Photo*.jpg'):
        user_im = Image.open(path)
        user_im = ImageOps.invert(user_im)
        user_im = user_im.crop(user_im.getbbox())
        user_im = ImageOps.invert(user_im)

        user_im = normalize_image(user_im)
        if correct_pixels_ratio(new_im, user_im) > 0.1:
            user_im.save('new_' + path)



if __name__ == '__main__':
    main()
