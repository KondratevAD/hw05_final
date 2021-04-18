from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        'Содержание поста',
        help_text='Введите содержание вашего поста.'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение'
    )

    def __str__(self) -> str:
        """Возвращает пост в удобоваримом виде

        Ключевой аргумент:
        text -- Содержание поста
        """
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Введите заголовок вашего поста.'
    )
    slug = models.SlugField('URL', unique=True)
    description = models.TextField(
        'Описание',
        help_text='Введите описание вашего поста.'
    )

    def __str__(self) -> str:
        """Возвращает заголовок группы

        Ключевой аргумент:
        title -- Заголовок группы
        """
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        'Комментарий',
        help_text='Введите ваш комментарий.'
    )
    created = models.DateTimeField('Дата комментария', auto_now_add=True)

    def __str__(self) -> str:
        """Возвращает текст комментария

        Ключевой аргумент:
        text -- Содержание комментария
        """
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписант'
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
