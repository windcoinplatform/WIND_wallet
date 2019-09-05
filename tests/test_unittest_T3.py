import unittest

import T3


class BasicTestsT3(unittest.TestCase):

    ###############
    #### tests ####
    ###############

    def test_t3_logger(self):
        self.assertNotEqual(T3.logger, None)

    def test_t3_url_ok_false(self):
        self.assertNotEqual(T3.url_ok('127.0.0.1', 4200), True)
        self.assertEqual(T3.url_ok('127.0.0.1', 4200), False)

    def test_t3_create_webview(self):
        webview = T3.create_webview()
        self.assertNotEqual(webview, None)
        self.assertEqual(webview.confirm_close, True)
        self.assertEqual(webview.text_select, True)
        self.assertIn("T3", webview.title)
