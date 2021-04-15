from django.test import Client, TestCase

from posts.tests.constants import ABOUT_AUTHOR_PAGE, ABOUT_TECH_PAGE


class AboutViewsTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_pages_accessible_by_name(self):
        """Страницы author и tech доступны неавторизированному пользователю."""
        templates_url_names = (
            ABOUT_AUTHOR_PAGE,
            ABOUT_TECH_PAGE,
        )
        for reversed_name in templates_url_names:
            response = self.guest_client.get(reversed_name)
            self.assertEqual(response.status_code, 200)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'author.html': ABOUT_AUTHOR_PAGE,
            'tech.html': ABOUT_TECH_PAGE,
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
