from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from chat.managers import MessageManager


class Thread(TimeStampedModel):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    last_message = models.ForeignKey('chat.Message', on_delete=models.SET_DEFAULT, null=True, default=None,
                                     related_name='last_message')

    def __str__(self):
        return str(self.pk)

    @staticmethod
    def get_thread_between(user1_id, user2_id):
        thread = Thread.objects.filter(participants__in=[user1_id])
        thread = thread.filter(participants__in=[user2_id])

        return thread.first()


class Message(TimeStampedModel):
    objects = MessageManager()
    thread = models.ForeignKey('chat.Thread', on_delete=models.CASCADE)
    body = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        """
        If first time message is saved (creation), update last_message and modified in thread
        """
        update_thread = False
        if not self.pk:
            update_thread = True

        super(Message, self).save(*args, **kwargs)

        if update_thread:
            self.thread.last_message = self
            self.thread.save()