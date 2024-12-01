
from django import template

register = template.Library()

@register.filter
def star_rating(value):
    filled_stars = min(int(value), 5)
    empty_stars = max(0, 5 - int(value))
    stars = ['filled'] * filled_stars + ['empty'] * empty_stars
    return stars

@register.filter
def for_three_loop(lst):
    return [lst[i:i+3] for i in range(0, len(lst), 3)]
