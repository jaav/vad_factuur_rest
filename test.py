from webtest import TestApp
import server

def test_hello_world():
    ap = TestApp(server.app)
    res = ap.get('/hello')
    assert res.status == '200 OK'

test_hello_world()
