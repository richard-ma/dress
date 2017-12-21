class Generator(object):
    def __init__(self):
        pass

    @classmethod
    def generat():
        pass

import random

class PasswordGenerator(Generator):
    @classmethod
    def generat(cls, password_len):
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
        return "".join(random.sample(s, password_len))
