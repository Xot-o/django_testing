from http import HTTPStatus
from django.urls import reverse

from notes.tests.base_core import CoreTestCase, AUTHOR, USER, ANON_USER, SLUG


class TestRoutes(CoreTestCase):
    def test_pages_availability_for_anonymous_user(self):
        """Проверка доступа к страницам."""
        urls = (
            (reverse('notes:home'), self.client, HTTPStatus.OK, ANON_USER),
            (reverse('users:login'), self.client, HTTPStatus.OK, ANON_USER),
            (reverse('users:logout'), self.client, HTTPStatus.OK, ANON_USER),
            (reverse('users:signup'), self.client, HTTPStatus.OK, ANON_USER),
            (reverse(
                'notes:detail', args=(SLUG,)
            ), self.author_client, HTTPStatus.OK, AUTHOR),
            (reverse(
                'notes:edit', args=(SLUG,)
            ), self.author_client, HTTPStatus.OK, AUTHOR),
            (reverse(
                'notes:delete', args=(SLUG,)
            ), self.author_client, HTTPStatus.OK, AUTHOR),
            (reverse('notes:add'), self.user_client, HTTPStatus.OK, USER),
            (reverse('notes:list'), self.user_client, HTTPStatus.OK, USER),
            (reverse('notes:success'), self.user_client, HTTPStatus.OK, USER),
            (reverse(
                'notes:detail', args=(SLUG,)
            ), self.user_client, HTTPStatus.NOT_FOUND, USER),
            (reverse(
                'notes:edit', args=(SLUG,)
            ), self.user_client, HTTPStatus.NOT_FOUND, USER),
            (reverse(
                'notes:delete', args=(SLUG,)
            ), self.user_client, HTTPStatus.NOT_FOUND, USER),
        )
        for url, client, expected_status, user in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                    msg=(
                        f"Код ответа страницы {url} для {user} не "
                        f"соответствует ожидаемому."
                    ),
                )

    def test_redirects(self):
        """Проверка редиректа для неавторизованного пользователя."""
        urls = (
            reverse('notes:list'),
            reverse('notes:add'),
            reverse('notes:success'),
            reverse('notes:detail', args=(SLUG,)),
            reverse('notes:edit', args=(SLUG,)),
            reverse('notes:delete', args=(SLUG,)),
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f"{reverse('users:login')}?next={url}"
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url,
                    msg_prefix=(
                        f"Убедитесь, что у неавторизованного "
                        f"пользователя нет доступа к странице {url}."
                    ),
                )
