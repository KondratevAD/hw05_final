from django.test import TestCase

from posts.models import Group, Post, User

from . import constants


class YatubeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=constants.username)
        cls.group = Group.objects.create(
            title=constants.title,
            description=constants.description,
        )
        cls.post = Post.objects.create(
            text=constants.text,
            author=cls.user,
            group=cls.group,
        )
        cls.get_verbose_name_post = cls.post._meta.get_field
        cls.get_verbose_name_group = cls.group._meta.get_field

    def test_verbose_name_post(self):
        """verbose_name в полях Post совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Post.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_post(value).verbose_name, expected)

    def test_verbose_name_group(self):
        """verbose_name в полях Group совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Group.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_group(value).verbose_name, expected)

    def test_help_text_post(self):
        """help_text в полях Post совпадает с ожидаемым."""
        for value, expected in constants.field_help_texts_Post.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_post(value).help_text, expected)

    def test_help_text_group(self):
        """help_text в полях Group совпадает с ожидаемым."""
        for value, expected in constants.field_help_texts_Group.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_group(value).help_text, expected)

    def test_object_name_is_post(self):
        """__str__  post - это строчка с содержимым post.text."""
        post = YatubeModelTest.post
        expected_object_name = post.text
        self.assertEquals(expected_object_name, str(post)[:15])

    def test_object_name_is_group(self):
        """__str__  group - это строчка с содержимым group.title."""
        group = YatubeModelTest.group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))
