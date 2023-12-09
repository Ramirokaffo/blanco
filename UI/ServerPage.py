
from datetime import datetime
from tkinter import *

from STATIC.ConstantFile import couleur_sous_fenetre
from Service.ImageService import ImageService
from Service.QRCodeService import QRCodeService
from Service.ServerService import ServerService

from Service.WIFIService import WIFIService


class ServerPage(Frame):
    server_page_list = []

    def __init__(self, master):
        super().__init__(master)
        ServerPage.server_page_list.append(self)
        self.start_date: datetime | None = None
        self.port = 9090
        self.configure(bg=couleur_sous_fenetre)
        self.frame_in_server = Frame(master, bg=couleur_sous_fenetre)
        self.my_photo_image = None
        self.qr_code_label = Label(self.frame_in_server, compound=BOTTOM)
        self.duration_variable = StringVar()
        self.duration_label = Label(self.frame_in_server, textvariable=self.duration_variable)

        self.start_server_button = Button(self.frame_in_server, text="Démarer le serveur",
                                          command=lambda: self.start_server(), bg=couleur_sous_fenetre
                                          )
        self.start_server_button.pack()
        # self.stop_server_button = Button(self.frame_in_server, text="Arreter le serveur",
        #                                  command=lambda: ServerService.stop_server()
        #                                  )
        # self.stop_server_button.pack()

    def start_server(self):
        ip = WIFIService.get_local_ip()
        ServerService.qr_code_path = QRCodeService.create_code(f"{ip}:{self.port}")
        ServerService().start_server(ip)
        self.my_photo_image = ImageService.resize_image(master=self.qr_code_label, image_path=ServerService.qr_code_path, height=500, width=500)
        self.qr_code_label.config(text="Scannez ce code QR pour vous connecter au serveur", image=self.my_photo_image, compound=TOP)
        self.qr_code_label.pack()
        self.start_server_button.config(text="Arreter le serveur et quitter l'application", command=lambda: ServerService.stop_server())
        self.duration_label.pack()
        self.start_date = datetime.now()
        self.show_duration()

    def displays(self):
        self.frame_in_server.pack(expand=YES)
        return self.master

    def show_duration(self):
        self.duration_variable.set(f"Le serveur est en marche depuis {datetime.now() - self.start_date}")
        self.duration_label.after(1000, self.show_duration)
