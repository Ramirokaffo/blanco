import os

import qrcode


class QRCodeService:

    @staticmethod
    def create_code(data: str, path: str = os.path.join("qr-ip.png")):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path)
        # print("path: ", path)
        return path


# QRCodeService.create_code(data="TOTO")