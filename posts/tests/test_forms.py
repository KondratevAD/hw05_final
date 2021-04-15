import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

from . import constants


class YatubeCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create_user(username=constants.username)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=constants.title,
            description=constants.description,
            slug=constants.slug,
        )
        cls.post_edit_page = reverse(
            'post_edit',
            kwargs={'username': constants.username, 'post_id': '1'}
        )
        cls.add_comment = reverse(
            'add_comment',
            kwargs={'username': constants.username2, 'post_id': '1'},
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        """Валидная форма создает запись."""
        posts_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=constants.small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': constants.text,
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            constants.NEW_POST_PAGE,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, constants.HOME_PAGE)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Валидная форма редактирует запись."""
        self.post = Post.objects.create(
            text=constants.text,
            author=self.user,
            group=self.group,
        )
        form_data = {
            'text': constants.text_edit,
            'group': self.group.id,
        }
        self.authorized_client.post(
            self.post_edit_page,
            data=form_data,
            follow=True,
        )
        post_edit = Post.objects.all()[0]
        self.assertEqual(post_edit.text, constants.text_edit)

    def test_add_comment(self):
        """Только авторизированный пользователь может создать комментарий"""
        self.guest_client = Client()
        self.user2 = User.objects.create_user(username=constants.username2)
        self.post = Post.objects.create(
            text=constants.text,
            author=self.user2,
            group=self.group,
        )
        form_data = {'text': 'TestComment'}
        post_comment = Post.objects.all()[0].comments.count()
        self.guest_client.post(
            self.add_comment,
            data=form_data,
            follow=True,
        )
        post_comment_not_add = Post.objects.all()[0].comments.count()
        self.authorized_client.post(
            self.add_comment,
            data=form_data,
            follow=True,
        )
        post_comment_add = Post.objects.all()[0].comments.count()
        self.assertEqual(post_comment, post_comment_not_add)
        self.assertEqual(post_comment + 1, post_comment_add)
