from urllib.parse import urlparse
import validators


MAX_URL_LENGHT = 255


def validator(url):
    error = None
    if not url:
        error = 'URL обязателен'
    elif len(url) > MAX_URL_LENGHT:
        error = f'URL превышает {MAX_URL_LENGHT} символов'
    elif not validators.url(url):
        error = 'Некорректный URL'
    return error


def normalizer(url):
    data = urlparse(url)
    return data.scheme + '://' + data.netloc
