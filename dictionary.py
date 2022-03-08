from flask import Flask, render_template, url_for, request, redirect, session, flash
from app import app


class Localization:

    dictionary_eng = {
        'menu_artcatering': 'Art Catering',
        'menu_menus': 'Menus',
        'menu_create': 'Create',
        'menu_calendar': 'Calendar',
        'menu_signup': 'Sing up',
        'menu_contact': 'Contact',
        'menu_aboutus': 'About us',
        'menu_admin': 'Admin',
        'menu_logout': 'Logout',

    }

    dictionary_fi = {
        'menu_artcatering': 'Art Catering',
        'menu_menus': 'Menus',
        'menu_create': 'Luoda',
        'menu_calendar': 'Kalenteri',
        'menu_signup': 'Kirjaudu',
        'menu_contact': 'Ota yhteyttä',
        'menu_aboutus': 'Meistä',
        'menu_admin': 'Admin',
        'menu_logout': 'Ulos',

    }

    dictionary_ru = {
        'menu_artcatering': 'Art Кейтеринг',
        'menu_menus': 'Меню',
        'menu_create': 'Создать',
        'menu_calendar': 'Календарь',
        'menu_signup': 'Войти',
        'menu_contact': 'Контакты',
        'menu_aboutus': 'О нас',
        'menu_admin': 'Админ',
        'menu_logout': 'Выйти',

    }

    dict = {'EN': dictionary_eng, 'FI': dictionary_fi, 'RU': dictionary_ru}

    if __name__ == '__main__':
        app.run()