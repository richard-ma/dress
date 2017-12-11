#!/usr/bin/env python

from app import app, db
import unittest

class HostTestCase(unittest.TestCase):
    def test_home_redirect_to_host(self):
        tester = app.test_client(self)
        rv = tester.get(
                '/',
                follow_redirects=True
        )
        self.assertTrue(b'Host' in rv.data)

if __name__ == '__main__':
    unittest.main()
