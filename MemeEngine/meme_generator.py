"""Module for MemeGenerator Class."""
from PIL import Image, ImageDraw, ImageFont
import random

class MemeGenerator:
    """MemeGenerator generates a meme from an image and text."""

    def __init__(self, path, font_path = "./_data/font/RobotoCondensed-BoldItalic.ttf"):
        """Create a MemeGenerator object with specific path and font.

        :param path: directory for saving image
        :param font_path: destination of font file"""
        self.out_dir = path
        self.font_path = font_path


    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Generate meme with given path, body, author and width.

        :param img_path: path stores image
        :param text: body of quote text
        :param author: author of quote
        :param width: desired image width
        :return: location of saved file
        """
        out_path = f"{self.out_dir}/{random.randint(0,1000000)}.jpg"
        width = 500
        try:
            with Image.open(img_path) as img:
                # resize image
                ratio = width / float(img.size[0])
                height = int(ratio * float(img.size[1]))
                img = img.resize((width, height), Image.NEAREST)
                
                message = f'"{text}" - {author}'
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(self.font_path, 22)
                # adding quote body and quote author to the image
                draw.text((width / 6, height / 1.2), message, font=font, fill='black')
                img.save(out_path)
                
        except Exception:
            raise ValueError("Invalid image path")

        return out_path