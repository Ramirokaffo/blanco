from tkinter import *
#
# from Service.ImageService import ImageService
# from Service.QRCodeService import QRCodeService
# from Service.WIFIService import WIFIService
# from Service.WebSocketService import WebSocketService
# import asyncio
#
# def save():
#     pass
#
# def reload():
#     WebSocketService.service.qr_code_path = QRCodeService.create_code(f"{WIFIService.get_local_ip()}:")
#     img_label.config(image=ImageService.resize_image(WebSocketService.qr_code_path, 300, 300))
#     # asyncio.run(WebSocketService().connect())
#     WebSocketService().connect()
#     pass
#
#
# def send():
#
#     asyncio.run(WebSocketService().send_data("Oui c'est bien le serveur"))
#
#     pass
#
from UI.DailyInventory.DailyInventoryForm import DailyInventoryForm
from UI.Product.ProductDetailsPage import ProductDetailsPage
from UI.Users.Client.ClientTable import ClientTable

app = Tk()

# ClientTable(app,).pack()
DailyInventoryForm(app,).pack()
# ProductDetailsPage(app, product_id=7776).pack()
# img_label = Label(app, image=ImageService.resize_image(WebSocketService.qr_code_path, 300, 300))
# img_label.pack()
# #
# print("Je suis ici")
# boutton = Button(app, text="Start", command=lambda: reload())
# boutton.pack()
#
# boutton = Button(app, text="Envoyer", command=lambda: send())
# boutton.pack()


app.mainloop()
# from tkinter import simpledialog
#
# new_value = simpledialog.askfloat(title="nom_ets", prompt="Montant de la tranche")
