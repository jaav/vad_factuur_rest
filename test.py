from webtest import TestApp
import server
import json

def test_hello_world():
    ap = TestApp(server.app)
    res = ap.get('/hello')
    assert res.status == '200 OK'

def add_user():
    ap = TestApp(server.app)
    user_info = dict(name='krishna',username='kittugadu',password='kittu',role=1)
    res = ap.put('/user', json.dumps(user_info))
    assert res.status == '200 OK'

test_hello_world()
add_user()
