from django.forms import ModelForm, Textarea, TextInput, CheckboxInput
from signal_api.models import Telegram_Webhook, Discord_Webhook, MT5_Webhook


class Telegram_Webhook_Form(ModelForm):
    class Meta:
        model = Telegram_Webhook
        fields = ["name", "message_prefix", "message_suffix", "parse", "message_format"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Webhook Name",
                    "style": "background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
           
                }
            ),
            "message_prefix": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional text placed before all your telegram alerts.",
                    "style": "width: 70%;height:60px;background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
            "message_suffix": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional text placed after all your telegram alerts.",
                    "style": "width: 70%;height:60px;background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
            "parse": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "onclick": "show_tg_parse(this)",
                    "checked": False,
                }
            ),
            "message_format": Textarea(
                attrs={
                    "class": "form-control tt-2",
                    "placeholder": " Optional text",
                    "style": "width: 70%;height:60px;background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
            # "channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
        }


class Discord_Webhook_Form(ModelForm):
    class Meta:
        model = Discord_Webhook
        fields = ["name", "message_prefix", "message_suffix", "parse", "message_format"]
        widgets = {
             "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Webhook Name",
                    "style": "background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
           
                }
            ),
            "message_prefix": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional text placed before all your discord alerts.",
                    "style": "width: 70%;height:60px;background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
            "message_suffix": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional text placed after all your discord alerts.",
                    "style": "width: 70%;height:60px;background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
            "parse": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "onclick": "show_tg_parse(this)",
                    "checked": False,
                }
            ),
            "message_format": Textarea(
                attrs={
                    "class": "form-control tt-2",
                    "placeholder": " Optional text",
                    "style": "width: 70%;height:60px;background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
            # "channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
        }


class MT5_Webhook_Form(ModelForm):
    class Meta:
        model = MT5_Webhook
        fields = ["name"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name...",
                    "style": "background: rgba(255, 255, 255, 0.22);box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);border: 1px solid rgba(255, 255, 255, 0.3);",
                }
            ),
        }
