from django.db import models

class MessageQuerySet(models.QuerySet):
    def messages_in_thread(self, thread, *args, **kwargs):
        return self.filter(thread=thread, *args, **kwargs).order_by('created').prefetch_related('sender')
