# -*- coding: utf-8 -*-
from django.template import Library
# from django.template.base import TemplateSyntaxError
# from django.template import Node
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

register = Library()

@register.assignment_tag(takes_context=True)
def notifications_unread(context, level=None):
    if 'user' not in context:
        return ''

    user = context['user']

    if user.is_anonymous():
        return ''
    if level is None:
        return user.notifications.unread().count()
    else:
        return user.notifications.filter(level=level).unread().count()

@register.simple_tag
def show_levels(value, exclude='', include=''):
    """
    Joins a list with a string, like Python's ``str.join(list)``. but allow
    for excluding or including a value
    """
    levels = value[:]
    if include and include not in levels:
        levels.append(include)
    if exclude and exclude in levels:
        levels.remove(exclude)
    levels = map(force_text, levels)
    try:
        data = ','.join(levels)
    except AttributeError:  # fail silently but nicely
        return levels
    return mark_safe(data)
