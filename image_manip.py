import math
import time

from PIL import Image, ImageDraw, ImageOps

BORDER_SIZE = (10, 10, 10, 10)
MAX_SIDE_LENGTH = 1920


def is_valid_image(file_name):
    # small delay to let files close before working with them
    time.sleep(1)
    try:
        with Image.open(file_name) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False


def add_border(img: Image.Image | str) -> Image:
    if isinstance(img, str):
        img = Image.open(img)

    color = "white"

    new_img = ImageOps.expand(img, border=BORDER_SIZE, fill=color)

    return new_img


# code from https://stackoverflow.com/a/75428526
def add_border_rounded(
    img: Image.Image | str, rad=16, bg=True, bgCol="white", bgPix=16
) -> Image:
    if isinstance(img, str):
        img = Image.open(img)
    bg_im = Image.new("RGB", tuple(x + (bgPix * 2) for x in img.size), bgCol)
    ims = [img if not bg else img, bg_im]
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    for i in ims:
        alpha = Image.new("L", i.size, "white")
        w, h = i.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        i.putalpha(alpha)
    bg_im.paste(img, (bgPix, bgPix), img)
    return img if not bg else bg_im


def resize_image(img: Image.Image | str) -> Image:
    if isinstance(img, str):
        img = Image.open(img)

    portrait = False

    if img.height > img.width:
        img = img.rotate(angle=90, expand=True)
        portrait = True

    if img.width > MAX_SIDE_LENGTH:
        factor = MAX_SIDE_LENGTH / img.width
        new_width = math.floor(img.width * factor)
        new_height = math.floor(img.height * factor)
        img = img.resize((new_width, new_height))

    if portrait:
        img = img.rotate(angle=270, expand=True)

    return img


def save_image(img: Image.Image | str, filename="tmp.webp") -> str:
    if isinstance(img, str):
        img = Image.open(img)

    img.save(filename)
    return filename


if __name__ == "__main__":
    new_img = add_border_rounded("test.webp")
    new_img = resize_image(new_img)
    # new_img.save("test_image_result.jpg")
    new_img.show()
