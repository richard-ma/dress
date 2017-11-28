#!/usr/bin/env python

# pip install godaddypy

from godaddypy import Client, Account

myAccount = Account(
        api_key='Your production api key',
        api_secret='Your production api secret')
client = Client(myAccount)
print(client.get_domains())
