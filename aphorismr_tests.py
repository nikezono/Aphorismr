# -*- coding: utf-8 -*-
"""
    Flaskr Tests
    ~~~~~~~~~~~~

    Tests the Flaskr application.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

"""盛大にパクったテストモジュール"""


import os
import aphorismr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, aphorismr.app.config['DATABASE'] = tempfile.mkstemp()
        aphorismr.app.config['TESTING'] = True
        self.app = aphorismr.app.test_client()
        aphorismr.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(aphorismr.app.config['DATABASE'])

    # testing functions

    def test_empty_db(self):
        """Start with a blank database."""
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def test_messages(self):
        """Test that messages work"""
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
