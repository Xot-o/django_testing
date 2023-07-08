from datetime import date

import pytest
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from conftest import PK
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count_order(client, news_list):
    """Проверка кол-ва новостей и их сортировку на главной."""
    response = client.get(reverse('news:home'))
    object_list = list(response.context['object_list'])
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comments_order(client, news, comments_list):
    """Проверка сортировки комментариев."""
    response = client.get(reverse('news:detail', args=(PK,)))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert isinstance(all_comments[0].created, timezone.datetime)
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


def test_client_has_form(client, admin_client, news):
    """Проверка доступности формы комментария и её типа."""
    response = client.get(reverse('news:detail', args=(PK,)))
    admin_response = admin_client.get(reverse('news:detail', args=(PK,)))
    assert (
        isinstance(admin_response.context['form'], CommentForm)
        and 'form' not in response.context
    )
