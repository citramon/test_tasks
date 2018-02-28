# -*- coding: utf-8 -*-

"""Тесты для задания «E-mail domains» + тесты"""

import unittest
from emaildomains import check_email, main
from os import remove


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        self.name_test_file = 'test_list.txt'
        self.name_null_file = 'test_null.txt'

        self.ok_emails = (
            'stanislav+spam@yandex.ru',
            'info@mail.ru',
            'support@vk.com',
            'ddd@rambler.ru',
            'rexette@mail.ru',
            'ivan@xn--c1ad6a.xn--p1ai')
        self.err_emails = (
            'stas@a.u',
            'spammer@8.8.8.8',
            'stas@xn--c1ad6a.xn---p1ai',
            '.@a.ru',
            '.yaa@mail.ru',
            'stas.@yandex.ru'
            'example@localhost',
            'sdfsdf@@@@rdgfdf',
            'иван@иванов.рф',)

        with open(self.name_test_file, 'w') as f:
            for email in self.ok_emails + self.err_emails:
                f.write('%s\n' % email)

        with open(self.name_null_file, 'w') as f:
            f.write('\n')

    def tearDown(self):
        remove(self.name_test_file)
        remove(self.name_null_file)

    def test_check_email(self):

        for i in self.ok_emails:
            self.assertTrue(check_email(i), '%s is False' % i)

        for i in self.err_emails:
            self.assertFalse(check_email(i), '%s is True' % i)

    def test_main(self):
        res = main(self.name_test_file)
        self.assertEqual(len(res['INVALID']), len(self.err_emails))

    def test_null_file(self):
        res = main(self.name_null_file)
        self.assertEqual(len(res['INVALID']), 1)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
