from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

User = settings.AUTH_USER_MODEL



class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    webhook_type = models.CharField(max_length=15, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    text = models.CharField(max_length=300, null=True)

    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
    

class MT5_Webhook(models.Model):
    webhook_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) #tview 
    mt5_id = models.UUIDField(default=uuid.uuid4, editable=False)  
    subscription_id = models.CharField(max_length=15, null=True, blank=True)
    product_id = models.UUIDField(null=True, blank=True)
    variant_id = models.UUIDField(null=True, blank=True)
    renews_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    meta_id = models.UUIDField(default=uuid.uuid4, editable=False)
    hits = models.IntegerField(default=0)
    hit_limit = models.IntegerField(null=True, blank=True)
    identifier = models.CharField(default="mt5", max_length=10)
    old_alerts = GenericRelation(Alert, related_query_name='webhook')
    status = models.CharField(max_length=10, default="inactive") #lemon
    pause = models.CharField(max_length=10, default="inactive") #user


class Telegram_Webhook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    # update_payment_method = models.CharField(max_length=50, null=True, blank=True)
    webhook_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) # same as id, for referencing in orders
    subscription_id = models.UUIDField(null=True, blank=True)
    product_id = models.UUIDField(null=True, blank=True)
    variant_id = models.UUIDField(null=True, blank=True)
    renews_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    parse = models.BooleanField(default=False)
    hits = models.IntegerField(default=0)
    hit_limit = models.IntegerField(null=True, blank=True)
    chat_limit = models.IntegerField(default=0)
    old_alerts = GenericRelation(Alert)
    status = models.CharField(max_length=10, default="inactive") #lemon
    pause = models.CharField(max_length=10, default="inactive") #user
    identifier = models.CharField(default="tg", max_length=10)
    message_format = models.CharField(max_length=500, null=True, blank=True)
    message_prefix = models.CharField(max_length=200, null=True, blank=True)
    message_suffix = models.CharField(max_length=200, null=True, blank=True)

    def get_chat_limit(self):
        return self.chat_limit-len(self.telegramchat_set.all())



class TelegramChat(models.Model):
    chat_id = models.CharField(max_length=20)
    webhook = models.ForeignKey(Telegram_Webhook, on_delete=models.CASCADE)


class Discord_Webhook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    webhook_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subscription_id = models.UUIDField(null=True, blank=True)
    product_id = models.UUIDField(null=True, blank=True)
    variant_id = models.UUIDField(null=True, blank=True)
    renews_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    parse = models.BooleanField(default=False)
    hits = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default="inactive") #lemon
    pause = models.CharField(max_length=10, default="inactive") #user
    hit_limit = models.IntegerField(null=True, blank=True)
    chat_limit = models.IntegerField(default=0)
    old_alerts = GenericRelation(Alert)
    identifier = models.CharField(default="discord", max_length=10)
    message_format = models.CharField(max_length=500, null=True, blank=True)
    message_prefix = models.CharField(max_length=200, null=True, blank=True)
    message_suffix = models.CharField(max_length=200, null=True, blank=True)

    def get_chat_limit(self):
        return self.chat_limit-len(self.discordchat_set.all())

class DiscordChat(models.Model):
    channel_webhook_url = models.CharField(max_length=200)
    webhook = models.ForeignKey(Discord_Webhook, on_delete=models.CASCADE)

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    webhook_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subscription_id = models.UUIDField(null=True, blank=True)
    product_id = models.UUIDField(null=True, blank=True)
    variant_id = models.UUIDField(null=True, blank=True)
    renews_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    old_alerts = GenericRelation(Alert)
    hits = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default="inactive")
    hit_limit = models.IntegerField(null=True, blank=True)


class Order(models.Model):
    is_active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    literal_webhook_id = models.UUIDField(null=True, blank=True)
    webhook_name = models.CharField(max_length=30, null=True, blank=True)
    entry = models.FloatField()
    magic = models.IntegerField(null=True, blank=True)
    tt = models.IntegerField(null=True, blank=True)
    td = models.IntegerField(null=True, blank=True)
    ts = models.IntegerField(null=True, blank=True)
    trailing_type = models.IntegerField(null=True, blank=True) # -1 for percent, 1 for points
    sl = models.FloatField()
    side = models.CharField(max_length=5)
    quantity = models.FloatField()
    q_type = models.IntegerField(null=True, blank=True) # -1 for percent, 1 for qty
    ticker = models.CharField(max_length=10, null=True, blank=True)
    img_url = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    alert_text = models.CharField(max_length=5000, null=True, blank=True)
    trader_notes = models.CharField(max_length=5000, null=True, blank=True)
    rating = models.FloatField(default=0.0)



class TakeProfit(models.Model):
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class CloseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField()
    literal_webhook_id = models.UUIDField(null=True, blank=True)
    magic = models.IntegerField(null=True, blank=True)
    ticker = models.CharField(max_length=10, null=True, blank=True)
    _all = models.BooleanField(null=True, blank=True)

class ModifyOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField()
    literal_webhook_id = models.UUIDField(null=True, blank=True)
    magic = models.IntegerField(null=True, blank=True)
    ticker = models.CharField(max_length=10, null=True, blank=True)
    sl = models.FloatField(null=True, blank=True)
    tp = models.FloatField(null=True, blank=True)
