import shutil
import tkinter.filedialog
from tkinter import *
from tkinter import filedialog, messagebox

import PIL
from PIL import Image, ImageTk

from DATA.SettingClass.Product import Product
from DATA.SettingClass.ProductImage import ProductImage
from customtkinter import CTkScrollableFrame, CTkButton, CTkFrame

from STATIC.ConstantFile import couleur_sous_fenetre
from Service.ImageService import ImageService
from UI.Images.OneImageWidget import OneImageWidget


class ImageManager(LabelFrame):

    def __init__(self, master, images: list[ProductImage], label_anchor=N, width: int = 690, borderwidth: int = 0,
                 background: str = "white", is_view_mode: bool = True, product_id: int = None):
        super().__init__(master)
        self.my_height = 150
        self.my_width = 150
        self.is_view_mode = is_view_mode
        self.product_id = product_id
        self.images = images
        self.configure(text="Images du produit", labelanchor=label_anchor, bg=couleur_sous_fenetre, borderwidth=borderwidth)
        self.frame_list_image = CTkScrollableFrame(self, orientation=HORIZONTAL, width=width, label_anchor=CENTER,
                                                   fg_color=background, bg_color=couleur_sous_fenetre)
        self.frame_list_image.pack(side=TOP, anchor=CENTER, fill=X)
        self.add_image_widget = CTkFrame(self.frame_list_image, height=self.my_height, width=self.my_width)
        self.add_image_widget.pack(anchor=CENTER, ipady=self.my_height, ipadx=self.my_width / 4, side=RIGHT)
        self.add_image_button = CTkButton(self.add_image_widget, text="Ajouter", command=self.add_product_images)
        self.add_image_button.pack(expand=YES, anchor=CENTER)
        for i, product_image in enumerate(self.images):
            try:
                OneImageWidget(self.frame_list_image, images=self.images, index=i, width=self.my_width,
                           height=self.my_height, on_delete_image=self.delete_image, on_edit_image=self.edit_image
                           ).pack(side=LEFT)
            except:
                pass

    def delete_image(self, image_widget: OneImageWidget):
        if self.is_view_mode and self.product_id is not None:
            image_widget.product_image.delete_permanently()
        self.images.remove(image_widget.product_image)
        image_widget.destroy()

    def edit_image(self, image_widget: OneImageWidget):
        image_path = filedialog.askopenfilename(title="Selectionner l'image", initialdir="/",
                                                   filetypes=(("jpeg filles", "*.jpg"), ("png files", "*.png")                                                              ))
        if image_path:
            if self.is_view_mode and self.product_id is not None:
                ProductImage(id=image_widget.product_image.id, real_path=image_path).get_path_from_real_path().update()
                ImageService.save_from_local("product", image_path)
            image_widget.product_image.real_path = image_path
            image_widget.refresh_image()

    def add_product_images(self):
        images_paths = filedialog.askopenfilenames(title="Selectionner des images", initialdir="/",
                                                 filetypes=(("jpeg filles", "*.jpg"), ("png files", "*.png")))
        if len(images_paths) > 0:
            product_images_list = [ProductImage(real_path=path, product=Product(id=self.product_id)) for path in images_paths]
            if self.is_view_mode and self.product_id is not None:
                for product_image in product_images_list:
                    product_image.get_path_from_real_path()
                ProductImage.save_many_to_db(product_images_list)
                for product_image in product_images_list:
                    ImageService.save_from_local("product", product_image.real_path)
            for i, product_image in enumerate(product_images_list):
                OneImageWidget(self.frame_list_image, images=product_images_list, index=i, width=self.my_width,
                               height=self.my_height, on_delete_image=self.delete_image, on_edit_image=self.edit_image
                               ).pack(side=LEFT)
            self.images += product_images_list
        else:
            question = messagebox.askretrycancel("Erreur", "Vous avez choisi un format de fichier incorrect")
            if question:
                self.add_product_images()
