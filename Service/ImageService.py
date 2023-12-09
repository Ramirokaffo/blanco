# import PIL
import os
import shutil

import PIL
from PIL import Image, ImageTk


def redimension_icone(icone, x, y):
    img = Image.open(icone)
    img = img.resize((x, y))
    img_pret = ImageTk.PhotoImage(img)
    return img_pret


class ImageService:

    @staticmethod
    def resize_image(master, image_path: str, width: float = 25, height: float = 25):
        img = PIL.Image.open(image_path)
        # img = img.resize((width, height))
        img.thumbnail((width, height))
        return ImageTk.PhotoImage(img, master=master)

    @staticmethod
    def get_saved_path(file_name: str, folder: str):
        image_path = os.path.join("image_app", folder, file_name)
        return os.path.join(os.getcwd().split("blanco")[0], "blanco", image_path)

    @staticmethod
    def save_from_local(folder: str, local_path):
        image_path = os.path.join("image_app", folder)
        shutil.copy(local_path, os.path.join(os.getcwd().split("blanco")[0], "blanco", image_path))

