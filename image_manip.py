import math

from PIL import Image, ImageOps

BORDER_SIZE = (10, 10, 10, 10)
MAX_SIDE_LENGTH = 1920


def is_valid_image(file_name):
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
    new_img = add_border("test.webp")
    new_img = resize_image(new_img)
    # new_img.save("test_image_result.jpg")
    new_img.show()
