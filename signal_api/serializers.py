from rest_framework import serializers
from .models import Order, TakeProfit


class TakeProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakeProfit
        fields = ["price", "is_active"]

class OrderSerializer(serializers.ModelSerializer):
    profit_targets = TakeProfitSerializer(many=True, required=False)
    class Meta:
        model=Order
        fields = [
            "is_active",
            "entry",
            "magic",
            "tt",
            "td",
            "ts",
            "trailing_type",
            "sl",
            "magic ",
            "side",
            "quantity",
            "q_type",
            "ticker",
            "date_created",
            "trader_notes",
            "rating",
        ]