import unittest

from TurtleNetwork import app, get_free_port
import T3


class BasicTests(unittest.TestCase):

    ########################
    #### helper methods ####
    ########################

    def login(self, seed, pk):
        return self.app.post(
            '/login',
            data=dict(seed=seed, pk=pk),
            follow_redirects=True
        )

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each tests
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each tests
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_get_free_port(self):
        port = get_free_port()
        self.assertGreater(port, 0)

    def test_login(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log in', response.data)
        self.assertIn(b'Seed', response.data)
        self.assertIn(b'Private', response.data)

    def test_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log in', response.data)
        self.assertIn(b'Seed', response.data)
        self.assertIn(b'Private', response.data)

    def test_valid_user_seed(self):
        response = self.login('a', '', )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leasing', response.data)
        self.assertIn(b'Portfolio', response.data)
        self.assertIn(b'Gateways', response.data)
        self.assertIn(b'Logout', response.data)

    def test_valid_user_pk(self):
        response = self.login('', '5LQ9aPY7St9Aw2igohPcesvWzBNkiN9BRn6UXW14nqvn')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leasing', response.data)
        self.assertIn(b'Portfolio', response.data)
        self.assertIn(b'Gateways', response.data)
        self.assertIn(b'Logout', response.data)
