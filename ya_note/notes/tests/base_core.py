from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

USER_MODEL = get_user_model()
SLUG = 'note-slug'
AUTHOR = 'Автор'
USER = 'Пользователь'
ANON_USER = 'Анонимный пользователь'
FIELD_NAMES = ('title', 'text', 'slug', 'author')
FIELD_DATA = ('Заголовок', 'Текст заметки', SLUG)
FIELD_NEW_DATA = ('Новый заголовок', 'Новый текст', 'new-slug')


class CoreTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = USER_MODEL.objects.create(username=USER)
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            **dict(zip(FIELD_NAMES, (*FIELD_DATA, cls.author)))
        )
