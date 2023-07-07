from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING, BAD_WORDS
from conftest import NEW_COMMENT_TEXT, COMMENT_TEXT, PK
from django.urls import reverse

from news.models import Comment


pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news, form_data):
    """Проверка создания комментария анонимным пользователем."""
    expected_count = Comment.objects.count()
    client.post(reverse('news:detail', args=(PK,)), data=form_data)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count


def test_user_can_create_comment(author_client, author, news, form_data):
    """Проверка создания комментария авторизованным пользователем."""
    expected_count = Comment.objects.count() + 1
    response = author_client.post(
        reverse('news:detail', args=(PK,)), data=form_data
    )
    comments_count = Comment.objects.count()
    new_comment = Comment.objects.get()
    assertRedirects(
        response,
        f"{reverse('news:detail', args=(PK,))}#comments"
    )
    assert expected_count == comments_count
    assert all(
        (
            new_comment.text == form_data['text'],
            new_comment.author == author,
            new_comment.news == news,
        )
    )


def test_author_can_delete_comment(author_client, comment, pk_news):
    """Проверка удаления комментария автором."""
    expected_count = Comment.objects.count() - 1
    response = author_client.delete(
        reverse('news:delete', args=(PK,))
    )
    comments_count = Comment.objects.count()
    assertRedirects(
        response,
        f"{reverse('news:detail', args=(PK,))}#comments"
    )
    assert expected_count == comments_count


@pytest.mark.parametrize('word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, news, word):
    """Проверка цензурных слов в форме."""
    expected_count = Comment.objects.count()
    bad_words_data = {'text': f"Какой-то текст, {word}, еще текст"}
    response = author_client.post(
        reverse('news:detail', args=(PK,)),
        data=bad_words_data
    )
    comments_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert expected_count == comments_count


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    """Проверка удаления комментария не автором."""
    expected_count = Comment.objects.count()
    response = admin_client.delete(
        reverse('news:delete', args=(PK,))
    )
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count


def test_author_can_edit_comment(
    author, author_client, comment, pk_news, form_data
):
    """Проверка редактирований комментария автором."""
    expected_count = Comment.objects.count()
    response = author_client.post(
        reverse('news:edit', args=(PK,)), data=form_data)
    assertRedirects(
        response, f"{reverse('news:detail', args=(PK,))}#comments"
    )
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert expected_count == comments_count
    assert all((comment.text == NEW_COMMENT_TEXT, comment.author == author))


def test_user_cant_edit_comment_of_another_user(
    author, admin_client, comment, pk_news, form_data
):
    """Проверка редактирований комментария не автором."""
    expected_count = Comment.objects.count()
    response = admin_client.post(
        reverse('news:edit', args=(PK,)),
        data=form_data
    )
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count
    assert all((comment.text == COMMENT_TEXT, comment.author == author))
