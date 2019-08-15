from django.contrib import admin

from chat.models import Thread, Message


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    list_display = ('pk', 'last_message', 'created', 'modified')

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('pk', 'body', 'sender', 'thread', 'created', 'modified')

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)