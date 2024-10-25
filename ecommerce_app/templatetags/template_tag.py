from django import template
from constance import config
from ..models import Category

register = template.Library()

@register.simple_tag
def get_logo_url():
    return f"/media/{config.LOGO}" if hasattr(config, 'LOGO') else '/static/frontend/assets/images/logo/logo.png'

@register.simple_tag
def site_title():
    return config.SITE_TITLE
