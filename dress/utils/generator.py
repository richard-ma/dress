class Generator(object):
    def __init__(self):
        pass

    @classmethod
    def generate():
        pass

import random

class PasswordGenerator(Generator):
    @classmethod
    def generate(cls, password_len):
        # fix #1 bash safety characters without escaping
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ,._+:@%-"
        return "".join(random.sample(s, password_len))

from dress.data.models import Setting

class OrderStartNumberGenerator(Generator):
    @classmethod
    def reset(cls, order_start_number=None):
        order_start_number_setting = Setting.query.filter_by(name=Setting.ORDER_START_NUMBER_NAME).first()
        order_start_number_setting.update(value=str(order_start_number or Setting.ORDER_START_NUMBER_VALUE))

    @classmethod
    def generate(cls, interval=10000):
        order_start_number_setting = Setting.query.filter_by(name=Setting.ORDER_START_NUMBER_NAME).first()
        new_order_start_number = int(order_start_number_setting.value) + interval
        order_start_number_setting.update(value=str(new_order_start_number))

        return new_order_start_number
