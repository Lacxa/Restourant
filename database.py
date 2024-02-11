from datetime import datetime, timedelta
from kivymd.toast import toast


class FireBase:
    def register_user(self, category, username, pin):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            store = db.reference("Restaurant").child("Users").child(category)
            data = store.get()
            if data and username in data:
                toast("User already exist")
                return False

            else:
                store = db.reference("Restaurant").child("Users").child(category).child(username).child(
                    'Info')
                store.set({
                    "user_name": username,
                    "user_pin": pin,
                })
                toast("User Added successfully")

    def get_user(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                user_list = []

                store = db.reference("Restaurant").child("Users").child("Waiter")
                waiter_list = store.get()
                user_list.append(waiter_list)

                ref = db.reference("Restaurant").child("Users").child("Admin")
                admin_list = ref.get()
                user_list.append(admin_list)

                return user_list
            except:
                return "No Internet!"

    def get_user_detail(self, name):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                list = db.reference("Restaurant").child("Users").child("Waiter")
                waiter = list.get()

                if name in waiter:
                    low = db.reference("Restaurant").child("Users").child("Waiter").child(name)
                    row = low.get()
                    print("waiter", row)

                ref = db.reference("Restaurant").child("Users").child("Admin")
                admin = ref.get()

                if name in admin:
                    up = db.reference("Restaurant").child("Users").child("Admin")
                    upp = up.get()
                    print("admin", upp)

            except:
                return "No Internet!"


    def get_waiter(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                user_list = []

                ref = db.reference("Restaurant").child("Users").child("Waiter")
                admin_list = ref.get()
                user_list.append(admin_list)

                return user_list
            except:
                return "No Internet!"

    def get_admin(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                user_list = []

                store = db.reference("Restaurant").child("Users").child("Admin")
                waiter_list = store.get()
                user_list.append(waiter_list)

                return user_list
            except:
                return "No Internet!"

    def register_product(self, category, name, price):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = db.reference("Restaurant").child("Products").child("category").child(category)
            data = ref.get()
            if data and name in data:
                return False

            else:
                ref = db.reference("Restaurant").child("Products").child("category").child(category).child(name)
                print("uploaded")
                ref.set(
                    {
                        "name": name,
                        "price": price,

                    }
                )
        return True

    def get_food(self, name):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = db.reference("Restaurant").child("Products").child("category").child(name)
            data = ref.get()

            return data

    def register_order(self, user, order, total_item, total_price, category):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = (db.reference("Restaurant").child("Users").child(category).child(user).child("Orders")
                   .child(self.year()).child(self.month_date()).child(self.generate_id()))
            ref.set(
                {
                    "total_item": total_item,
                    "total_price": total_price,
                }
            )

            store = (db.reference("Restaurant").child("Orders").child(self.year()).child(self.month_date())
                     .child(self.generate_id()))
            store.set(
                {
                    "total_item": total_item,
                    "total_price": total_price,
                }
            )

            for i in order:
                order_ref = ref.push()
                order_ref.set(
                    {
                        "name": i["product_name"],
                        "price": i["price"],
                        "quantity": i["quantity"],
                    }
                )

                all_order = store.push()
                all_order.set(
                    {
                        "name": i["product_name"],
                        "price": i["price"],
                        "quantity": i["quantity"],
                    }
                )

                toast("Order Successful")

    def get_all_orders(self, ):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            today = (db.reference("Restaurant").child("Orders").child(self.year()).child(self.month_date()))
            data1 = today.get()

            current_date_obj = datetime.strptime(self.month_date(), "%m_%d")

            # Calculate the previous date
            previous_date_obj = current_date_obj - timedelta(days=1)

            # Format the previous date as a string in the same format
            previous_date_str = previous_date_obj.strftime("%m_%d")

            yesterday = (db.reference("Restaurant").child("Orders").child(self.year()).child(previous_date_str))
            data2 = yesterday.get()

            comp = data1, data2

            return comp

    def get_user_sales(self, user, category):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = (db.reference("Restaurant").child("Users").child(category).child(user).child("Orders")
                   .child(self.year()).child(self.month_date()))

            data1 = ref.get()

            current_date_obj = datetime.strptime(self.month_date(), "%m_%d")

            # Calculate the previous date
            previous_date_obj = current_date_obj - timedelta(days=1)

            # Format the previous date as a string in the same format
            previous_date_str = previous_date_obj.strftime("%m_%d")

            store = (db.reference("Restaurant").child("Users").child(category).child(user).child("Orders")
                     .child(self.year()).child(previous_date_str))

            data2 = store.get()

            comp = data1, data2

            return comp

    def user_sales(self, user, category, year, my_time):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = (db.reference("Restaurant").child("Users").child(category).child(user).child("Orders")
                   .child(year).child(my_time))

            data = ref.get()

            return data

    def generate_id(self):
        timestamp = datetime.now().strftime('%m%d%H%M%S%f')
        order_id = timestamp
        return order_id

    def year(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return y

    def month_date(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return f"{m}_{d}"

FireBase.get_user_detail(FireBase() , "koko")
# FireBase.get_all_orders(FireBase())
# FireBase.get_user_sales(FireBase(), "joo", "Waiter")

