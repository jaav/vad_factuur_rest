from bottle import HTTPError, run, route,default_app,debug
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

app = default_app()
debug(True)

def main():
    run(host='localhost', port=8080)

if __name__=='__main__':
    sys.exit(main())
