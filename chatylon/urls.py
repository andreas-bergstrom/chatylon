from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

import chat
from chatylon import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('threads/', include('chat.urls', namespace='chat')),
    path('', RedirectView.as_view(url=reverse_lazy('chat:threads'), permanent=True))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

handler404 = chat.views.NotFoundView.as_view()