import re
import time

import qrcode
from kivy.base import EventLoop
from kivy.graphics.svg import Window
from kivy.properties import NumericProperty, StringProperty, DictProperty

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineIconListItem, OneLineListItem
from kivymd.uix.textfield import MDTextField

from database import FireBase as FB

Window.size = [1280, 800]


class RowCard(MDCard):
    date = StringProperty("")
    icon = StringProperty("")
    cate = StringProperty("")
    name = StringProperty("")
    price = StringProperty("")


class Order(MDCard):
    pass


class Table(MDCard):
    time = StringProperty("00:20")
    status = StringProperty("yet to order")
    number = StringProperty("01")
    guest_num = NumericProperty(0)
    guest = StringProperty("0")
    price = StringProperty("10,000Tsh")


class Empty(MDCard):
    number = StringProperty("07")


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 10 or not substring.isdigit():
            return

        if len(self.text) == 0:
            if substring != "0":
                return
        elif len(self.text) == 1:
            if substring != "7" and substring != "6":
                return

        return super(NumberOnlyField, self).insert_text(substring, from_undo=from_undo)


class Main(MDApp):
    size_x, size_y = Window.size

    design_link = "https://dribbble.com/shots/13927167-Waiter-App-contactless-dinning-experience/attachments/5537475?mode=media"
    # APP
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

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

    def spinner(self):
        spiner = self.root.ids.spine_del
        spiner.active = True
        print("user")

    def end_spine(self):
        spinier = self.root.ids.spine_del
        spinier.active = False

    """"def pending(self):
        pend = self.root.ids.pend
        pre = self.root.ids.pre
        comp = self.root.ids.comp

        pend.md_bg_color = "#ffd241"
        pre.md_bg_color = "white"
        comp.md_bg_color = "white"

    def prepare(self):
        pend = self.root.ids.pend
        pre = self.root.ids.pre
        comp = self.root.ids.comp

        pend.md_bg_color = "white"
        pre.md_bg_color = "#ffd241"
        comp.md_bg_color = "white"

    def complete(self):
        pend = self.root.ids.pend
        pre = self.root.ids.pre
        comp = self.root.ids.comp

        pend.md_bg_color = "white"
        pre.md_bg_color = "white"
        comp.md_bg_color = "#ffd241"""""

    def button_color(self, button_name):
        pend = self.root.ids.pend
        pre = self.root.ids.pre
        comp = self.root.ids.comp

        pend.md_bg_color = "white"
        pre.md_bg_color = "white"
        comp.md_bg_color = "white"

        if "Pending" in button_name.text:
            pend.md_bg_color = "#ffd241"
        elif "Complete" in button_name.text:
            comp.md_bg_color = "#ffd241"
        elif "Preparing" in button_name.text:
            pre.md_bg_color = "#ffd241"

    def order_category(self, button_name):
        fod = self.root.ids.fod
        drnk = self.root.ids.drnk

        fod.md_bg_color = "white"
        drnk.md_bg_color = "white"

        if "Food" in button_name.text:
            fod.md_bg_color = "#ffd241"
        elif "Drinks" in button_name.text:
            drnk.md_bg_color = "#ffd241"


    def orders(self):
        data = {"detail": {"time": "00:15", "icon": "table-chair", "price": "5"}}

        for i, y in data.items():
            self.root.ids.today.data.append(
                {
                    "viewclass": "RowCard",
                    "name": y["time"],
                    "icon": y["icon"],
                    "price": y["price"]

                }
            )

    def table(self):
        data = dict(detail={'time': "00:15", 'number': "01", 'price': "5000", 'guest': "2 guest", 'status': "served"},
                    date={'time': "00:15", 'number': "01", 'price': "5000", 'guest': "2 guest", 'status': "served"})

        for i, y in data.items():
            self.root.ids.test.data.append(
                {
                    "viewclass": "Table",
                    "number": y["number"],
                    "guest": y["guest"],
                    "price": y["price"],
                    "time": y["time"],
                    "status": y["status"]

                }
            )

    """ KEYBOARD INTEGRATION """

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    """
    
            LOGIN FUNCTIONS
    
    """

    def login_waiter(self, phone, password):
        data = FB.get_user(FB())

        if phone in data:
            if password == data[phone]["Waiter_Info"]["user_password"]:
                toast("Login Successfully")
                self.screen_capture("orders")
            else:
                toast("Wrong Password")
        else:
            toast("Waiter Not Available")
            self.end_spine()

    """
                LOGIN FUNCTIONS
    """

    """
            ORDER FUNCTIONS
    
    """

    def add_item(self):
        for i in range(3):
            self.root.ids.customers.data.append(
                {
                    "viewclass": "RowCard",
                    "name": str(i),
                    "price": "3",
                    "id": i
                }
            )

    """
            END ORDER FUNCTIONS
    
    """

    """ SCREEN FUNCTIONS """

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)


Main().run()
