from http import HTTPStatus

from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


def test_anonymous_user_cant_create_comment(news, form_data):
    """
    Проверяет, что анонимный пользователь
    не может создать комментарий.
    """
    client = Client()
    url = reverse('news:detail', args=[news.id])
    client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_can_create_comment(author_client, news, form_data):
    """
    Проверяет, что авторизованный пользователь
    может создать комментарий.
    """
    url = reverse('news:detail', args=[news.id])
    author_client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_user_cant_use_bad_words(author_client, news, form_data):
    """
    Проверяет, что пользователь не может использовать
    запрещённые слова в комментарии.
    """
    url = reverse('news:detail', args=[news.id])
    bad_words_date = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_date)
    form = response.context['form']
    assertFormError(form=form, field='text', errors=WARNING)


def test_author_can_delete_comment(author_client, news, comment):
    """
    Проверяет, что автор
    может удалить свой комментарий.
    """
    url_delete = reverse('news:delete', args=[comment.id])
    response = author_client.post(url_delete)
    assert response.status_code == HTTPStatus.FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_author_can_edit_comment(author_client, news, comment, form_data):
    """
    Проверяет, что автор может
    редактировать свой комментарий.
    """
    url_edit = reverse('news:edit', args=[comment.id])
    author_client.post(url_edit, data=form_data)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_delete_comment_of_another_user(
        not_author_client,
        news,
        comment,
        form_data
):
    """
    Проверяет, что пользователь
    не может удалить комментарий другого пользователя.
    """
    url_delete = reverse('news:delete', args=[comment.id])
    not_author_client.post(url_delete)
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        news,
        comment,
        form_data
):
    """
    Проверяет, что пользователь
    не может редактировать комментарий другого пользователя.
    """
    url_edit = reverse('news:edit', args=[comment.id])
    not_author_client.post(url_edit, data=form_data)
    comment.refresh_from_db()
    assert comment.text != form_data['text']
