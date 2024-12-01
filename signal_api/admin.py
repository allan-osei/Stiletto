from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Telegram_Webhook)
admin.site.register(Discord_Webhook)
admin.site.register(MT5_Webhook)
admin.site.register(TelegramChat)
admin.site.register(DiscordChat)
admin.site.register(Order)
admin.site.register(Alert)
admin.site.register(TakeProfit)

