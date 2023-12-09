from tkinter import *
from tkinter import filedialog

import PIL
from PIL import Image, ImageTk


from DATA.SettingClass.ProductImage import ProductImage
from STATIC.ConstantFile import *
from Service.ImageService import ImageService


class OneImageWidget(Label):
    current_index = 2

    def __init__(self, master, images: list[ProductImage], index: int, height, width, on_delete_image, on_edit_image
                 ):
        super().__init__(master, height=height, width=width)
        self.height = height
        self.width = width
        self.product_image = images[index]
        if self.product_image.path is not None:
            self.product_image.load_local_path()
        self.my_photo_image = ImageService.resize_image(master=self, image_path=self.product_image.real_path, height=height, width=width)
        self.image_label_frame = LabelFrame(self)
        self.configure(cursor="target")

        self.label_widget = Frame(self.image_label_frame)
        # self.delete_icon = ImageService.resize_image(self.label_widget, image_suppression_noir, height=15, width=15)
        self.delete_icon = ImageService.resize_image(self.label_widget, image_suppression, height=15, width=15)
        # self.delete_icon = ImageService.resize_image(self.label_widget, image_suppression_noir_croix, height=15, width=15)
        self.edit_icon = ImageService.resize_image(self.label_widget, image_dossier, height=20, width=20)
        Button(self.label_widget, image=self.delete_icon, relief=FLAT, command=lambda: on_delete_image(self)).pack(side=LEFT)
        Button(self.label_widget, image=self.edit_icon, relief=FLAT, command=lambda: on_edit_image(self)).pack(side=RIGHT)
        self.image_label_frame["labelwidget"] = self.label_widget
        self.image_label_frame.pack()

        self.one_image = Label(self.image_label_frame, height=height, width=height, image=self.my_photo_image)
        self.one_image.pack(side=LEFT)
        self.one_image.bind("<ButtonRelease-1>", self.show_full_screen)

    def show_full_screen(self, even):
        def quit_img(event):
            fenetre_photo.destroy()

        fenetre_photo = Toplevel(self)
        fenetre_photo.attributes("-fullscreen", True)
        image = PIL.Image.open(self.product_image.real_path)
        z, s = self.winfo_screenheight(), self.winfo_screenwidth()
        x, y = image.size
        if x == y and x <= s:
            image = image.resize((z, z))
            photo = ImageTk.PhotoImage(image)
            canevas_affichage_photo = Canvas(fenetre_photo, height=z, width=z)
            canevas_affichage_photo.create_image(z / 2, z / 2, image=photo)
            canevas_affichage_photo.image = photo
            canevas_affichage_photo.pack(expand=YES)
            canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
        elif y > z:
            a = str((z / y) * x).split(".")
            image = image.resize((int(a[0]), z))
            photo = ImageTk.PhotoImage(image)
            canevas_affichage_photo = Canvas(fenetre_photo, height=z, width=x)
            canevas_affichage_photo.create_image(x / 2, z / 2, image=photo)
            canevas_affichage_photo.image = photo
            canevas_affichage_photo.pack(expand=YES)
            canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
        elif s >= x >= y and y <= z:
            a = str((s / x) * y).split(".")
            if int(a[0]) < z:
                image = image.resize((s, int(a[0])))
                photo = ImageTk.PhotoImage(image)
                canevas_affichage_photo = Canvas(fenetre_photo, height=int(a[0]), width=s)
                canevas_affichage_photo.create_image(s / 2, int(a[0]) / 2, image=photo)
                canevas_affichage_photo.image = photo
                canevas_affichage_photo.pack(expand=YES)
                canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
            else:
                image = image.resize((s, z))
                photo = ImageTk.PhotoImage(image)
                canevas_affichage_photo = Canvas(fenetre_photo, height=z, width=s)
                canevas_affichage_photo.create_image(s / 2, z / 2, image=photo)
                canevas_affichage_photo.image = photo
                canevas_affichage_photo.pack(expand=YES)
                canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
        elif x <= s and z >= y >= x:
            a = str((z / y) * x).split(".")
            image = image.resize((int(a[0]), z))
            photo = ImageTk.PhotoImage(image)
            canevas_affichage_photo = Canvas(fenetre_photo, height=z, width=int(a[0]))
            canevas_affichage_photo.create_image(int(a[0]) / 2, z / 2, image=photo)
            canevas_affichage_photo.image = photo
            canevas_affichage_photo.pack(expand=YES)
            canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
        else:
            a = str((s / x) * y).split(".")
            image = image.resize((s, int(a[0])))
            photo = ImageTk.PhotoImage(image)
            canevas_affichage_photo = Canvas(fenetre_photo, height=y, width=s)
            canevas_affichage_photo.create_image(s / 2, z / 2, image=photo)
            canevas_affichage_photo.image = photo
            canevas_affichage_photo.pack(expand=YES)
            canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
        canevas_affichage_photo.bind("<Double-ButtonRelease-1>", quit_img)
        fenetre_photo.bind("<Double-ButtonRelease-1>", quit_img)

    def refresh_image(self):
        self.my_photo_image = ImageService.resize_image(master=self, image_path=self.product_image.real_path,
                                                        height=self.height, width=self.width)
        self.one_image.configure(image=self.my_photo_image)


        # self.but = Button()

    # def delete_image(self, images: list[ProductImage]):
    #     print(len(images))
    #     images.remove(self.product_image)
    #     self.destroy()
    #
    # def edit_image(self, images: list[ProductImage]):
    #     print(len(images))
        # image_path = filedialog.askopenfilename(title="Selectionner l'image", initialdir="/",
        #                                            filetypes=(("jpeg filles", "*.jpg"), ("png files", "*.png")
        #                                                       # , ("all files", "*.*")
        #                                                       ))
        # if image_path:





