from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from app_menu.models import Menu

register = template.Library()


@register.simple_tag
def draw_menu(name):
    """Отрисовка древовидного меню"""
    # Получаем текущий url
    current_url = reverse('index')
    # Получаем все пункты меню с заданным именем
    menu_items = Menu.objects.filter(name=name)
    # Построение древовидной структуры меню и отрисовка
    if menu_items.exists():
        menu_structure = build_menu_structure(menu_items[0])
        menu_html = build_menu_html(menu_structure, current_url)
        return mark_safe(menu_html)
    else:
        return ""


def build_menu_structure(menu_item):
    """
    Рекурсивное построение древовидной структуры меню
    :param menu_item:
    :return:
    """
    menu_structure = {"item": menu_item, "children": []}
    for child in menu_item.children.all():
        menu_structure["children"].append(build_menu_structure(child))
    return menu_structure


def build_menu_html(menu_structure, current_url):
    """
    Рекурсивное построение HTML кода для меню
    :param menu_structure:
    :param current_url:
    """
    html = '<ul>'
    for child in menu_structure["children"]:
        child_html = build_menu_html(child, current_url)
        html += '<li>'
        html += '<a href="' + conditional_escape(child["item"].url) + '"'
        if current_url.startswith(child["item"].url):
            html += ' class="active"'
        html += '>' + conditional_escape(child["item"].name) + '</a>'
        html += child_html
        html += '</li>'
    html += '</ul>'
    return html


register.simple_tag(draw_menu)
