from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_for_products')
def media_for_products(img_path):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not img_path:
        img_path = 'products/default.jpg'

    return f'{settings.MEDIA_URL}{img_path}'


@register.filter(name='media_for_users')
def media_for_users(img_path):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not img_path:
        img_path = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{img_path}'