# -*- coding: utf-8 -*-

"""«E-mail domains» + тесты
Создать утилиту командной строки, которая обрабатывает данные способом,
описанным ниже, и возвращает результат в STDOUT.
ВХОДНЫЕ ДАННЫЕ:
В командной строке указывается имя текстового файла.
Текстовый файл с email-адресами (разделитель — перевод строки). Пример:
info@mail.ru
support@vk.com
ddd@rambler.ru
roxette@mail.ru
sdfsdf@@@@@rdfdf
example@localhost
иван@иванов.рф
ivan@xn--c1ad6a.xn--p1ai

СУТЬ ОБРАБОТКИ:
Группировка адресов по имени домена, подсчёт email-адресов для каждого домена.

ВЫХОДНЫЕ ДАННЫЕ:
Имена доменов и количество адресов в каждом домене.
Сортировка по количеству адресов в домене, по убыванию.
Отдельной строкой — количество невалидных адресов. Пример:
mail.ru    2
vk.com    1
rambler.ru    1
INVALID    1

Созданная программа, должна быть максимально покрыта автоматическими тестами
(юнит тесты и т. п.), валидирующими все аспекты функционирования программы и
покрывающими максимальное количество кода программы.
Несмотря на игрушечный пример оценивается качество кода, его форматирование
(пробелы, отступы, пустые строки, выделение смысловых блоков и т.п.),
модульность, соответствие «лучшим практикам» Python-программирования и,
главное, способности писать автотесты.
Присылаемый код должен проходить проверку flake8
"""

from sys import argv
from os.path import isfile
from string import ascii_lowercase, digits


def check_email(email):
    try:
        login, domain = email.lower().split('@')
    except ValueError:
        """Не разрешаем использовать несколько @ в email"""
        return False

    if login.startswith('.') or login.endswith('.'):
        """Логин не должен начинаться или заканчиваться точкой"""
        return False

    if '..' in login:
        """Две и более точек подряд недопустимы"""
        return False

    for i in login:
        if i not in ascii_lowercase + digits + '.+_-':
            """Допустимые символы логина"""
            return False

    if '.' not in domain or '---' in domain:
        """Домен должен разделяться точкой, более двух тире быть не должно"""
        return False

    for i in domain:
        if i not in ascii_lowercase + digits + '.-':
            """локальные адреса откидываем как ошибочные"""
            return False

    if len([i for i in domain if i not in digits + '.-']) < 3:
        """Длина должна быть более 3 (хотя бы a.ru)"""
        return False

    return True


def main(f_name):

    res = dict()
    res['INVALID'] = set()

    with open(f_name) as f:
        for line in f.readlines():
            if not check_email(line[:-1]):
                res['INVALID'].add(line[:-1])
                continue

            login, domain = line[:-1].split('@')
            if domain not in res:
                res[domain] = set()
            res[domain].add(login)

    return res


if __name__ == "__main__":

    if len(argv) == 1 or not isfile(argv[1]):
        print('usage: {} <file path>'.format(argv[0]))
        exit(2)

    result = main(argv[1])
    _invalid = result.pop('INVALID')

    for i in sorted(result, key=lambda x: len(result[x]), reverse=True):
        print(i, len(result[i]))

    print('INVALID', len(_invalid))
