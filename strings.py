#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
https://gist.github.com/VadimPushtaev/e17f29baa5359547c41c9ab9b7da0726
Написать скрипт, который выводит все строки,
лексикографически и по длине, находящиеся между двумя заданными,
и состоящие только из строчных латинских букв.
Оцениваться будет не только алгоритмическая верность,
но и архитетура всего решения.

./strings --from a --to ab

a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z
aa
ab
"""


from getopt import getopt
from sys import argv


class MyString(object):

    def __init__(self, value):

        for i in set(value):
            if ord(i) not in range(ord('a'), ord('z') + 1):
                raise ValueError

        self._value = [ord(i) for i in value]
        self._len = len(self._value)

    def __iadd__(self, other):

        for _ in range(other):

            i = len(self._value) - 1
            while i >= 0:
                if self._value[i] == ord('z'):
                    self._value[i] = ord('a')
                else:
                    self._value[i] += 1
                    break
                i -= 1
            else:
                self._value = [ord('a')] + self._value
                self._len += 1

        return self

    def __len__(self):
        return self._len

    def __le__(self, other):

        if self._len > len(other):
            return False
        if self._len < len(other):
            return True

        for num, i in enumerate(self._value):
            if i < other[num]:
                return True
            if i > other[num]:
                return False

        return True

    def __str__(self):
        return ''.join([chr(i) for i in self._value])

    def __getitem__(self, item):
        return self._value[item]


def main(_from, _to):
    while _from <= _to:
        print(_from)
        _from += 1


def usage():

    print("usage: {script} --from <string> --to <string>\n\
<string>: only lowercase Latin letters".format(script=argv[0]))
    exit(2)


if __name__ == "__main__":
    try:
        opts, args = getopt(argv[1:], "h", ["help", "from=", "to="])
    except getopt.GetoptError as err:
        usage()

    _from, _to = None, None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--from':
            try:
                _from = MyString(arg)
            except ValueError:
                usage()
        elif opt == '--to':
            try:
                _to = MyString(arg)
            except ValueError:
                usage()
        else:
            usage()

    if not _from or not _to:
        usage()

    main(_from, _to)
