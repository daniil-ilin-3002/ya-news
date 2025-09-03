from django.urls import reverse

from news.forms import CommentForm

from yanews import settings


def test_news_count(author_client, news_10):
    """
    Проверяет, что на главной странице
    отображается правильное количество новостей
    """
    url = reverse('news:home')
    response = author_client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(author_client, news_10):
    """
    Проверяет, что новости на главной странице
    отсортированы по дате в порядке убывания.
    """
    url = reverse('news:home')
    response = author_client.get(url)
    object_list = response.context['object_list']
    all_dates = [news_10.date for news_10 in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_order(author_client, news, comments_10):
    """
    Проверяет, что комментарии к новости отсортированы
    по времени создания в порядке возрастания.
    """
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comments_10.created for comments_10 in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(author_client, news):
    """
    Проверяет, что у анонимного клиента на
    странице детали новости нет формы для комментариев.
    """
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context


def test_authorized_client_has_form(not_author_client, news):
    """
    Проверяет, что у авторизованного клиента на странице
    детали новости есть форма для комментариев
    и что эта форма является экземпляром CommentForm.
    """
    url = reverse('news:detail', args=(news.id,))
    response = not_author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
