from flask import (
    Flask, request, render_template, redirect,
    url_for, flash
)

import os
from dotenv import load_dotenv
import requests

from .db import (
    get_url_by_name, add_url_into_db, get_url_by_id,
    add_url_check, get_checks_by_url_id, get_all_urls
)

from .url import validator, normalizer
from .html import parse_page

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.get('/')
def get_index():
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    url = request.form.get('url')
    error = validator(url)
    if error:
        flash(error, 'alert-danger')
        return render_template('index.html'), 422
    url = normalizer(url)
    data = get_url_by_name(url)
    if data:
        id = data.id
        flash('Страница уже существует', 'alert-info')
    else:
        id = add_url_into_db(url)
        flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_url', id=id))


@app.get('/urls')
def get_urls():
    urls = get_all_urls()
    return render_template('urls.html', items=urls)


@app.get('/urls/<int:id>')
def get_url(id):
    url = get_url_by_id(id)
    if url is None:
        return render_template('404.html'), 404
    checks = get_checks_by_url_id(id)
    return render_template(
        'url_info.html',
        url=url,
        checks=checks
    )


@app.post('/url/<int:id>/checks')
def url_checks(id):
    url = get_url_by_id(id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('get_url', id=id))
    check_data = parse_page(response.text)
    check_data['url_id'] = id
    check_data['status_code'] = response.status_code
    add_url_check(check_data)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('get_url', id=id))


if __name__ == '__main__':
    app.run(debug=True)
