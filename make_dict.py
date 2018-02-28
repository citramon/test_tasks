#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Есть два списка разной длины. В первом содержатся ключи, а во втором значения.
Напишите функцию, которая создаёт из этих ключей и значений словарь.
Если ключу не хватило значения, в словаре должно быть значение None.
Значения, которым не хватило ключей, нужно игнорировать.
"""


def MakeDict(keys, values):
	result = {}
	i = 0
	for key in keys:
		if len(values) > i:
			result[key] = values[i]
		else:
			result[key] = None
		i += 1
	return result


if __name__ == '__main__':
	keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
	values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	print MakeDict(keys, values)
