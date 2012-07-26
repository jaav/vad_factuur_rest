from bottle import HTTPError, run, route,default_app,debug,get
import model
import commands
import sys
#from model import Entity

#@route('/get/:name')
#def show(name,db):
#    entity = db.query(Entity).filter_by(name=name).first()
#    if entity:
#        return {'id': entity.id, 'name': entity.name}
#    return HTTPError(404, "Entity not found")

@route('/hello')
def hello():
    return "hello, world"

@get('/login')
def login():
  return '''
  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
          "http://www.w3.org/TR/html4/loose.dtd">
  <html>
  <head>
    <title></title>
    <style type="text/css">
      .mybutton{
        font-size: 2em;
        margin: 1em;
        padding: 0.5em;
      }
    </style>
  </head>
  <body>
  <form action="login" method="POST">
    <input type="hidden" name="username" value="admin" />
    <input type="hidden" name="password" value="admin" />
    <input type="submit" value="Do login" class="mybutton" />
  </form>
  </body>
  </html>
  '''

app = default_app()
debug(True)

def main():
    run(host='localhost', port=8070)

if __name__=='__main__':
    sys.exit(main())
