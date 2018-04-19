# -*- coding: utf-8 -*-

EmailError = 1


class MyProjectError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
