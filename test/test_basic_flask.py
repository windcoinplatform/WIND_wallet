import unittest
from TurtleNetwork import app


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

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### test ####
    ###############

    def test_main_login_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log in', response.data)

    def test_login_with_seed(self):
        response = self.login('a', '',)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leasing', response.data)


if __name__ == "__main__":
    unittest.main()
