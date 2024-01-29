import json
import re

from datetime import datetime
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy import utils
from kivy.clock import Clock, mainthread
from threading import Thread
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

from kivy.metrics import dp
from kivymd_extensions.akivymd.uix.charts import AKPieChart

import network
from database import FireBase as FB

from pdf import Pdf

if utils.platform != 'android':
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


class Deco(MDCard):
    name = StringProperty("")


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
    drink = StringProperty("")

    category = StringProperty("")
    today_time = StringProperty("")

    # user
    nodata = StringProperty("")
    user_category = StringProperty("")
    user_type = StringProperty("")

    user_nodata = StringProperty("components/open.png")

    # overall admin
    total_users = StringProperty("")
    total_orders = StringProperty("")
    total_main = StringProperty("")
    yes_day = StringProperty("")

    # graph
    graph = StringProperty("")
    bar = StringProperty("")

    # date
    today_date = StringProperty("")
    year = StringProperty("")
    selected_date = StringProperty("Open date picker")

    # orders
    orders_no = StringProperty("")
    order_price = StringProperty("")

    # List
    waiter_list = None
    admin_list = None
    orders_list = None
    orders = []

    def on_start(self):
        Clock.schedule_once(self.keyboard_hooker, .1)
        thread = Thread(target=self.get_users())
        thread.start()

        self.first()
        self.bar = "components/stacked_bar_chart.png"
        self.display_food("Main Dish")
        # self.selected_item()
        pass

    @mainthread
    def first(self):
        self.waiter_list = FB.get_waiter(FB())
        self.admin_list = FB.get_admin(FB())
        self.orders_list = FB.get_all_orders(FB())
        self.count_data()
        self.get_current_date()

        # self.waiter_list = []  # FB.get_waiter(FB())
        # self.admin_list = []  # FB.get_admin(FB())
        # self.orders_list = [[], []]  # FB.get_all_orders(FB())
        # self.count_data()

    def print(self):
        toast("Under construction")

    """

            LOGIN FUNCTIONS

    """

    def get_users(self):
        if network:
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

        else:
            toast("no internet")

    def update_text(self, button_text):
        text_input = self.root.ids.input
        current_text = text_input.text
        text_input.text = current_text + button_text

    def delete_last_digit(self):
        text_input = self.root.ids.input
        current_text = text_input.text
        text_input.text = current_text[:-1]

    def check(self, text):
        if len(text) > 3:
            if text == self.admin():
                """
                sm = self.root
                sm.current = "admin"
                """
                self.screen_capture("admin")
                self.user_type = "Admin"
                self.clear_login()

            elif text == self.waiter():
                """
                sm = self.root
                sm.current = "orders
                """
                self.screen_capture("sales")
                self.user_type = "Waiter"
                self.clear_login()
            else:
                toast("Wrong pin")

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

    def clear_login(self):
        # Iterate through input fields and reset their values
        for input_field_id in ['input']:
            input_field = self.root.ids[input_field_id]
            input_field.text = ""

    """
                END LOGIN FUNCTIONS
    """

    """ 

            DATE AND TIME FUNCTIONS

    """

    def on_save(self, instance, value, date_range):
        self.selected_date = str(value)
        two = self.selected_date.strip().split('-')
        year = f"{two[0]}"
        datep = f"{two[1]}_{two[2]}"
        self.display_presales(year, datep)

    def on_savu(self, instance, value, date_range):
        pass

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def report_date_picker(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_savu, on_cancel=self.on_cancel)
        date_dialog.open()

    def get_current_date(self, ):
        current_datetime = datetime.now()
        current_date = str(current_datetime.date())
        current_year = current_datetime.year

        date_object = datetime.strptime(current_date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%m-%d")

        self.today_date = str(formatted_date)
        self.year = str(current_year)

    def time_updater(self):
        current_time = datetime.now()
        self.graph = "components/pie_chart.png"
        self.bar = "components/stacked_bar_chart.png"
        self.admin_pie_chart()
        formatted_time = current_time.strftime("%a %d %b %Y")
        self.today_time = formatted_time

    """ 

            END OF DATE AND TIME FUNCTIONS

    """

    """ 

                REPORT FUNCTIONS

    """

    def create_sales_report(self):
        Pdf.create_sales_report()

    """ 

               END REPORT FUNCTIONS

    """

    """ 

             DISPLAY FUNCTIONS

    """

    @mainthread
    def display_sales(self):
        if network:
            self.root.ids.sales.data = {}
            users_data = FB.get_user_sales(FB(), self.username, self.user_type)
            today = users_data[0]
            yes_day = users_data[1]
            self.user_pie_chart(today, yes_day)

            if today:
                for user_id, user_info in today.items():
                    self.root.ids.sales.data.append(
                        {
                            "viewclass": "Daily",
                            "item": user_info["total_item"],
                            "price": user_info["total_price"],
                            "idd": user_id
                        }
                    )

            else:
                self.root.ids.sales.data.append(
                    {
                        "viewclass": "Nodaily",
                        "idd": "No oder Yet!",
                    }
                )
        else:
            toast("No internet!")

    @mainthread
    def presales(self, ):
        if network:
            self.root.ids.profile.data = {}
            users_data = FB.get_user_sales(FB(), self.username, self.user_type)
            today = users_data[0]
            if today:
                for user_id, user_info in today.items():
                    self.root.ids.profile.data.append(
                        {
                            "viewclass": "Daily",
                            "item": user_info["total_item"],
                            "price": user_info["total_price"],
                            "idd": user_id
                        }
                    )

            else:
                self.root.ids.profile.data.append(
                    {
                        "viewclass": "Nodaily",
                        "idd": "No oder Yet!",
                    }
                )
        else:
            toast("No internet!")

    @mainthread
    def display_presales(self, year, my_date):
        if network:
            self.root.ids.profile.data = {}
            users_data = FB.user_sales(FB(), self.username, self.user_type, year, my_date)

            if users_data:
                for user_id, user_info in users_data.items():
                    self.root.ids.profile.data.append(
                        {
                            "viewclass": "Daily",
                            "item": user_info["total_item"],
                            "price": user_info["total_price"],
                            "idd": user_id
                        }
                    )

            else:
                self.root.ids.profile.data.append(
                    {
                        "viewclass": "Nodaily",
                        "idd": "No oder Yet!",
                    }
                )
        else:
            toast("No internet!")

    @mainthread
    def display_food(self, name):
        if network:
            self.root.ids.food.data = {}
            data = FB.get_food(FB(), name)

            if data:
                no = len(data)
                self.total_main = str(no)

                for i, y in data.items():
                    self.root.ids.food.data.append(
                        {
                            "viewclass": "Food",
                            "name": y["name"],
                            "price": y["price"],
                        }
                    )
            else:
                self.total_main = "0"
                self.root.ids.food.data.append(
                    {
                        "viewclass": "Nofood",
                        "name": "No data Yet!",
                    }
                )

        else:
            toast("no internet!")

    def search_live(self, text):
        self.root.ids.all.data = {}
        users_data = self.get_user_data()
        users = users_data["users"]

        for x, y in enumerate(users):
            if text.lower() in y["username"]:
                self.nodata = ""
                self.root.ids.all.data.append(
                    {
                        "viewclass": "Allow",
                        "name": y["username"],
                    }
                )
            else:
                self.nodata = "components/no-data-found.png"

    def search_user(self, text):
        self.root.ids.user.data = {}
        users_data = self.get_user_data()
        users = users_data["users"]

        for x, y in enumerate(users):
            if text.lower() in y["username"]:
                self.user_nodata = "components/open.png"
                self.root.ids.user.data.append(
                    {
                        "viewclass": "User_allow",
                        "name": y["username"],
                    }
                )
            else:
                self.user_nodata = "components/no-data-found.png"

    """ 

          END OF DISPLAY FUNCTIONS

    """

    """ 

               ORDERS FUNCTION

    """

    def count_data(self, ):
        # Count occurrences of 'Info' key
        if self.waiter_list:
            waiter_count = sum(
                'Info' in user_info for user_dict in self.waiter_list for user_info in user_dict.values())
        else:
            waiter_count = 0

        if self.admin_list:
            admin_count = sum('Info' in user_info for user_dict in self.admin_list for user_info in user_dict.values())

        else:
            admin_count = 0

        total = waiter_count + admin_count
        self.total_users = str(total)

        order_ids = set()
        if self.orders_list[0]:
            today = self.orders_list[0]
            for order_id, order_info in today.items():
                order_ids.add(order_id)
                data = len(order_ids)
                self.total_orders = str(data)

        else:
            self.total_orders = "0"

        if self.orders_list[1]:
            yesterday = self.orders_list[1]
            for idd, info in yesterday.items():
                order_ids.add(idd)
                data = len(order_ids)
                self.yes_day = str(data)

        else:
            self.yes_day = "0"

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

    def total_cost(self):
        # Calculate and return the total cost of products in the order
        self.total_price = str(
            sum(int(order_item['quantity']) * int(order_item['price'].strip().split("/")[0]) for order_item in
                self.orders))

        product_names = set(order_item['product_name'] for order_item in self.orders)

        self.item_selected = str(len(product_names))

    def order_count(self):
        # total cost of products in the order
        self.total_price = str(
            sum(int(order_item['quantity']) * int(order_item['price'].strip().split("/")[0]) for order_item in
                self.orders))

        product_names = set(order_item['product_name'] for order_item in self.orders)

        self.orders_no = str(len(product_names))

    def quantity(self, id):
        if "minus-circle" in id.icon:
            if int(self.quantity_text) == 1:
                toast("Cant be below 1")

            else:
                self.quantity_text = str(int(self.quantity_text) - 1)

        else:
            self.quantity_text = str(int(self.quantity_text) + 1)

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
                FB.register_order(FB(), self.username, self.orders, self.item_selected, self.total_price,
                                  self.user_type)
                self.caller()

            else:
                toast("Select item first!")

        else:
            toast("No internet")

    @mainthread
    def caller(self):
        print("caller")
        self.orders.clear()
        self.selected_item()
        self.admin_list = FB.get_admin(FB())
        self.orders_list = FB.get_all_orders(FB())
        self.count_data()

    """ 

             END OF ORDERS FUNCTION

    """

    """ LOCAL TEST """

    def get_user_data(self):
        # Load user data from the JSON file
        with open('users.json', 'r') as file:
            data = json.load(file)

        return data

    """ END LOCAL TEST """

    """ 
                    GRAPH AND CHART
    
    """

    piechart = None
    items = None

    def admin_pie_chart(self):
        if int(self.total_orders) > 1:
            total_orders = int(self.total_orders)

        else:
            total_orders = 1

        if int(self.yes_day) > 1:
            yes_day = int(self.yes_day)

        else:
            yes_day = 1

        total = total_orders + yes_day

        # Calculate the percentages with rounding
        percentage1 = round((total_orders / total) * 100)
        percentage2 = 100 - percentage1  # The sum will always be 100

        self.items = [{"Yesterday": percentage2, "Today": percentage1}]

        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(250), dp(250)),
        )
        self.root.ids.admin_box.add_widget(self.piechart)

    user_chart = None
    itemu = None

    def user_pie_chart(self, today, yes_day):

        if today:
            one = len(today)

        else:
            one = 1
        if yes_day:
            two = len(yes_day)

        else:
            two = 1

        total = one + two

        percentage1 = round((one / total) * 100)
        percentage2 = 100 - percentage1  # The sum will always be 100

        self.itemu = [{"Yesterday": percentage2, "Today": percentage1}]

        self.user_chart = AKPieChart(
            items=self.itemu,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(250), dp(250)),
        )
        self.root.ids.user_box.add_widget(self.user_chart)

    """ 
                        GRAPH AND CHART

    """

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
            self.display_food("Main Dish")
        elif "Fish" in button_name.text:
            comp.md_bg_color = "#ffd241"
            self.display_food("Fish")
        elif "Extra" in button_name.text:
            pre.md_bg_color = "#ffd241"
            self.display_food("Extra")

    def product_color(self, button_name):
        pend = self.root.ids.main
        pre = self.root.ids.extra
        comp = self.root.ids.fish

        pend.md_bg_color = "#424242"
        pre.md_bg_color = "#424242"
        comp.md_bg_color = "#424242"

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

    def dcolor(self, name):
        pend = self.root.ids.agua
        pre = self.root.ids.pan

        pend.md_bg_color = "white"
        pre.md_bg_color = "white"

        if "Soft Drink" in name.text:
            pend.md_bg_color = "#ffd241"
            pre.md_bg_color = "white"
            self.display_food("Soft Drink")

        elif "Beverages" in name.text:
            pend.md_bg_color = "white"
            pre.md_bg_color = "#ffd241"
            self.display_food("Beverages")

    def drink_color(self, button_name):
        pend = self.root.ids.soft
        pre = self.root.ids.brave

        pend.md_bg_color = "#424242"
        pre.md_bg_color = "#424242"

        pend.text_color = "black"
        pre.text_color = "black"

        if "Soft Drink" in button_name.text:
            pend.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            pend.text_color = "white"
            self.drink = "Soft Drink"

        elif "Beverages" in button_name.text:
            pre.md_bg_color = 80 / 225, 136 / 225, 114 / 225, 1
            pre.text_color = "white"
            self.drink = "Beverages"

    def user_color(self, button_name):
        pend = self.root.ids.wai
        pre = self.root.ids.adm

        pend.md_bg_color = "#424242"
        pre.md_bg_color = "#424242"

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
                ADD FUNCTIONS

    """

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

    def add_drinks(self, name, price):
        if network.ping_net():
            if self.drink == "":
                toast("Please select category")
            elif name == "":
                toast("Please enter name")

            elif price == "":
                toast("Please enter price")

            else:
                if FB.register_product(FB(), self.drink, name, price):
                    toast("Product Added successfully")
                    self.clear_drink()
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

    def clear_drink(self):
        # Iterate through input fields and reset their values
        for input_field_id in ['drink', 'peace']:
            input_field = self.root.ids[input_field_id]
            input_field.text = ""

    """
            END ADD FUNCTIONS
    
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
            END KEYBOARD FUNCTIONS

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
