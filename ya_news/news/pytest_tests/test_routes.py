from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from conftest import ADMIN, AUTHOR, CLIENT, PK
from django.urls import reverse
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (reverse('news:home'), CLIENT, HTTPStatus.OK),
        (reverse('news:detail', args=(PK,)), CLIENT, HTTPStatus.OK),
        (reverse('users:login'), CLIENT, HTTPStatus.OK),
        (reverse('users:logout'), CLIENT, HTTPStatus.OK),
        (reverse('users:signup'), CLIENT, HTTPStatus.OK),
        (reverse('news:edit', args=(PK,)), AUTHOR, HTTPStatus.OK),
        (reverse('news:detail', args=(PK,)), AUTHOR, HTTPStatus.OK),
        (reverse('news:edit', args=(PK,)), ADMIN, HTTPStatus.NOT_FOUND),
        (reverse('news:delete', args=(PK,)), ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability_for_anonymous_user(
    url, parametrized_client, expected_status, comment
):
    """Проверка для доступа к страницам."""
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        reverse('news:edit', args=(PK,)),
        reverse('news:delete', args=(PK,)),
    )
)
def test_redirect_for_anonymous_client(client, url, comment):
    """Проверка редиректов для анонимного пользователя."""
    expected_url = f"{reverse('users:login')}?next={url}"
    response = client.get(url)
    assertRedirects(response, expected_url)
