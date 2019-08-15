import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from accounts.models import CustomUser
from chat.forms import MessageForm
from chat.models import Thread, Message
from chat.responses import TemplateResponseNotFound


class UsersListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'chat/user_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'users': CustomUser.objects.get_user_list_for(me=self.request.user)
        }

        return context


class MessagesListView(LoginRequiredMixin, generic.FormView):
    template_name = 'chat/message_list.html'
    form_class = MessageForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['messages'] = Message.objects.messages_in_thread(thread=self.get_thread())
        context['other_user'] = get_object_or_404(CustomUser, pk=self.kwargs['pk'])

        return context

    def form_valid(self, form):
        form.sender = self.request.user
        form.other_user_pk = self.kwargs['pk']
        form.thread = self.get_thread()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat:messages', args=[self.kwargs['pk']])

    def get_thread(self):
        other_user = self.kwargs['pk']
        me_user = self.request.user.pk

        thread = Thread.objects.filter(participants__in=[me_user])
        thread = thread.filter(participants__in=[other_user])

        return thread.first()

class NotFoundView(generic.TemplateView):
    response_class = TemplateResponseNotFound
    template_name = 'chat/404.html'
