import pytz

from django.db import models
from django.utils import timezone


class Reminder(models.Model):
    name = models.CharField(max_length=150, default="none", unique=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    guild = models.PositiveBigIntegerField(default=0)
    channel = models.PositiveBigIntegerField(default=0)
    role_to_remind = models.TextField(null=True)
    advertised = models.BooleanField(default=False)
    dp_participants = models.BooleanField(default=False)

    @property
    def isNow(self):
        return (timezone.now() >= self.start_time) and not self.advertised

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def serialized(self):
        return {
            "ID": self.id,
            "name": self.name,
            "start_time": self.start_time.astimezone(pytz.timezone('Europe/Brussels')).strftime("%d %b %Y à %H:%M"),
            "roles": self.role_to_remind,
            "duration": self.duration,
        }

    def set_duration(self, duration):
        self.end_time = self.start_time + duration

    def __repr__(self):
        return f"Reminder {self.name} (advertised: {self.advertised})"
