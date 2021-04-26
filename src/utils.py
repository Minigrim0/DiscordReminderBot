from datetime import datetime
from django.utils import timezone
from db.models import Reminder

from src.decorators import log_this


def createReminder(name, start_time, duration, people_to_remind, channel_id, server_id):
    Reminder.objects.create(
        name=name,
        start_time=start_time,
        duration=duration,
        role_to_remind=people_to_remind,
        channel=channel_id,
        guild=server_id,
    )


def modifyReminder(name, server_id, field, value, cog):
    reminder = Reminder.objects.filter(name=name, guild=server_id)
    if reminder.count() == 0:
        return {"error": True, "msg": f"Bert a pas trouvé événement '{name}'"}

    reminder = reminder.first()

    if field == "start_date":
        try:
            value = datetime.strptime(value, "%d/%m/%Y %H:%M")
        except Exception:
            return {
                "error": True,
                "msg": f"Format pas correct : {value}",
            }
        old_value = datetime.strftime(
            timezone.make_naive(reminder.start_time),
            "%d/%m/%Y %H:%M"
        )
        reminder.start_time = value

    elif field == "name":
        value = value.lower()
        old_value = reminder.name
        reminder.name = value

    elif field == "duration":
        hours, minutes = value.split(":")
        if not hours.isdigit():
            return {"error": True, "msg": "Heures doivent être chiffre"}
        if not minutes.isdigit():
            return {"error": True, "msg": "Minutes doivent être chiffre"}
        if int(hours) > 23:
            return {"error": True, "msg": "Heures peut pas être plus que 23"}
        if int(minutes) > 59:
            return {"error": True, "msg": "Minutes peut pas être plus que 59"}
        value = timezone.time(hour=int(hours), minute=int(minutes))
        old_value = reminder.duration
        reminder.duration = value

    elif field == "channel":
        guild = cog.bot.get_guild(server_id)
        channel = guild.get_channel(int(value[2:-1]))
        if channel is None:
            return {"error": True, "msg": f"Bert pas trouvé channel '{value}'"}
        old_value = f"<#{reminder.channel}>"
        reminder.channel = value[2:-1]

    elif field == "allow_dp":
        value = value.lower()
        if value not in ["true", "false"]:
            return {"error": True, "msg": f"Toi choisir 'true' ou 'false', pas {value}"}
        old_value = "true" if reminder.dp_participants else "false"
        reminder.dp_participants = value == "true"

    else:
        return {"error": True, "msg": f"Bert pas connaitre champs {field}"}

    reminder.save()

    return {
        "error": False,
        "msg": f"Bert a modifié champs **{field}** ({old_value} => {value}) événement '**{reminder.name}**'",
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
                timezone.now(),
                timezone.now() + timezone.timedelta(hours=value),
            ]
        ).order_by("start_time")
    elif name == "days":
        reminders = Reminder.objects.filter(
            start_time__range=[
                timezone.now(),
                timezone.now() + timezone.timedelta(days=value),
            ]
        ).order_by("start_time")
    elif name == "week":
        reminders = Reminder.objects.filter(
            start_time__range=[
                timezone.now(),
                timezone.now() + timezone.timedelta(weeks=value),
            ]
        ).order_by("start_time")
    else:
        return Reminder.objects.none()

    reminders = reminders.filter(guild=guild)

    return [reminder.serialized for reminder in reminders]


def loadNearFutureEvents():
    """ Loads every event that starts in less than 5 minutes """
    return Reminder.objects.filter(
        start_time__gte=timezone.now() - timezone.timedelta(minutes=5),
        start_time__lt=timezone.now() + timezone.timedelta(minutes=5),
        advertised=False,
    )


@log_this
async def advertise_event(event, guild):
    channel = guild.get_channel(event.channel)
    await channel.send(
        f"Salut {event.role_to_remind} ! C'est le moment pour {event.name} durant {event.duration} !"
    )
    if event.dp_participants:
        await channel.send(f"/deathping {event.role_to_remind}")
