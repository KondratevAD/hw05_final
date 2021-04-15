import datetime as dt

from django.contrib.auth import get_user_model

from posts.models import Group


def year(request):
    """Возвращает год

        Ключевые аргументы:
        year -- сегодняшняя дата в формате: год
        """
    year = dt.datetime.now().strftime('%Y')
    return {'year': year}


def group(request):
    """Возвращает год

        Ключевые аргументы:
        year -- сегодняшняя дата в формате: год
        """
    group_button = Group.objects.all()
    return {'group_button': group_button}


def users(request):
    """Возвращает год

        Ключевые аргументы:
        year -- сегодняшняя дата в формате: год
        """
    User = get_user_model()
    user_button = User.objects.all()
    return {'user_button': user_button}
