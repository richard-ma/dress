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
        # fix #1 bash safety characters without escaping
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ,._+:@%/-"
        return "".join(random.sample(s, password_len))
