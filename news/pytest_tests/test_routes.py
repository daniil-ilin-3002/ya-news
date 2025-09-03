from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name',
    (
        'news:home',
        'users:login',
        'users:signup',
    )
)
def test_pages_availability_for_anonymous_user(author_client, name):
    """Общедоступные страницы (home, login, signup) возвращают 200."""
    url = reverse(name)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_page(author_client, news):
    """
    Страница новости detail доступна и
    отвечает 200 для авторизованного клиента.
    """
    url = reverse('news:detail', kwargs={'pk': news.id})
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status, should_redirect',
    (
        (lf('client'), HTTPStatus.FOUND, True),
        (lf('not_author_client'), HTTPStatus.NOT_FOUND, False),
        (lf('author_client'), HTTPStatus.OK, False),
    ),
)
@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete',
    )
)
def test_availability_for_comment_edit_and_delete(
        news,
        name,
        comment,
        parametrized_client,
        expected_status,
        should_redirect
):
    """
    Доступ к страницам редактирования/
    удаления комментария:
    - анонимный пользователь: редирект на страницу логина (302 Found);
    - авторизованный не автор: 404 Not Found
    (нет доступа к чужому комментарию);
    - автор комментария: 200 OK.
    """
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
    if should_redirect:
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={url}'
        assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete',
    )
)
def test_not_author_edit_delete_comment_returns_404(
        not_author_client,
        name,
        comment
):
    """
    Не автор комментария получает 404 при открытии
    edit/delete чужого комментария.
    """
    url = reverse(name, args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
