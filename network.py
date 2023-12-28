import requests


def ping_net():
    try:
        code = requests.get("https://console.firebase.google.com/project/farmzon-abdcb/database/farmzon-abdcb/data/~2FRestaurant")

        print(code.status_code)

        if code.status_code == 200:
            return True

    except:
        return False