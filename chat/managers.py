from django.db import models

class MessageQuerySet(models.QuerySet):
    def messages_in_thread(self, thread):
        return self.model.objects.filter(thread=thread).order_by('created').prefetch_related('sender')
