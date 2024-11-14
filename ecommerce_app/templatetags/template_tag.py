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

@register.simple_tag
def office_address():
    return config.OFFICE_ADDRESS

@register.simple_tag
def contact1():
    return config.CONTACT1

@register.simple_tag
def contact2():
    return config.CONTACT2

@register.simple_tag
def support_mail():
    return config.SUPPORT_MAIL

@register.simple_tag
def powered_by():
    return config.POWERED_BY
