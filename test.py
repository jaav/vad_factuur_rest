from webtest import TestApp
import server
import json

ap = TestApp(server.app)

def test_hello_world():
    res = ap.get('/hello')
    assert res.status == '200 OK'

def add_user():
    user_info = dict(name='kamal',username='kittugadu',password='kittu',role=1)
    res = ap.put('/user', json.dumps(user_info))
    assert res.status == '200 OK'
    print res.body

def get_users():
     res = ap.get('/users')
     assertResponseOk(res)
     a = json.loads(res.body)
     assertNotNone(a[0],'name')
     assertNotNone(a[0],'role')
     assertNotNone(a[0],'username')
     assertNone(a[0],'password')
     user_id = a[0].get('id')
     res = ap.get('/user/%s' %user_id)
     assertResponseOk(res)


def assertResponseOk(res):
    assert res.status == '200 OK'

def assertNotNone(a,b):
    assert a.get(b) != None

def assertNone(a,b):
    assert a.get(b) == None
test_hello_world()
get_users()
