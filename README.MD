# Медицинский справочник первой помощи

![Screenshot](screenshot.png) <!-- Добавьте позже скриншот -->

## Функционал
- База экстренных медицинских состояний
- Пошаговая оценка состояния пациента
- Таймер СЛР с визуальным руководством
- Система тегирования

## Технологии
- Python 3.13
- Django 5.2
- Bootstrap 5
- PostgreSQL (готовность к продакшену)

## Установка
```bash
git clone https://github.com/ваш-логин/first_aid.git
cd first_aid
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver