from django.db import models

class MessageQuerySet(models.QuerySet):
    def messages_in_thread(self, thread, *args, **kwargs):
        return self.filter(thread=thread, *args, **kwargs).prefetch_related('sender')
