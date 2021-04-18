import shutil
import tempfile
from django.core.cache import cache
from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

from . import constants


class YatubePagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create_user(username=constants.username)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=constants.title,
            slug=constants.slug,
            description=constants.description,
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=constants.small_gif,
            content_type='image/gif'
        )
        cls.form_data = {
            'text': constants.text,
            'group': cls.group.id,
            'image': cls.uploaded,
        }
        cls.authorized_client.post(
            constants.NEW_POST_PAGE,
            data=cls.form_data,
            follow=True,
        )
        cls.post = Post.objects.all()[0]
        cls.post_edit_page = reverse(
            'post_edit',
            kwargs={'username': constants.username, 'post_id': '1'}
        )
        cls.post_page = reverse(
            'post',
            kwargs={'username': constants.username, 'post_id': '1'}
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': constants.HOME_PAGE,
            'new.html': constants.NEW_POST_PAGE,
            'group.html': (constants.group_page),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_and_profile_page_shows_correct_context(self):
        """Шаблон index и profile сформирован с правильным контекстом."""
        templates_pages_names = (
            constants.HOME_PAGE,
            constants.profile_page,
        )
        for reversed_name in templates_pages_names:
            response = self.authorized_client.get(reversed_name)
            first_object = response.context['page'][0]
            self.assertEqual(first_object.text, constants.text)
            self.assertEqual(first_object.pub_date, self.post.pub_date)
            self.assertEqual(first_object.author.username, constants.username)
            self.assertEqual(first_object.group.title, constants.title)
            self.assertEqual(first_object.image, self.post.image)

    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            constants.group_page
        )
        object_group = response.context['group']
        first_object_posts = response.context['page'][0]
        self.assertEqual(object_group.title, constants.title)
        self.assertEqual(object_group.slug, constants.slug)
        self.assertEqual(object_group.description, constants.description)
        self.assertEqual(first_object_posts.text, constants.text)
        self.assertEqual(first_object_posts.pub_date, self.post.pub_date)
        self.assertEqual(
            first_object_posts.author.username,
            constants.username
        )
        self.assertEqual(first_object_posts.group.title, constants.title)
        self.assertEqual(first_object_posts.image, self.post.image)

    def test_new_post_shows_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(constants.NEW_POST_PAGE)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_with_group_shows_correct_template(self):
        """Post c группой отображается только на нужных шаблонах."""
        templates_url_names = (
            constants.HOME_PAGE,
            constants.group_page
        )
        for reversed_name in templates_url_names:
            response = self.authorized_client.get(reversed_name)
            first_object = response.context['page'][0]
            self.assertEqual(first_object.text, constants.text)
            self.assertEqual(first_object.pub_date, self.post.pub_date)
            self.assertEqual(first_object.author.username, constants.username)
            self.assertEqual(first_object.group.title, constants.title)

    def test_post_with_group_not_shows_incorrect_template(self):
        """Post c группой не отображается на шаблоне другой группы."""
        self.group_other = Group.objects.create(
            title=constants.title_other,
            slug=constants.slug_other,
            description=constants.description_other,
        )
        self.post_other = Post.objects.create(
            text=constants.text_other,
            author=self.user,
            group=self.group_other,
        )
        response = self.authorized_client.get(reverse(
            'group',
            kwargs={'slug': constants.slug_other}
        ))
        first_object = response.context['page'][0]
        self.assertNotEqual(first_object.text, constants.text)
        self.assertNotEqual(first_object.pub_date, self.post.pub_date)
        self.assertNotEqual(first_object.group.title, constants.title)

    def test_post_page_shows_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.post_page)
        first_object = response.context['post']
        self.assertEqual(first_object.text, constants.text)
        self.assertEqual(first_object.pub_date, self.post.pub_date)
        self.assertEqual(first_object.author.username, constants.username)
        self.assertEqual(first_object.group.title, constants.title)
        self.assertEqual(first_object.image, self.post.image)

    def test_post_edit_shows_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.post_edit_page)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_paginator_index_page_shows_correct_context(self):
        """Paginator передает в шаблон index заданое количество постов."""
        post = [Post(
            text=constants.text,
            author=self.user,
            group=self.group) for i in range(13)]
        self.posts = Post.objects.bulk_create(
            post
        )
        response = self.authorized_client.get(constants.HOME_PAGE)
        posts_count = response.context['page'].paginator.per_page
        self.assertEqual(posts_count, settings.PAGINATOR_PAGE)

    def test_cache_index_page(self):
        """Кэш страницы index работает корректно"""
        response = self.authorized_client.get(constants.HOME_PAGE)
        context = response.content
        Post.objects.create(
            text=constants.text_other,
            author=self.user,
            group=self.group,
        )
        response = self.authorized_client.get(constants.HOME_PAGE)
        context_add = response.content
        cache.clear()
        response = self.authorized_client.get(constants.HOME_PAGE)
        context_clean = response.content
        self.assertEqual(context, context_add)
        self.assertNotEqual(context, context_clean)

    def test_follow_unfollow(self):
        """
        Авторизированный пользователь может
        подписаться/отписатся на автора
        """
        author = User.objects.create_user(username=constants.username2)
        follower = self.user.follower.count()
        self.authorized_client.get(
            reverse('profile_follow', kwargs={'username': author}),
        )
        follower_add = self.user.follower.count()
        self.authorized_client.get(
            reverse('profile_unfollow', kwargs={'username': author}),
        )
        unfollow = self.user.follower.count()
        self.assertEqual(follower + 1, follower_add)
        self.assertEqual(follower_add - 1, unfollow)

    def test_follow_index_page_shows_correct_context(self):
        """Шаблон follow_index сформирован с правильным контекстом."""
        author = User.objects.create_user(username=constants.username2)
        self.authorized_client.get(
            reverse('profile_follow', kwargs={'username': author}),
        )
        response = self.authorized_client.get(constants.FOLLOW)
        context = response.context['page'].end_index()
        Post.objects.create(
            text=constants.text_other,
            author=author,
            group=self.group,
        )
        response = self.authorized_client.get(constants.FOLLOW)
        context_add = response.context['page'].end_index()
        self.authorized_client.get(
            reverse('profile_unfollow', kwargs={'username': author}),
        )
        response = self.authorized_client.get(constants.FOLLOW)
        context_not_add = response.context['page'].end_index()
        self.assertEqual(context + 1, context_add)
        self.assertEqual(context, context_not_add)
