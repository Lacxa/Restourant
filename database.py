from datetime import datetime

from kivymd.toast import toast


class FireBase:
    def register_user(self, phone, username, password):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                store = db.reference("Restaurant").child("Waiters").child(phone).child('Waiter_Info')
                store.set({
                    "user_name": username,
                    "user_phone": phone,
                    "user_password": password,
                })
            except:
                return "No Internet!"

    def get_user(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                store = db.reference("Restaurant").child("Waiters")
                stores = store.get()
                return stores
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

    def get_main(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = db.reference("Restaurant").child("Products").child("category").child("Main Dish")
            data = ref.get()

            return data

    def register_order(self, user, order, total_item, total_price):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            ref = db.reference("Restaurant").child("Users").child("category").child(user).child(self.year()).child(
                self.month_date()).child(self.generate_id())
            ref.set(
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

                toast("Order Successful")

    def generate_id(self):
        # Generate a unique order ID based on timestamp and counter
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
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

# FireBase.register_order(FireBase(), "lul", [{'product_name': 'john_doe', 'quantity': '1', 'price': '500'}, {'product_name': 'jane_smith', 'quantity': '1', 'price': '500'}, {'product_name': 'bob_jones', 'quantity': '1', 'price': '500'}])
#FireBase.get_main(FireBase())