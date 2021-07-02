import os
import django

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()


def main():
    from singleton.client import Bert

    API_KEY = os.environ.get("API_KEY", "")
    if API_KEY == "":
        raise Exception("You must specify an API key")

    client = Bert.getInstance()

    client.run(API_KEY)


if __name__ == "__main__":
    main()
