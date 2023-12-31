import json
import re

from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

import network
from database import FireBase as FB

# Window.size = [1280, 800]
Window.size = [1000, 520]


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class RowCard(MDCard):
    date = StringProperty("")
    icon = StringProperty("")
    cate = StringProperty("")
    name = StringProperty("")
    price = StringProperty("")


class Order(MDCard):
    pass


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class NumericKeyboardLayout(FloatLayout):
    pass


class Deco(MDCard):
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

    # sign in
    password = StringProperty("")
    username = StringProperty("")

    # product
    quantity_text = StringProperty("1")
    item_selected = StringProperty("0")
    total_price = StringProperty("")

    category = StringProperty("")

    # user
    nodata = StringProperty("")
    user_category = StringProperty("")
    user_type = StringProperty("")

    def update_text(self, button_text):
        text_input = self.root.ids.input
        current_text = text_input.text
        text_input.text = current_text + button_text

    def delete_last_digit(self):
        text_input = self.root.ids.input
        current_text = text_input.text
        text_input.text = current_text[:-1]

    def on_start(self):
        self.keyboard_hooker()
        # self.display_users()
        self.get_users()
        # self.display_manage()
        # self.display_main()
        # self.selected_item()
        pass

    def get_user_data(self):
        # Load user data from the JSON file
        with open('users.json', 'r') as file:
            data = json.load(file)

        return data

    def print(self):
        user_data = self.get_user_data()

        for user in user_data:
            print(f"Username: {user['username']}, Password: {user['password']}")

    def display_users(self):
        self.root.ids.studs.data = {}
        users_data = self.get_user_data()

        if not users_data:
            self.root.ids.studs.data.append(
                {
                    "viewclass": "Deco",
                    "name": "No data Yet!",
                }
            )
        else:
            users = users_data["users"]
            for i, user in enumerate(users):
                self.root.ids.studs.data.append(
                    {
                        "viewclass": "Deco",
                        "name": user["username"],
                        "id": str(i)
                    }
                )

    def display_manage(self):
        self.root.ids.food.data = {}
        users_data = self.get_user_data()

        if not users_data:
            self.root.ids.all.data.append(
                {
                    "viewclass": "Nofood",
                    "name": "No data Yet!",
                }
            )
        else:
            users = users_data["users"]
            for i, user in enumerate(users):
                self.root.ids.all.data.append(
                    {
                        "viewclass": "Allow",
                        "name": user["username"],
                        "id": str(i)
                    }
                )

    def display_main(self):
        self.root.ids.food.data = {}
        data = FB.get_main(FB())

        if data:
            for i, y in data.items():
                self.root.ids.food.data.append(
                    {
                        "viewclass": "Food",
                        "name": y["name"],
                        "price": y["price"],
                    }
                )
        else:
            self.root.ids.food.data.append(
                {
                    "viewclass": "Nofood",
                    "name": "No data Yet!",
                }
            )

    def selected_item(self):
        self.root.ids.selected.data = {}
        users_data = self.orders

        if not users_data:
            self.root.ids.selected.data.append(
                {
                    "viewclass": "Noselected",
                    "name": "No data Yet!",
                }
            )
            self.total_cost()
        else:
            for i in users_data:
                self.root.ids.selected.data.append(
                    {
                        "viewclass": "Selected",
                        "name": i["product_name"],
                        "price": i["price"],
                        "quantity": i["quantity"],
                        "id": str(i)
                    }
                )
            self.total_cost()

    def search_live(self, text):
        self.root.ids.all.data = {}
        users_data = self.get_user_data()
        text = text.upper()
        users = users_data["users"]
        for i, user in enumerate(users):
            if text in user["username"]:
                self.nodata = ""
                self.root.ids.all.data.append(
                    {
                        "viewclass": "Allow",
                        "name": user["username"],
                    }
                )

            else:
                self.nodata = "components/no-data-found.png"

    def total_cost(self):
        # Calculate and return the total cost of products in the order
        self.total_price = str(
            sum(int(order_item['quantity']) * int(order_item['price'].strip().split("/")[0]) for order_item in
                self.orders))

        product_names = set(order_item['product_name'] for order_item in self.orders)

        self.item_selected = str(len(product_names))

    def quantity(self, id):
        if "minus-circle" in id.icon:
            if int(self.quantity_text) == 1:
                toast("Cant be below 1")

            else:
                self.quantity_text = str(int(self.quantity_text) - 1)

        else:
            self.quantity_text = str(int(self.quantity_text) + 1)

    def __init__(self, **kwargs):
        # Initialize an empty list to store orders
        super().__init__(**kwargs)
        self.orders = []
        self.waiter_list = FB.get_waiter(FB())
        self.admin_list = FB.get_admin(FB())

    def add_to_order(self, product_name, quantity, price):
        # Check if the product is already in the order
        for order_item in self.orders:
            if order_item['product_name'] == product_name:
                # Update the quantity if the product is found
                order_item['quantity'] = quantity
                print(self.orders)
                self.selected_item()
                return

        # If the product is not in the order, add a new entry
        order_item = {
            'product_name': product_name,
            'quantity': "1",
            'price': price
        }
        self.orders.append(order_item)
        self.selected_item()
        print(self.orders)

    def remove_from_order(self, product_name):
        # Remove the product from the order by filtering it out
        self.orders = [item for item in self.orders if item['product_name'] != product_name]
        print("test", self.orders)
        self.selected_item()

    def create_order(self):
        if network.ping_net():
            if self.orders:
                FB.register_order(FB(), self.username, self.orders, self.item_selected, self.total_price, self.user_type)
                self.caller()

            else:
                toast("Select item first!")

        else:
            toast("No internet")

    def caller(self):
        print("caller")
        self.orders.clear()
        self.selected_item()

    def check(self, text):
        if len(text) > 3:
            if text == self.admin():
                """
                sm = self.root
                sm.current = "add_product"
                """
                self.screen_capture("add_product")
                self.user_type = "Admin"
                self.clear_login()

            elif text == self.waiter():
                """
                sm = self.root
                sm.current = "orders
                """
                self.screen_capture("orders")
                self.user_type = "Waiter"
                self.clear_login()
            else:
                toast("Wrong pin")

    def get_data(self):
        with open('users.json', 'r') as file:
            data = json.load(file)
            user = next((user for user in data.get('users', []) if user['username'] == self.username), None)

            self.password = user["password"]

    def admin(self):
        for user_info in self.admin_list:
            for key, value in user_info.items():
                if value.get('Info', {}).get('user_name') == self.username:
                    return value['Info']['user_pin']
        return None

    def waiter(self):
        for user_info in self.waiter_list:
            for key, value in user_info.items():
                if value.get('Info', {}).get('user_name') == self.username:
                    return value['Info']['user_pin']
        return None

    """ 
    
        CATEGORY SELECTION  FUNCTION
     
    """

    def button_color(self, button_name):
        pend = self.root.ids.one
        pre = self.root.ids.two
        comp = self.root.ids.three

        pend.md_bg_color = "white"
        pre.md_bg_color = "white"
        comp.md_bg_color = "white"

        if "Main Dish" in button_name.text:
            pend.md_bg_color = "#ffd241"
            self.display_main()
        elif "Fish" in button_name.text:
            comp.md_bg_color = "#ffd241"
        elif "Extra" in button_name.text:
            pre.md_bg_color = "#ffd241"

    def product_color(self, button_name):
        pend = self.root.ids.main
        pre = self.root.ids.extra
        comp = self.root.ids.fish

        pend.md_bg_color = "white"
        pre.md_bg_color = "white"
        comp.md_bg_color = "white"

        pend.text_color = "black"
        pre.text_color = "black"
        comp.text_color = "black"

        if "Main Dish" in button_name.text:
            pend.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            pend.text_color = "white"
            self.category = "Main Dish"
        elif "Fish" in button_name.text:
            comp.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            comp.text_color = "white"
            self.category = "Fish"
        elif "Extra" in button_name.text:
            pre.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            pre.text_color = "white"
            self.category = "Extra"

    def user_color(self, button_name):
        pend = self.root.ids.wai
        pre = self.root.ids.adm

        pend.md_bg_color = "white"
        pre.md_bg_color = "white"

        pend.text_color = "black"
        pre.text_color = "black"

        if "Waiter" in button_name.text:
            pend.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            pend.text_color = "white"
            self.user_category = "Waiter"

        elif "Admin" in button_name.text:
            pre.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            pre.text_color = "white"
            self.user_category = "Admin"

    """ 
    
        ENDS CATEGORY FUNCTON
        
    """

    """ 
    
        KEYBOARD INTEGRATION
        
    """

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

    def get_users(self):
        # Assuming FB is a class with a get_user method
        data = FB.get_user(FB())
        users_data = []

        for user_dict in data:
            for user_key, user_info in user_dict.items():
                users_data.append(user_info['Info'])

        if not users_data:
            self.root.ids.studs.data.append(
                {
                    "viewclass": "Deco",
                    "name": "No data Yet!",
                }
            )
        else:
            for i, user in enumerate(users_data):
                self.root.ids.studs.data.append(
                    {
                        "viewclass": "Deco",
                        "name": user["user_name"],
                    }
                )

    """
                END LOGIN FUNCTIONS
    """

    """
            ORDER FUNCTIONS
    
    """

    """def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"""""

    def add_product(self, name, price):
        if network.ping_net():
            if self.category == "":
                toast("Please select category")
            elif name == "":
                toast("Please enter name")

            elif price == "":
                toast("Please enter price")

            else:
                if FB.register_product(FB(), self.category, name, price):
                    toast("Product Added successfully")
                    self.clear_form()
                else:
                    toast("Product already exist")
        else:
            toast("No internet")

    def add_user(self, name, pin):
        if network.ping_net():
            if self.user_category == "":
                toast("Please select category")
            elif name == "":
                toast("Please enter username")
            elif pin == "":
                toast("Please enter pin")
            else:
                FB.register_user(FB(), self.user_category, name, pin)
                self.clear_input()

        else:
            toast("No internet")

    def clear_input(self):
        # Iterate through input fields and reset their values
        for input_field_id in ['user', 'pin']:
            input_field = self.root.ids[input_field_id]
            input_field.text = ""

    def clear_form(self):
        # Iterate through input fields and reset their values
        for input_field_id in ['price', 'name']:
            input_field = self.root.ids[input_field_id]
            input_field.text = ""

    def clear_login(self):
        # Iterate through input fields and reset their values
        for input_field_id in ['input']:
            input_field = self.root.ids[input_field_id]
            input_field.text = ""

    """
            END ORDER FUNCTIONS
    
    """

    """ 
    
        SCREEN FUNCTIONS
     
    """

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

    """ 

           END SCREEN FUNCTIONS

    """


Main().run()
