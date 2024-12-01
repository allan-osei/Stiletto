import requests
import json


def create_checkout(user_id="heysup"):
    api_url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NGQ1OWNlZi1kYmI4LTRlYTUtYjE3OC1kMjU0MGZjZDY5MTkiLCJqdGkiOiJjNTk5ZTA4YmFhNjk4YzdkYTkxZTQzMGIzOThjYTAwOWZjNmZiNDcwOTBlZGIzNzUwMzliZjBlMDM4NmUyMjVhNzU3MGVkMTYyOTdkNjE0MyIsImlhdCI6MTcwMTgxMjcxOS43ODYzNjEsIm5iZiI6MTcwMTgxMjcxOS43ODYzNjUsImV4cCI6MjAxNzQzMTkxOS43NTkxMTgsInN1YiI6IjE3MDQxODciLCJzY29wZXMiOltdfQ.JiXJEyZANZ1bRcAItMsUZBVkp5OeADJ7eQ6ssDrZaejS1EVQ3wxB1ggsCHvjt6838x6IJ5mWkg5jKC2t-zinpKFKzw7SybyjTvJ4i7RN7Kwt49E-L_8EMVhm2kRoBJ8MZ82OUPmjfNp8UKjhJqV3NrtDJn4zyOJW6veZRPZRFO4_QGtNFebv_Tl13Cz1_8f5qQxNhMNnpWnBSmTdfhOeHRiGI8zmnEwC-U4_Z_wJY0NVfFGO4AeDt3ZBsDcv_BK3VNk21oETvf434E0icnhf5Zvc5hbvfoo_kTDcAXovpZ7RPDwUgKQO931zCKbfBG8C0jpCBRCN8Mw-3sKpHo8tO8M2jW8vNjI39UAhVTXV6TlYvv-DeyLVLcbnSyjrYeW5lQTDEyB8lozcA43ajFZoC1znDghqN1DWgLM1aJFheDEEUq2hVDyQDXM2pd6ZhgdikbSe7Aj-t9o3g9wkuOjNbkeKvGD9u0jlPfkqdJV2_-_l28-o80vS2M0suI66h7uR",
    }
    data = {
        "type": "checkouts",
        "attributes": {"product_options": {"enabled_variants": []}},
        "checkout_data": {"custom": {"user_id": str(user_id)}},
        "preview": True,
        "relationships": {
            "store": {"data": {"type": "stores", "id": "58249"}},
            "variant": {"data": {"type": "variants", "id": "145362"}},
        },
    }
    "https://stiletto.lemonsqueezy.com/checkout/buy/e323c57d-b490-4d15-96fb-00b0ccc1a91c?checkout[custom][user_id]={uid}"
    print(
        requests.get(
            "https://api.lemonsqueezy.com/v1/subscriptions/208545",
            headers=headers,
        ).json()


    )

    """Close EURUSD
    Close 7
    Buy GBPUSD e=1.2345 tp=1.24333 sl=1.02222 q=0.1 m=7 tt=100 td=200 ts=10 q=4% i https://example.com/pictures/chart/vh36352
    Modify 7 tp=0, sl=0
    Modify 7 sl=b
    """
if not (False or False):
    print("hit")


