from webtest import TestApp
import server
from unittest import TestCase

__author__ = 'jefw'

ap = TestApp(server.app)


class TestVadFactuur(TestCase):
  def test_setUser(self):
    res = ap.get('/hello')
    self.assertEqual(res.status, '200 OK', 'Hello World is A OK')