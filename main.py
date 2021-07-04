import os
import django
from web.app import app

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()


def main():
    """The main function of the program, loads needed libs and runs the bot

    Raises:
        Exception: In case the API KEY is missing
    """
    from singleton.client import Bert
    from singleton.cog import ReminderCog

    API_KEY = os.environ.get("API_KEY", "")
    if API_KEY == "":
        raise Exception("You must specify an API key")

    client = Bert.getInstance()
    ReminderCog.getInstance()  # Start the cog

    client.loop.create_task(app.run_task('0.0.0.0'))
    client.run(API_KEY)


if __name__ == "__main__":
    main()
