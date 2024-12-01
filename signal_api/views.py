from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import telebot
import requests, datetime
import hashlib
import hmac
import logging
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import base64
from io import BytesIO
from reportlab.pdfgen import canvas


std_logger = logging.getLogger(__name__)
lemon_logger = logging.getLogger("lemon")


def send_messages(data: list, w):
    if w == "telegram":
        telegram_settings = settings.TELEGRAM
        bot = telebot.TeleBot(telegram_settings["token"])
        for x in data:
            try:
                if x[3] is not None:
                    bot.send_photo(x[0], x[3], x[2])
                bot.send_message(x[0], x[1])
            except:
                std_logger.error(e)
    elif w == "discord":
        discord_settings = settings.DISCORD
        for x in data:
            try:
                webhook_url = x[0]
                message = x[1]
                webhook = DiscordWebhook(url=webhook_url)
                embed = DiscordEmbed(
                    title="Alert Triggered Via ToT",
                    description=message,
                    color="03b2f8",
                )
                if x[2] is not None:
                    embed.set_image(url=x[2])
                webhook.add_embed(embed)
                response = webhook.execute()
                if response.status_code != 200:
                    std_logger.error(f"Webhook Error: {response.status_code} - {response.content}")
            except Exception as e:
                std_logger.error(e)


def parse_signal_hit(m: str):
    r = []
    for msg in m.split("\n"):
        d = {}
        msg = re.sub(
            "\s*(\W)\s*", r"\1", msg
        )  # Get rid of wild whitespaces between special chars, as well as double spaces
        params = msg.split(" ")
        for i, v in enumerate(params):
            if "http" in v:
                img_url = params.pop(i)
                d.update({"img": img_url})

        command = params[0].lower()
        d.update({"side": command})
        if msg.lower() == "close":
            d.update(
                {
                    "all": True,
                }
            )

        if command == "close":
            try:
                magic = int(params[1])
                d.update({"m", magic})
            except ValueError:
                d.update({"symbol": params[1].upper()})

        elif command == "modify":
            try:
                magic = int(params[1])
                d.update({"m", magic})
            except ValueError:
                d.update({"symbol": params[1].upper()})
            for p in params:
                k, v = p.split("=")
                if k.lower() == "tp":
                    d.update({"tp": v})
                if k.lower() == "sl":
                    if v.lower == "b":  # breakeven
                        v = -1
                    d.update({"sl": v})

        elif command in ["buy", "sell"]:
            d.update({"symbol": params[1].upper()})

            for param in params[2:]:
                if "=" in param:
                    key, value = param.split("=")
                    key = key.lower()

                    if key in ["p", "price"]:
                        d.update({"price": value})
                    elif key == "link":
                        d.update({"img": value})
                    elif key.startswith("tp"):
                        d.setdefault("tp", []).append(value)
                    elif key == "sl":
                        d.update({"sl": value})
                    elif key == "e":
                        d.update({"e": value})
                    elif key == "q":
                        if "%" in value:
                            d.update({"qt": "1"})
                        else:
                            d.update({"qt": "-1"})
                        d.update({"q": value})
                    elif key == "m":
                        d.update({"m": value})
                    elif key == "tt":
                        d.update({"tt": value})
                    elif key == "td":
                        d.update({"td": value})
                    elif key == "ts":
                        d.update({"ts": value})
        r.append(d)
    return r


def parse(params: dict, webhook):
    if params["side"] in ["buy", "sell"]:
        default_template = """
{{side}} {{symbol}}


Entry Price: {{e}}
Quantity: {{q}}
Profit Targets: {{tp}}
Stop Loss: {{sl}}
--------------------
Trailing Settings
Trigger: {{tt}}
Distance: {{td}}
Step: {{ts}}

            """
    elif params["side"] == "modify":
        m = f"""
Modify {params.get("symbol", None) or "#"+str(params.get("m", None))}

SL: {params.get("sl", None) or "Unchanged"}
TP: {params.get("tp", None) or "Unchanged"}
{"Break Even"}
        """
        return m

    elif params["side"] == "close":
        m = f"""
Close {params.get("symbol", None) or params.get("m", None)  or "all previously opened trades"}

        """
        return m

    if webhook.message_format == None:
        template = default_template
    else:
        template = webhook.message_format

    # Using a more robust replacement method to avoid replacing unintended text
    m = template
    for k, v in params.items():
        placeholder = f"{{{{{k}}}}}"  # Creates a placeholder in the format {{key}}
        m = m.replace(placeholder, str(v))

    # Remove any remaining placeholders that were not replaced
    m = re.sub(r"\{\{[^\{\}]*\}\}", "", m)
    if params.get("tt", None) == None:
        m = m.split("--------------------")[0]
    m = (
        m.replace("{{sl}}", "None")
        .replace("{{e}}", "Current")
        .replace("{{tp}}", "None")
        .replace("{{q}}", "Your Choice")
    )
    return m


def parse_incoming_webhook_request(w, pk, data):
    webhook = (
        MT5_Webhook.get(id=pk).first()
        or Telegram_Webhook.get(id=pk).first()
        or Discord_Webhook.get(id=pk).first()
        or Journal.get(id=pk).first()
    )
    if webhook.hits > webhook.hit_limit:
        return JsonResponse({"status": "limit exceeded"})
    tradingview_message = data.get("message")
    for params in parse_signal_hit(tradingview_message):
        if params.get("side").lower() == "close":
            order = Order.objects.filter(
                magic=params.get("m", None), literal_webhook_id=webhook.webhook_id
            ).first()
            o = CloseOrder.objects.create(
                is_active=True,
                literal_webhook_id=webhook.webhook_id,
                webhook_name=webhook.name,
                order=order,
                user=order.user,
                ticker=params.get("symbol", None),
                magic=params.get("m", None),
                _all=params.get("all", False),
            )
            o.save()
        elif params.get("side").lower() == "modify":
            order = Order.objects.filter(
                magic=params.get("m", None), literal_webhook_id=webhook.webhook_id
            ).first()
            if order:
                modify_order = ModifyOrder.objects.create(
                    is_active=True,
                    order=order,
                    user=order.user,
                    literal_webhook_id=webhook.webhook_id,
                    webhook_name=webhook.name,
                    ticker=params.get("symbol", None),
                    magic=params.get("m", None),
                    sl=params.get("sl", None),
                    tp=params.get("tp", None),
                )
                modify_order.save()

        elif params.get("side").lower() in ["buy", "sell"]:
            o = Order.objects.create(
                is_active=True,
                literal_webhook_id=webhook.webhook_id,
                webhook_name=webhook.name,
                ticker=params.get("symbol", ""),
                side=params.get("side", ""),
                tt=params.get("tt", None),
                ts=params.get("ts", None),
                td=params.get("td", None),
                sl=params.get("sl", None),
                magic=params.get("m", None),
                quantity=params.get("q", None),
                entry=params.get("e", None),
                q_type=params.get("qt", None),
                trailing_type=params.get("trail_type"),
            )

            o.save()
            tp_values = params.get("tp", [])
            for tp_value in tp_values:
                tp = TakeProfit.objects.create(is_active=True, order=o, price=tp_value)
            tp.save()
    chats = None
    if w == "telegram":
        chats = webhook.telegramchat_set.all()
    elif w == "discord":
        chats = webhook.discordchat_set.all()
    if chats:
        data = parse(params, telegram_webhook)
        res = [[chat.chat_id, data, params.get("img", None)] for chat in chats]
        print(res)
        send_message(res, w)
    webhook.hits += 1
    webhook.save()
    return JsonResponse({"status": "success"})


class TelegramAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return parse_incoming_webhook_request(
            "telegram", self.kwargs["pk"], self.request.data
        )


class JournalAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return parse_incoming_webhook_request(
            "journal", self.kwargs["pk"], self.request.data
        )


class MT5APIView(APIView):
    def post(self, *args, **kwargs):
        return parse_incoming_webhook_request(
            "mt5", self.kwargs["pk"], self.request.data
        )


class DiscordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return parse_incoming_webhook_request(
            "discord", self.kwargs["pk"], self.request.data
        )


class NoteAPIView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data, dict(data).get("note-rating"))
        order = get_object_or_404(Order, id=data.get("pk"))
        note = data.get("note-text", order.trader_notes)
        rating = dict(data).get("note-rating", order.rating)
        print(note, rating)
        order.trader_notes = note
        order.rating = rating
        order.save()
        print(note, rating)
        return JsonResponse({"status": "success"})

    def get(self, request, *args, **kwargs):
        wid = self.request.query_params.get("wid", None)
        webhook_type = self.request.query_params.get("w", None)
        if webhook_type in ["mt5", "tg", "discord"]:
            model_map = {
                "mt5": MT5_Webhook,
                "tg": Telegram_Webhook,
                "discord": Discord_Webhook,
            }
            model = model_map[webhook_type]
            webhook = model.objects.filter(webhook_id=wid).first()
            if not webhook:
                return HttpResponseNotFound("Webhook not found")

            queryset = Order.objects.filter(literal_webhook_id=wid).all()
            buffer = BytesIO()
            print(wid, queryset)
            text = "\n-----------------------------------------------\n"
            for order in queryset:
                print(order)
                t = f"""
                Trailing Settings
                Trigger: {order.tt}
                Step: {order.ts}
                Distance: {order.td}
                """
                modify = "\n".join(
                    [
                        f"Modify {m.magic or m.ticker} Tp: {m.tp or 'No Change'} Sl: {m.sl or 'No Change'}"
                        for m in order.modifyorder_set.all()
                    ]
                )
                close = "\n".join(
                    [
                        f"Close {m.magic or m.ticker or 'All'}"
                        for m in order.closeorder_set.all()
                    ]
                )
                at = f"""
                {order.date_created.strftime("%m/%d/%Y, %H:%M:%S")}
                {order.side.upper()} - {order.ticker.upper()}
                Chart Image: {order.img_url}
                
                Entry: {order.entry}
                Profit Targets: {", ".join([str(tp.price) for tp in order.takeprofit_set.all()])}
                Stop Loss(initial): {order.sl}
                Quantity: {order.quantity}{"%" if order.q_type < 0 else ""}
                
                {t if order.tt is not None else ""}
                Related Commands:
                
                {modify}
                {close}
                
                Trade Rating: {order.rating}
                Trade Notes: 
                
                {order.trader_notes}
                """
                buffer.write(at.encode("utf-8"))
                buffer.write(b"\n-----------------------------------------------\n")

            buffer.seek(0)
            txt_content = buffer.read().decode("utf-8")
            encoded_txt = base64.b64encode(txt_content.encode("utf-8")).decode("utf-8")
            print(encoded_txt)
            return JsonResponse({"message": encoded_txt})
        else:
            return HttpResponseNotAllowed(["GET"])


def handle_lemon_webhook(id, wid, reason):
    url = f"https://api.lemonsqueezy.com/v1/subscriptions/{str(id)}"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {settings.LEMONSQUEEZY['api_key']}",
    }
    result = requests.get(url, headers=headers).json()
    pid = result["data"]["attributes"]["product_id"]
    vid = result["data"]["attributes"]["variant_id"]
    status = result["data"]["attributes"]["status"]
    renews_at = result["data"]["attributes"]["renews_at"]

    if pid == settings.LEMONSQUEEZY["telegram_pid"]:
        t = Telegram_Webhook.objects.filter(webhook_id=wid).first()

    elif pid == settings.LEMONSQUEEZY["discord_pid"]:
        t = Discord_Webhook.objects.filter(webhook_id=wid).first()

    elif pid == settings.LEMONSQUEEZY["mt5_pid"]:
        t = MT5_Webhook.objects.filter(webhook_id=wid).first()

    if reason == "subscription_created":
        t.variant_id = vid
        t.product_id = pid
        t.subscription_id = id
        t.status = "active"
        t.pause = "active"
        t.renews_at = datetime.datetime.strptime(renews_at, "%Y-%m-%dT%H:%M:%S.%fZ")

        if vid in settings.LEMONSQUEEZY["telegram_vids"]:
            hit_limit = settings.LEMONSQUEEZY["telegram_vids"][vid]
            t.hit_limit = hit_limit
            t.chat_limit = int(
                result["data"]["attributes"]["first_subscription_item"]["quantity"]
            )

        if vid in settings.LEMONSQUEEZY["discord_vids"]:
            hit_limit = settings.LEMONSQUEEZY["discord_vids"][vid]
            t.hit_limit = hit_limit
            t.chat_limit = int(
                result["data"]["attributes"]["first_subscription_item"]["quantity"]
            )

        if vid in settings.LEMONSQUEEZY["mt5_vids"]:
            hit_limit = settings.LEMONSQUEEZY["mt5_vids"][vid]
            t.hit_limit = hit_limit

    elif status in ["past_due", "unpaid"]:
        ends_at = result["data"]["attributes"]["ends_at"]
        t.ends_at = datetime.datetime.strptime(ends_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    elif status == "active":
        t.ends_at = None
        t.status = "active"

    elif status == "on_trial":
        t.status = "active"
        t.ends_at = datetime.datetime.strptime(
            result["data"]["attributes"]["trial_ends_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

    elif status == "expired":
        t.status = "inactive"

    t.save()

    return [pid, vid]


class LemonAPIView(APIView):
    def post(self, request, *args, **kwargs):
        signature = request.META["HTTP_X_SIGNATURE"]
        secret = settings.lemon_signed_secret

        digest = hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(digest, signature):
            lemon_logger.critical(f"Attempted fake lemon api hit: {request}")
            # logging here
        data = request.POST
        lemon_logger.info(str(datetime.datetime.now()) + "   " + str(data))
        subscription_id = data["data"]["attributes"]["subscription_id"]
        reason = data["meta"]["event_name"]
        if reason == "renewal":
            return  # check if webhook is inactive, and activate it
        webhook_id = data["meta"]["custom_data"]["webhook_id"]
        handle_lemon_webhook(subscription_id, webhook_id, reason)

        return JsonResponse({"status": "success"})


class EAAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mt5_account = get_object_or_404(MT5_Webhook, webhook_id=self.kwargs["pk"])
        order = Order.objects.filter(is_active=True, mt5_webhook=mt5_account).first()
        close_order = CloseOrder.objects.filter(
            is_active=True, mt5_webhook=mt5_account
        ).first()
        modify_order = ModifyOrder.objects.filter(
            is_active=True, mt5_webhook=mt5_account
        ).first()
        if not (order or close_order or modify_order):
            return JsonResponse({"status": "no orders"})
        if order:
            tps = order.takeprofit_set.filter(is_active=True).all()
            if not tps:
                order.is_active = False
                order.save()
                return JsonResponse({"status": "no orders"})

            tp = tps.first()
            tp.is_active = False
            tp.save()
            return JsonResponse(
                {
                    "status": "success",
                    "command": "neworder",
                    "entry": order.entry,
                    "sl": order.sl,
                    "tp": tp.price,
                    "tt": order.tt,
                    "ts": order.ts,
                    "td": order.td,
                    "magic": order.magic,
                    "trailing_type": order.trailing_type,
                    "q_type": order.q_type,
                    "ticker": order.ticker,
                    "side": order.side,
                }
            )
        elif close_order:
            return JsonResponse(
                {
                    "status": "success",
                    "command": "close",
                    "magic": close_order.magic,
                    "ticker": close_order.ticker,
                    "all": close_order._all,
                }
            )
        elif modify_order:
            return JsonResponse(
                {
                    "status": "success",
                    "command": "close",
                    "magic": modify_order.magic,
                    "ticker": modify_order.ticker,
                    "sl": modify_order.sl,
                    "tp": modify_order.price,
                }
            )
