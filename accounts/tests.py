from django.test import TestCase

class URLTests(TestCase):
    def test_testhomepage(self):
        response = self.client.get('/log-in')
        self.assertEqual(response.status_code, 200)

