import datetime

from db.models import Reminder


def createReminder(name, start_time, duration, people_to_remind, channel_id, server_id):
    Reminder.objects.create(
        name=name,
        start_time=start_time,
        duration=duration,
        role_to_remind=people_to_remind,
        channel=channel_id,
        guild=server_id,
    )


def modReminder(name, server_id, field, value):
    reminder = Reminder.objects.filter(name=name, guild=server_id)
    if reminder.count() == 0:
        return {"error": True, "msg": f"Bert a pas trouvé événement '{name}'"}

    reminder = reminder.first()
    old_value = getattr(reminder, field)
    setattr(reminder, field, value)

    return {
        "error": False,
        "msg": f"Bert a modifié champs {field} ({old_value} => {value}) événement '{name}'",
    }


def deleteReminder(name, server_id):
    reminder = Reminder.objects.filter(name=name, guild=server_id)
    if reminder.count() == 0:
        return {"error": True, "msg": f"Bert a pas trouvé événement '{name}'"}

    reminder = reminder.first()
    reminder.delete()
    return {"error": False, "msg": f"Bert a supprimé événement '{name}'"}


def getFutureEvents(name, value, guild):
    if name == "hours":
        reminders = Reminder.objects.filter(
            start_time__range=[
                datetime.datetime.now(),
                datetime.datetime.now() + datetime.timedelta(hours=value),
            ]
        ).order_by("start_time")
    elif name == "days":
        reminders = Reminder.objects.filter(
            start_time__range=[
                datetime.datetime.now(),
                datetime.datetime.now() + datetime.timedelta(days=value),
            ]
        ).order_by("start_time")
    elif name == "week":
        reminders = Reminder.objects.filter(
            start_time__range=[
                datetime.datetime.now(),
                datetime.datetime.now() + datetime.timedelta(weeks=value),
            ]
        ).order_by("start_time")
    else:
        return Reminder.objects.none()

    reminders = reminders.filter(guild=guild)

    return [reminder.serialized for reminder in reminders]
