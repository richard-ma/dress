import random


def generator_password_helper(password_len):
    # fix #1 bash safety characters without escaping
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ,._+:@%-"
    return "".join(random.sample(s, password_len))
