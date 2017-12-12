#!/usr/bin/env python

import os
import unittest

from dress.app import create_app, db

class HostTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['APP_CONFIG'] = 'dress.config.TestingConfig'
        db.create_all()
        self.app = create_app()

    def test_home_redirect_to_host(self):
        tester = self.app.test_client(self)
        rv = tester.get(
                '/',
                follow_redirects=True
        )
        self.assertTrue(b'Host' in rv.data)

if __name__ == '__main__':
    unittest.main()
