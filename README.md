# Проект Yatube

## Описание
Yatube – социальная сеть для публикации дневников.
Социальная сеть с возможностью публикования постов, объединения их в группы. Публикации можно обсуждать с другими участниками сети,
подписываться на любимых авторов.
Регистрация пользователей реализована с верификацией данных, сменой и восстановлением пароля через электронную почту.

## Техническое описание
* Технология - Django
* База данных - SQLite

## Стек технологий
Python 3, Django 3.1+, pytest, Bootstrap 4.3

## Установка
Создайте виртуальное окружение:
```bash
python3 -m venv venv
```
Активируйте его:
```bash
source venv/bin/activate
```
Используйте [pip](https://pip.pypa.io/en/stable/), чтобы установить зависимости:
```bash
pip install -r requirements.txt
```
Не забудьте применить все миграции:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
Создайте суперпользователя для входа в админку:
```bash
python manage.py createsuperuser
```
И запускайте сервер:
```bash
python manage.py runserver
```

## Доступ к админке
Чтобы открыть админку, запустите сервер и перейдите по ссылке:
```
http://127.0.0.1:8000/admin/
```
