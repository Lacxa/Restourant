import qrcode
from kivy.graphics.svg import Window

from kivymd.app import MDApp

Window.size = [420, 740]


class Main(MDApp):

    def qrcode(self, food):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        data = food
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="green", back_color="white")

        img.save("qr_code.png")

        sm = self.root
        sm.current = "qr"



Main().run()
