from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

from . import constants


class YatubeURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=constants.username)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=constants.title,
            slug=constants.slug,
            description=constants.description,
        )
        cls.post = Post.objects.create(
            text=constants.text,
            author=cls.user,
            group=cls.group,
        )
        cls.post_edit_page = reverse(
            'post_edit',
            kwargs={'username': constants.username, 'post_id': '1'}
        )
        cls.post_page = reverse(
            'post',
            kwargs={'username': constants.username, 'post_id': '1'}
        )

    def test_urls_guest_client(self):
        """Доступность страниц неавторизированным пользователям"""
        templates_url_names = (
            constants.HOME_PAGE,
            constants.group_page,
            constants.profile_page,
            self.post_page,
        )
        for reversed_name in templates_url_names:
            response = self.guest_client.get(reversed_name)
            self.assertEqual(response.status_code, 200)

    def test_urls_authorized_client(self):
        """Доступность страниц авторизированным пользователям"""
        templates_url_names = (
            constants.HOME_PAGE,
            constants.group_page,
            constants.NEW_POST_PAGE
        )
        for reversed_name in templates_url_names:
            response = self.authorized_client.get(reversed_name)
            self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'index.html': constants.HOME_PAGE,
            'group.html': constants.group_page,
            'new.html': constants.NEW_POST_PAGE,
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_url_post_edit(self):
        """Доступность страницы post_edit разным пользователям"""
        self.user2 = User.objects.create_user(username='TestUser2')
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)
        condition_users = {
            self.guest_client: 302,
            self.authorized_client: 200,
            self.authorized_client2: 302,
        }
        for user, code in condition_users.items():
            with self.subTest():
                response = user.get(self.post_edit_page)
                self.assertEqual(response.status_code, code)

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        """Страница post_edit перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            self.post_edit_page,
            follow=True
        )
        self.assertRedirects(
            response,
            '/auth/login/?next=%2FTestUser%2F1%2Fedit%2F'
        )

    def test_post_edit_uses_correct_template(self):
        """Страница post_edit использует соответствующий шаблон."""
        response = self.authorized_client.get(self.post_edit_page)
        self.assertTemplateUsed(response, 'new.html')

    def test_page_not_found(self):
        """Сервер возвращает код 404"""
        response = self.guest_client.get(constants.PAGE_NOT_FOUND)
        self.assertEqual(response.status_code, 404)
