from django.forms import ModelForm, TextInput

from accounts.models import CustomUser
from chat.models import Message, Thread


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
        labels = {
            "body": ('Message'),
        }
        widgets = {
            'body': TextInput(attrs={'autofocus': 'autofocus'}),
        }

    def save(self, commit=True):
        """
        If first message between users and no thread exists, first create a thread
        """
        if not self.thread:
            other_user = CustomUser.objects.get(pk=self.other_user_pk)
            new_thread = Thread.objects.create()
            new_thread.participants.add(self.sender)
            new_thread.participants.add(other_user)

            self.thread = new_thread

        message = super(ModelForm, self).save(commit=False)
        message.sender = self.sender
        message.thread = self.thread
        if commit:
            message.save()
        return message