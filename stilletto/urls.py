"""
URL configuration for stilletto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from signal_api.views import TelegramAPIView, MT5APIView, DiscordAPIView, EAAPIView, LemonAPIView, NoteAPIView
from app.views import *
import os

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('dashboard/', dashboard, name="dashboard"),
    path('platforms/', platforms, name="platforms"),
    path('pricing/', pricing, name="pricing"),
    path('', index, name="index"),
    path('submitwebhookdiscord/', submit_discord_webhook, name="submitwebhookdiscord"),
    path('submitwebhooktg/', submit_telegram_webhook, name="submitwebhooktg"),
    path('submitwebhookmt5/', submit_mt5_webhook, name="submitwebhookmt5"),
    path('submittg/', submit_telegram_link, name="submittg"),
    path('submitmt5/', submit_telegram_link, name="submitmt5"),
    path('add_chat/', add_chat, name="add_chat"),
    path('toggle_webhook_status/<uuid:webhook_id>/<str:identifier>/', toggle_webhook_status, name="toggle_webhook_status"),
    path('delete_webhook/<uuid:webhook_id>/<str:identifier>/', delete_webhook, name="delete_webhook"),
    path('submitdiscord/', submit_telegram_link, name="submitdiscord"),
    path('tview_api/telegram/<uuid:pk>', TelegramAPIView.as_view(), name="telegram_signal_api_endpoint"),
    path('tview_api/mt5/<uuid:pk>', MT5APIView.as_view(), name="mt5_signal_api_endpoint"),
    path('tview_api/discord/<uuid:pk>', DiscordAPIView.as_view(), name="discord_signal_api_endpoint"),
    path('metatrader_api/<str:pk>', EAAPIView.as_view(), name="ea_signal_api_endpoint"),
    path('journal_note_api/', NoteAPIView.as_view(), name="note_api_endpoint"),
    path('webhooks/lemons', LemonAPIView.as_view(), name="lemon_api_endpoint"),
    path('submitalert/', submit_alert, name="submitalert"),
    path('help/telegram/', telegram_help_page, name="telegram_help_page"),
    path('help/discord/', discord_help_page, name="discord_help_page"),
    path('help/mt5/', mt5_help_page, name="mt5_help_page"),
    path('help/privacy-TOS/', pp_tos_page, name="pp_tos_page"),
    path("get_ea/", download_file, name="get_ea")

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'app/static'))
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'accounts/static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
       urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
