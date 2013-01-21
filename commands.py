from datetime import datetime, date
import json
from datetime import datetime
from bottle import get, post, put, delete, request, abort, response
import hashlib
from sqlalchemy.exc import ProgrammingError
import cleaner
import model
import settings
from sqlalchemy import or_, and_, desc
from model import User, Unit, ArticleType, Supplier, Sector, Person, Customer, Address, Article, Stock, InvoiceLine, Invoice, Post

@put('/user')
@post('/user')
def setUser(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    user = User(name=json_input.get("name"), username=json_input.get("username"), password=json_input.get("password"), role=json_input.get("role"))
    db.add(user)

@post('/user/:id')
def updateUser(id,db):
    isValidUser(db,request)
    try:
        user = db.query(User).filter_by(id=id).first()
        json_input = get_input_json(request)
        if json_input.get("name"): user.name = json_input.get("name")
        if json_input.get("username"): user.username = json_input.get("username")
        if json_input.get("role"): user.role = json_input.get("role")
        if json_input.get("password"): user.addHash(json_input.get("password"))
        db.merge(user)
    except:
        resource_not_found( 'User not found')

@get('/user/:id')
def getUser(id,db):
    isValidUser(db,request)
    try:
        user = db.query(User).filter_by(id=id).first()
        return user_json()
    except:
        resource_not_found( 'User')

@get('/users')
def getUsers(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    users = getDbObjects(db, User)
    json_response['data'].append([ user_json(user) for user in users])
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, User)
    
    return json.dumps(json_response,ensure_ascii=False)

def user_json(user):
  return {'id': user.id,
               'name': user.name,
               'username': user.username,
               'role': user.role}

@delete('/user/:id')
def deleteUser(id, db):
    isValidUser(db,request)
    try:
        user = db.query(User).filter_by(id=id).first()
        soft_delete(db, user)
    except:
        resource_not_found( 'User')

@post('/login')
def login(db):
   username = request.params.get('username') 
   password = request.params.get('password')
   user = check(db,username,password)
   if user:
       #response.set_cookie('username',username,settings.cookie_secret)
       #response.set_cookie('password',hashlib.md5(password.encode('utf-8')).hexdigest(),settings.cookie_secret)
       return str(user.id)+'___'+hashlib.md5(password.encode('utf-8')).hexdigest()
   else:
       forbidden()

def check(db,username,password):
    if not username or not password:
        return None
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    try:

        user = db.query(User).filter(and_ (User.username==username,
                User.password_hash==password)).first()
        if user:
            return user
        else:
            return None
    except:
        return None

def isValidUser(db,request):
    return True
#    print request.get_cookie("username")
#    print request.get_cookie("password")
#    print request.get_cookie("username", "unknown", settings.cookie_secret)
#    print request.get_cookie("password", "unknown", settings.cookie_secret)
#    username = request.get_cookie("username", "unknown", settings.cookie_secret)
#    password = request.get_cookie("password", "unknown", settings.cookie_secret)
#    if not username or not password:
#        forbidden()
#    try:
#        user = db.query(User).filter(or_ (User.username==username,User.password_hash==password)).first()
#        print user
#        if user:
#            return True
#        else:
#            forbidden()
#    except:
#        forbidden()

#@get('/shouldRefresh')
#def shouldRefresh(db):
#  username = request.params.get('username')
#  user = db.query(User).filter_by(username=username).first()
#  update_status = db.query(model.UpdateStatus).filter_by(user=user.id).first()
#  return {'articles':update_status.articles, 'customers':update_status.customers}
#
#@get('/resetStatuses')
#def resetAllStatuses(db):
#   statuses = db.query(model.UpdateStatus)
#   for status in statuses:
#     db.delete(status)
#   users = db.query(User)
#   for user in users:
#     status = model.UpdateStatus(user, True, True)
#     db.add(status)



@put('/post')
@post('/post')
def setPost(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    post = Post(name=json_input.get("name"), bottom=json_input.get("bottom"), top=json_input.get("top"), price=json_input.get("price"))
    db.add(post)

@post('/post/:id')
def updatePost(id,db):
    isValidUser(db,request)
    try:
        post = db.query(Post).filter_by(id=id).first()
        json_input = get_input_json(request)
        if json_input.get("name"): post.name = json_input.get("name")
        if json_input.get("bottom") is not None: post.bottom_weight = json_input.get("bottom")
        if json_input.get("top") is not None: post.top_weight = json_input.get("top")
        if json_input.get("price") is not None: post.price = json_input.get("price")
        db.merge(post)
    except:
        resource_not_found( "Post not found")

@get('/post/:id')
def getPost(id,db):
    isValidUser(db,request)
    try:
        post = db.query(Post).filter_by(id=id).first()
        return {'id': post.id, 'name': post.name,
                'bottom': post.bottom_weight, 'top': post.top_weight, 'price': post.price}
    except:
        resource_not_found( "Post")

@get('/posts')
def getPosts(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    posts = getDbObjects(db, Post)
    json_response['data'] = [ {'id': post.id, 'name': post.name,
                               'bottom': post.bottom_weight, 'top': post.top_weight, 'price': post.price} for post in posts]
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Post)
    return json.dumps(json_response,ensure_ascii=False)

@delete('/post/:id')
def deletePost(id,db):
    isValidUser(db,request)
    try:
        post = db.query(Post).filter_by(id=id).first()
        soft_delete(db, post)
    except:
        resource_not_found("Post")





@put('/unit')
@post('/unit')
def setUnit(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    unit = Unit(name=json_input.get("name"))
    db.add(unit)

@post('/unit/:id')
def updateUnit(id,db):
    isValidUser(db,request)
    try:
        unit = db.query(Unit).filter_by(id=id).first()
        json_input = get_input_json(request)
        if json_input.get("name"): unit.name = json_input.get("name")
        db.merge(unit)
    except:
        resource_not_found( "Unit not found")

@get('/unit/:id')
def getUnit(id,db):
    isValidUser(db,request)
    try:
        unit = db.query(Unit).filter_by(id=id).first()
        return {'id': unit.id,
                'name': unit.name}
    except:
        resource_not_found( "Unit")

@get('/units')
def getUnits(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    units = getDbObjects(db, Unit)
    json_response['data'] = [ {'id': unit.id,
                        'name': unit.name} for unit in units]
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Unit)
    return json.dumps(json_response,ensure_ascii=False)

@delete('/unit/:id')
def deleteUnit(id,db):
    isValidUser(db,request)
    try:
        unit = db.query(Unit).filter_by(id=id).first()
        soft_delete(db, unit)
    except:
        resource_not_found("Unit")

@put('/articleType')
@post('/articleType')
def addArticleType(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    articleType = ArticleType(name=json_input.get("name"))
    db.add(articleType)

@post('/articleType/:id')
def updateArticleType(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        articleType = db.query(ArticleType).filter_by(id=id).first()
        if json_input.get("name"): articleType.name = json_input.get("name")
        db.merge(articleType)
    except:
        resource_not_found("ArticleType")

@get('/articleType/:id')
def getArticleType(id,db):
    isValidUser(db,request)
    try:
        articleType = db.query(ArticleType).filter_by(id=id).first()
        return {'id': articleType.id,
                'name': articleType.name}
    except:
        resource_not_found("ArticleType")

@get('/articleTypes')
def getArticleTypes(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    articleTypes = getDbObjects(db, ArticleType)
    json_response['data'] = [ {'id': a.id,
                        'name': a.name} for a in articleTypes]
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, ArticleType)
    return json.dumps(json_response,ensure_ascii=False)

@delete('/articleType/:id')
def deleteArticleType(id,db):
    isValidUser(db,request)
    try:
      articleType = db.query(ArticleType).filter_by(id=id).first()
      soft_delete(db, articleType)
#        db.delete(articleType)
    except:
        resource_not_found("ArticleType")

@put('/supplier')
@post('/supplier')
def addSupplier(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    supplier = Supplier(name=json_input.get("name"))
    db.add(supplier)

@post('/supplier/:id')
def updateSupplier(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        supplier = db.query(Supplier).filter_by(id=id).first()
        if json_input.get("name"): supplier.name = json_input.get("name")
        db.merge(supplier)
    except:
        resource_not_found("Supplier")

@get('/supplier/:id')
def getSupplier(id,db):
    isValidUser(db,request)
    try:
        supplier = db.query(Supplier).filter_by(id=id).first()
        return {'id': supplier.id,
                'name': supplier.name}
    except:
        resource_not_found("Supplier")

@get('/suppliers')
def getSuppliers(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    suppliers = getDbObjects(db, Supplier)
    json_response['data'] = [
            {'id': s.id,
                'name': s.name} for s in suppliers]
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Supplier)
    return json.dumps(json_response,ensure_ascii=False)

@delete('/supplier/:id')
def deleteSupplier(id,db):
    isValidUser(db,request)
    try:
        supplier = db.query(Supplier).filter_by(id=id).first()
        soft_delete(db, supplier)
    except:
        resource_not_found("Supplier")

@put('/sector')
@post('/sector')
def addSector(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    sector = Sector(json_input.get('name'),json_input.get('parent'))
    db.add(sector) 

@post('/sector/:id')
def updateSector(id, db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        sector = db.query(Sector).filter_by(id=id).first()
        if json_input.get('name'): sector.name = json_input.get('name')
        if json_input.get('parent') is not None: sector.parent = json_input.get('parent')
        db.merge(sector)
    except:
        resource_not_found("Sector")

@get('/sector/:id')
def getSector(id, db):
    isValidUser(db,request)
    try:
        sector = db.query(Sector).filter_by(id=id).first()
        if sector.parent:
            return {'id': sector.id,
                    'name': sector.name,
                    'parent': sector.parent}
        else:
            return {'id':sector.id,
                    'name': sector.name}
    except:
        resource_not_found("Sector")

@get('/sectors')
def getSectors(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    sectors = getDbObjects(db, Sector)
    json_response['data'] = [
            {'id': s.id,
                'name': s.name,
                'parent': s.parent} for s in sectors]
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Sector)
    return json.dumps(json_response, ensure_ascii=False)

@get('/subSectors/:parent_id')
def getSectors(parent_id, db):
    isValidUser(db,request)
    orderOn = request.params.get('orderOn')
    if orderOn == None:
      sectors = db.query(Sector).filter(and_(Sector.active==1,Sector.parent==parent_id)).order_by('name')
    else:
      sectors = db.query(Sector).filter(and_(Sector.active==1,Sector.parent==parent_id)).order_by(orderOn)
    json_response = [
            {'id': s.id,
                'name': s.name,
                'parent': s.parent} for s in sectors]
    return json.dumps(json_response, ensure_ascii=False)

@delete('/sector/:id')
def deleteSector(id, db):
    isValidUser(db,request)
    try:
        sector = db.query(Sector).filter_by(id=id).first()
        soft_delete(db, sector)
    except:
        resource_not_found("Sector")

@put('/person')
@post('/person')
def addPerson(db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        person  = Person(title=json_input.get('title'),
                name=json_input.get('name'),email=json_input.get('email'),
                phone=json_input.get('phone'),customer=json_input.get('customer'))
        db.add(person)
    except:
        resource_not_found("Person")

@post('/person/:id')
def updatePerson(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        person = db.query(Person).filter_by(id=id).first()
        if json_input.get('name'): person.name = json_input.get('name')
        if json_input.get('email'): person.email = json_input.get('email')
        if json_input.get('phone'): person.phone = json_input.get('phone')
        if json_input.get('customer'): person.customer = json_input.get('customer')
        if json_input.get('title'): person.title = json_input.get('title')
        db.merge(person)
    except:
        resource_not_found("Person")

@get('/person/:id')
def getPerson(id,db):
    isValidUser(db,request)
    try:
        person = db.query(Person).filter_by(id=id).first()
        return person_json(person)
    except:
        resource_not_found("Person")

#@get('/personByCustomer/:id')
#def getPersonByCustomer(id,db):
#    isValidUser(db,request)
#    try:
#        orderOn = request.params.get('orderOn')
#        if orderOn == None:
#          person = db.query(Person).filter(and_(Person.active==1, Person.customer==id)).order_by('id').first()
#        else:
#          person = db.query(Person).filter(and_(Person.active==1, Person.customer==id)).order_by(orderOn).first()
#        return { 'id': person.id,
#                'title': person.title,
#                'name': person.name,
#                'email': person.email,
#                'phone': person.phone,
#                'customer': person.customer }
#    except:
#        resource_not_found("Person")

@delete('/person/:id')
def deletePerson(id,db):
    isValidUser(db,request)
    try:
        person = db.query(Person).filter_by(id=id).first()
        soft_delete(db, person)
    except:
        resource_not_found("Person")

@get('/persons')
def getPersons(db):
    isValidUser(db,request)
    full_info = getFullInfo()
    json_response = getJsonContainer()
    persons = getDbObjects(db, Person)
    count = request.params.get('count')
    if full_info:
      for person in persons:
          persDict = person_json(person)
          json_response['data'].append(persDict)
      if count is not None:
        json_response['info']['count']=getCount(db, Person)
      return json.dumps(json_response,ensure_ascii=False)
    else:
      json_response['data'] = [ { 'id': person.id } for person in persons]
      if count is not None:
        json_response['info']['count']=getCount(db, Person)
      return json.dumps(json_response,ensure_ascii=False)

def person_json(person):
  return { 'id': person.id,
                  'title': person.title,
                  'name': person.name,
                  'email': person.email,
                  'phone': person.phone,
                  'customer': person.customer }

@put('/customer')
@post('/customer')
def addCustomer(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    customer = Customer(name=json_input.get('name'),vat=json_input.get('vat'),
            iban=json_input.get('iban'),remark=json_input.get('remark'),
            sector=json_input.get('sector'),subsector=json_input.get('subsector'))
    db.add(customer)

@post('/customer/:id')
def updateCustomer(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        customer = db.query(Customer).filter_by(id=id).first()
        if json_input.get('name'): customer.name = json_input.get('name')
        if json_input.get('vat'): customer.vat = json_input.get('vat')
        if json_input.get('iban'): customer.iban = json_input.get('iban')
        if json_input.get('remark'): customer.remark = json_input.get('remark')
        if json_input.get('sector') and json_input.get('sector')>=0: customer.sector = json_input.get('sector')
        elif json_input.get('sector'): customer.sector = None
        if json_input.get('subsector') and json_input.get('subsector')>=0: customer.subsector = json_input.get('subsector')
        elif json_input.get('subsector'): customer.subsector = None
        db.merge(customer)
    except:
        resource_not_found("Customer")

@get('/customer/:id')
def getCustomer(id,db):
    isValidUser(db,request)
    try:
        customer = db.query(Customer).filter_by(id=id).first()
        addresses = db.query(Address).filter_by(customer=customer.id).all()
        persons = db.query(Person).filter_by(customer=customer.id).all()
        custDict = {'id': customer.id,
                'name': customer.name,
                'vat': customer.vat,
                'iban': customer.iban,
                'remark': customer.remark,
                'sector': customer.sector,
                'subsector': customer.subsector}
        addressDictList = []
        personDictList = []
        for add in addresses:
          if add.active:
            address = {'id': add.id,
                    'customer': add.customer,
                    'address': add.street,
                    'address_type': add.address_type,
                    'zipcode': add.zipcode,
                    'city': add.city,
                    'tel': add.tel,
                    'fax': add.fax,
                    'email': add.email,
                    'att': add.att}
            addressDictList.append(address)
        for person in persons:
          if person.active:
            person =  {'id': person.id,
                    'title': person.title,
                    'name': person.name,
                    'email': person.email,
                    'phone': person.phone,
                    'customer': person.customer }
            personDictList.append(person)
        custDict['person'] = personDictList
        custDict['address'] = addressDictList
        return custDict
    except:
        resource_not_found("Customer")

@delete('/customer/:id')
def deleteCustomer(id,db):
    isValidUser(db,request)
    try:
        customer = db.query(Customer).filter_by(id=id).first()
        soft_delete(db, customer)
    except:
        resource_not_found("Customer")

@get('/allCustomers')
def getAllCustomers(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    query = '''
    SELECT customer.id AS customer_id, customer.name AS customer_name, address.city AS address_city
    FROM customer LEFT OUTER JOIN address ON customer.id = address.customer
    WHERE customer.active = 1 ORDER BY customer.name
    '''

    result = db.execute(query)
    prev_id = 0
    for row in result:
        if row.customer_id != prev_id:
          prev_id = row.customer_id
          custDict = { 'id': row.customer_id,
                       'name': row.customer_name}
          if row.address_city is not None:
            custDict['name'] = custDict['name'] + ' (' + row.address_city + ')'
          json_response['data'].append(custDict)

    return json.dumps(json_response,ensure_ascii=False)


@get('/customers')
def getCustomers(db):
    isValidUser(db,request)
    full_info = getFullInfo()
    json_response = getJsonContainer()
    count = request.params.get('count')
    if full_info:
      query = getQuery(db, Customer, None)

      fromPos = request.params.get('from')
      quantity = request.params.get('quantity')
      paging = False
      if fromPos and quantity:
        paging=True
      if paging:
        customers = query.offset(fromPos).limit(quantity)
      else:
        customers = query.all()
      for customer in customers:
          custDict = { 'id': customer.id,
                       'name': customer.name,
                       'vat': customer.vat,
                       'iban': customer.iban,
                       'remark': customer.remark,
                       'sector': customer.sector,
                       'subsector': customer.subsector }
          addressDictList = []
          personDictList = []
          for add in customer.addresses:
            if add.active:
              address = {'id': add.id,
                      'customer': add.customer,
                      'address': add.street,
                      'address_type': add.address_type,
                      'zipcode': add.zipcode,
                      'city': add.city,
                      'tel': add.tel,
                      'fax': add.fax,
                      'email': add.email,
                      'att': add.att }
              addressDictList.append(address)
          for person in customer.persons:
            if person.active:
              person =  {'id': person.id,
                      'title': person.title,
                      'name': person.name,
                      'email': person.email,
                      'phone': person.phone,
                      'customer': person.customer }
              personDictList.append(person)
          custDict['person'] = personDictList
          custDict['address'] = addressDictList
          json_response['data'].append(custDict)
      if count is not None:
        json_response['info']['count']=getCount(db, Customer)
      return json.dumps(json_response,ensure_ascii=False)
    else:
      #customers = getDbObjects(db, Customer)
      query = getQuery(db, Customer, Address)
      customers = query.all()
      for customer in customers:
          custDict = { 'id': customer.Customer.id,
                       'name': customer.Customer.name}
          if customer.Address is not None:
            custDict['name'] = custDict['name'] + ' (' + customer.Address.city + ')'
          #address = addresses[0]
            #custDict['name'] = custDict['name'] + ' (' + addresses[0].city + ')'
          json_response['data'].append(custDict)
      if count is not None:
        json_response['info']['count']=getCount(db, Customer)
      return json.dumps(json_response,ensure_ascii=False)

#@get('/customersBySector/:id')
#def getCustomersBySector(id,db):
#    isValidUser(db,request)
#    try:
#        customers = db.query(Customer).filter(or_ (Customer.sector==id,
#                Customer.subsector==id))
#        return json.dumps([{'id' : cust.id } for cust in customers],ensure_ascii=False)
#    except:
#        resource_not_found("Customers")

@put('/address')
@post('/address')
def addAddress(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    address = Address(customer=json_input.get('customer'),street=json_input.get('address'),
            address_type=json_input.get('address_type'),zipcode=json_input.get('zipcode'),
            city=json_input.get('city'),tel=json_input.get('tel'),fax=json_input.get('fax'),
            email=json_input.get('email'), att=json_input.get('att'))
    db.add(address)

@post('/address/:id')
def updateAddress(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        address = db.query(Address).filter_by(id=id).first()
        if json_input.get('customer'): address.customer = json_input.get('customer')
        if json_input.get('address_type'): address.address_type = json_input.get('address_type')
        if json_input.get('address'): address.street = json_input.get('address')
        if json_input.get('zipcode'): address.zipcode = json_input.get('zipcode')
        if json_input.get('city'): address.city = json_input.get('city')
        if json_input.get('tel'): address.tel = json_input.get('tel')
        if json_input.get('fax'): address.fax = json_input.get('fax')
        if json_input.get('email'): address.email = json_input.get('email')
        if json_input.get('att'): address.att = json_input.get('att')
        db.merge(address)
    except:
        resource_not_found("Address")

@get('/address/:id')
def getAddress(id,db):
    isValidUser(db,request)
    try:
        address = db.query(Address).filter_by(id=id).first()
        return address_json(address)
    except:
        resource_not_found('Address')

@get('/addresses')
@get('/addresss')
def getAddresses(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    addresses = getDbObjects(db, Address)
    full_info = getFullInfo()
    if full_info:
      for add in addresses:
        addDict = address_json(add)
        json_response['data'].append(addDict)
    else: json_response['data'].append({'id': a.id} for a in addresses)
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Address)
    return json.dumps(json_response,ensure_ascii=False)

@delete('/address/:id')
def deleteAddress(id,db):
    isValidUser(db,request)
    try:
        address = db.query(Address).filter_by(id=id).first()
        soft_delete(db, address)
    except:
        resource_not_found('Address')



def address_json(address):
  return {'id': address.id,
          'customer': address.customer,
          'address': address.street,
          'address_type': address.address_type,
          'zipcode': address.zipcode,
          'city': address.city,
          'tel': address.tel,
          'fax': address.fax,
          'email': address.email,
          'att': address.att}



@get('/allArticles')
def getAllArticles(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    query = '''
    SELECT id , code, name, price, free_quantity, vat
    FROM article
    WHERE active = 1 ORDER BY code
    '''

    result = db.execute(query)
    prev_id = 0
    for row in result:
        if row.id != prev_id:
          prev_id = row.id
          artDict = { 'id': row.id,
                       'name': row.name,
                       'code': row.code,
                       'freeQuantity': row.free_quantity,
                       'vat': row.vat,
                       'price': row.price
          }
          json_response['data'].append(artDict)

    return json.dumps(json_response,ensure_ascii=False)


@get('/articles')
def getArticles(db):
    isValidUser(db,request)
    #articles = getDbObjects(db, Article)
    full_info = getFullInfo()

    json_response = getJsonContainer()
    query = getQuery(db, Article, Stock)

    fromPos = request.params.get('from')
    quantity = request.params.get('quantity')
    paging = False
    if fromPos and quantity:
      paging=True
    if paging:
      articles = query.offset(fromPos).limit(quantity)
    else:
      articles = query.all()


    if full_info:
      for article in articles:
          artDict = article_json(article[0], article[1])
          json_response['data'].append(artDict)
    else:
      for article in articles:
          artDict = { 'id': article[0].id,'name': article[0].name}
          json_response['data'].append(artDict)
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Article)
    return json.dumps(json_response,ensure_ascii=False)

@put('/article')
@post('/article')
def addArticle(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    user_id = json_input.get('creator')
    if json_input.get("copyDate") is None: copy_date_value = ''
    else: copy_date_value = datetime.strptime(json_input.get("copyDate"),"%d/%m/%Y")
    #user_id = getUserByUsername(username, db).id
    article = Article(article_type=json_input.get('article_type'),
            code=json_input.get('code'), name=json_input.get('name'),
            description=json_input.get('description'),price=json_input.get('price'),
            free_quantity=json_input.get('freeQuantity'), copy_date=copy_date_value,
            unit=json_input.get('unit'),supplier=json_input.get('supplier'),
            weight=json_input.get('weight'), create_date=datetime.now(),
            vat=json_input.get('vat'),creator=user_id)
    db.add(article)
    db.flush();
    stock = Stock(0, article.id, True)
    db.add(stock)

@post('/article/:id')
def updateArticle(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        user_id = json_input.get('creator')
        #user_id = getUserByUsername(username, db).id
        article = db.query(Article).filter_by(id=id).first()
        if json_input.get('article_type') is not None: article.article_type=json_input.get('article_type')
        if json_input.get('code') is not None: article.code=json_input.get('code')
        if json_input.get('name') is not None: article.name=json_input.get('name')
        if json_input.get('description') is not None: article.description=json_input.get('description')
        if json_input.get('price') is not None: article.price=json_input.get('price')
        if json_input.get('freeQuantity') is not None: article.free_quantity=json_input.get('freeQuantity')
        if json_input.get('unit') is not None: article.unit=json_input.get('unit')
        if json_input.get('weight') is not None: article.weight=json_input.get('weight')
        if json_input.get('create_date') is not None: article.create_date=datetime.strptime(json_input.get('create_date'), "%d/%m/%Y")
        if json_input.get('copyDate') is not None: article.copy_date=datetime.strptime(json_input.get('copyDate'), "%d/%m/%Y")
        if json_input.get('vat') is not None: article.vat=json_input.get('vat')
        if user_id: article.creator=user_id
        if json_input.get('supplier') is not None: article.supplier=json_input.get('supplier')
        db.merge(article)
    except:
        resource_not_found("Article")


#@get('/articleBySupplier/:supplierId')
#def getArticlesBySupplier(supplierId,db):
#    isValidUser(db,request)
#    try:
#        articles = db.query(Article).filter_by(supplier=supplierId).all()
#        return json.dumps([ {'id': a.id } for a in articles ],ensure_ascii=False)
#    except:
#        resource_not_found("Article")

@get('/article/:id')
def getArticle(id,db):
    isValidUser(db,request)
    try:
        article = db.query(Article).filter_by(id=id).first()
        stock = db.query(Stock).filter_by(article=article.id).first()
        artDict = article_json(article, stock)
        if stock:
            artDict['stock'] = {'id': stock.id, 'quantity': stock.quantity}
        return artDict
    except:
        resource_not_found("Article")

@delete('/article/:id')
def deleteArticle(id,db):
    isValidUser(db,request)
    try:
        article = db.query(Article).filter_by(id=id).first()
        soft_delete(db, article)
    except:
        resource_not_found('Article')

def article_json(article, stock):
  artDict = { 'id': article.id,
     'article_type': article.article_type,
     'code': article.code,
     'name': article.name,
     'description': article.description,
     'price': article.price,
     'freeQuantity': article.free_quantity,
     'unit': article.unit,
     'weight': article.weight,
     'create_date': str(article.create_date),
     'copyDate': str(article.copy_date),
     'vat': article.vat,
     'creator': article.creator,
     'supplier': article.supplier
     }
  if stock:
      artDict['stock'] = {'id': stock.id, 'quantity': stock.quantity}
  return artDict

@put('/stock')
@post('/stock')
def addStock(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    stock = Stock(article=json_input.get('article'),quantity=json_input.get('quantity'))
    db.add(stock)

@post('/stock/:id')
def updateStock(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        stock = db.query(Stock).filter_by(id=id).first()
        if json_input.get('article'): stock.article = json_input.get('article')
        if json_input.get('quantity'): stock.quantity = json_input.get('quantity')
        db.merge(stock)
    except:
        resource_not_found("Stock")

@get('/stock/:id')
def getStock(id,db):
    isValidUser(db,request)
    try:
        stock = db.query(Stock).filter(and_(Stock.id==id, Stock.active==1)).first()
        return {'id': stock.id,
                'article': stock.article,
                'quantity': stock.quantity }
    except:
        resource_not_found("Stock")

@delete('/stock/:id')
def deleteStock(id,db):
    isValidUser(db,request)
    try:
        stock = db.query(Stock).filter_by(id=id).first()
        db.delete(stock)
    except:
        resource_not_found("Stock")

@get('/stocks')
def getStocks(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    stocks = getDbObjects(db, Stock)
    json_response['data'] = [ {'id': s.id,
        'article': s.article,
        'quantity': s.quantity} for s in stocks ]
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, Stock)
    return json.dumps(json_response,ensure_ascii=False)

@put('/invoiceLine')
@post('/invoiceLine')
def addInvoiceLine(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    invoice_line = InvoiceLine(article=json_input.get('article').get('id'),
            quantity=json_input.get('quantity'),
            unit_price=json_input.get('unit_price'),
            unit_discount=json_input.get('unit_discount'),
            invoice=json_input.get('order_id'),
            active=True,
            apply_free=json_input.get('apply_free'))
    db.add(invoice_line)
    updateInvoiceData(db, json_input.get('order_id'))
    adapt_stock(db, json_input.get('article').get('id'), json_input.get('quantity'))
    return order_line_json(db, invoice_line)

@post('/invoiceLine/:id')
def updateInvoiceLine(id,db):
    isValidUser(db,request)
    try:
      json_input = get_input_json(request)
      invoice_line = db.query(InvoiceLine).filter_by(id=id).first()
      old_article_id = invoice_line.article
      old_quantity = invoice_line.quantity
      if json_input.get('article') and json_input.get('article').get('id'):
        invoice_line.article=json_input.get('article').get('id')
        if json_input.get('quantity') is not None: invoice_line.quantity=json_input.get('quantity')
        if json_input.get('unit_discount') is not None: invoice_line.unit_discount=json_input.get('unit_discount')
        if json_input.get('invoice') is not None: invoice_line.invoice=json_input.get('invoice')
        if json_input.get('apply_free') is not None: invoice_line.apply_free=json_input.get('apply_free')
        else: invoice_line.apply_free=True
        db.merge(invoice_line)
        updateInvoiceData(db, json_input.get('order_id'))
        adapt_stock(db, old_article_id, -old_quantity)
        adapt_stock(db, json_input.get('article').get('id'), json_input.get('quantity'))
    except ProgrammingError as e:
        resource_not_found("InvoiceLine")

@get('/invoiceLine/:id')
def getInvoiceLine(id,db):
    isValidUser(db,request)
    try:
        invoice_line = db.query(InvoiceLine).filter_by(id=id).first()
        return order_line_json(invoice_line)
    except:
        resource_not_found("InvoiceLine")

#@get('/invoiceLinesByInvoice/:invoice_id')
#
# IS REPLACED BY /invoiceLines with additionalCondition set to invoice=8
#
#def getInvoiceLineByInvoice(invoice_id,db):
#    isValidUser(db,request)
#    try:
#        invoice_lines = db.query(InvoiceLine).filter(and_(InvoiceLine.invoice==invoice_id, InvoiceLine.active==1)).order_by('id')
#        return json.dumps([{'id': invoice_line.id, 'article': invoice_line.article, 'quantity': invoice_line.quantity, 'unit_price': invoice_line.unit_price, 'unit_discount': invoice_line.unit_discount} for invoice_line in invoice_lines],ensure_ascii=False)
#    except:
#        resource_not_found("InvoiceLine")

@get('/invoiceLines')
def getInvoiceLines(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    invoice_lines = getDbObjects(db, InvoiceLine)
    full_info = getFullInfo()


    if full_info:
      for invoice_line in invoice_lines:
          invDict = order_line_json(db, invoice_line)
          json_response['data'].append(invDict)
    else:
      for invoice_line in invoice_lines:
          invDict = { 'id': invoice_line.id}
          json_response['data'].append(invDict)
    count = request.params.get('count')
    if count is not None:
      json_response['info']['count']=getCount(db, InvoiceLine)
    return json.dumps(json_response,ensure_ascii=False)

@delete('/invoiceLine/:id')
def deleteInvoiceLine(id,db):
    isValidUser(db,request)
    try:
        invoice_line = db.query(InvoiceLine).filter_by(id=id).first()
        quantity = invoice_line.quantity
        article_id = invoice_line.article
        order_id = invoice_line.invoice
        db.delete(invoice_line)
        updateInvoiceData(db, order_id)
        adapt_stock(db, article_id, -quantity)
    except:
        resource_not_found("InvoiceLine")


def order_line_json(db, invoice_line):
  art_object = { 'id': invoice_line.id,
     'quantity': invoice_line.quantity,
     'unit_discount': invoice_line.unit_discount,
     'order_id': invoice_line.invoice,
     'apply_free': invoice_line.apply_free
     }
  if invoice_line.article:
    full_article = db.query(Article).filter(Article.id==invoice_line.article).order_by('id').first()
    if full_article: art_object["article"] = article_json(full_article, None)
  return art_object

def updateInvoiceData(db, order_id):
  invoice = db.query(Invoice).filter_by(id=order_id).first()
  prices = calculate_costs(db, invoice)
  invoice.shipping = prices[1]
  invoice.products = prices[0]
  invoice.total = invoice.products+invoice.shipping
  db.merge(invoice)

def calculate_costs(db, invoice):
  weight = 0
  products = 0
  for i in invoice.invoice_line:
    article = db.query(Article).filter_by(id=i.article).first()
    weight += (i.quantity*article.weight)
    if i.apply_free and article.free_quantity is not None:
      new_quantity = i.quantity - article.free_quantity
      if new_quantity < 0: new_quantity = 0
    else:
      new_quantity = i.quantity
    products += (new_quantity*article.price)
  post = db.query(Post).filter(and_(Post.bottom_weight<weight, weight<Post.top_weight)).first()
  return [products, post.price]



@put('/invoice')
@post('/invoice')
def addInvoice(db):
    isValidUser(db,request)
    json_input = get_input_json(request)
    invoice = Invoice(customer=None,
            inv_address=json_input.get("inv_address"),
            del_address=json_input.get("del_address"),
            code=json_input.get("code"),
            remark=json_input.get("remark"),
            shipping=json_input.get("shipping"),
            products=json_input.get("products"),
            total=json_input.get("total"),
            vat=json_input.get("vat"),
            creation_date=datetime.strptime(json_input.get("creation_date"),"%d/%m/%Y"),
            delivery_date=datetime.strptime(json_input.get("delivery_date"),"%d/%m/%Y"),
            paid_date=datetime.strptime(json_input.get("paid_date"),"%d/%m/%Y"),
            weight=json_input.get("weight"),
            status=json_input.get("status"),
            creator=json_input.get("creator")
            )
    if json_input.get('customer'):
      customer_id = json_input.get('customer').get('id')
      if customer_id:
        invoice.customer=customer_id
    db.add(invoice)

@post('/invoice/:id')
def updateInvoice(id,db):
    isValidUser(db,request)
    try:
        json_input = get_input_json(request)
        invoice = db.query(Invoice).filter_by(id=id).first()
        if json_input.get('customer'):
          customer_id = json_input.get('customer').get('id')
          if customer_id:
            invoice.customer=customer_id
        if json_input.get("inv_address"):invoice.inv_address=json_input.get("inv_address")
        if json_input.get("del_address"):invoice.del_address=json_input.get("del_address")
        if json_input.get("code"):invoice.code=json_input.get("code")
        if json_input.get("remark"):invoice.remark=json_input.get("remark")
        if json_input.get("shipping") is not None:invoice.shipping=json_input.get("shipping")
        if json_input.get("products") is not None:invoice.products=json_input.get("products")
        if json_input.get("total") is not None:invoice.total=json_input.get("total")
        if json_input.get("vat"):invoice.vat=json_input.get("vat")
        if json_input.get("creation_date"):invoice.creation_date=datetime.strptime(json_input.get("creation_date"),"%d/%m/%Y")
        if json_input.get("delivery_date"):invoice.delivery_date=datetime.strptime(json_input.get("delivery_date"),"%d/%m/%Y")
        if json_input.get("paid_date"):invoice.paid_date=datetime.strptime(json_input.get("paid_date"),"%d/%m/%Y")
        if json_input.get("weight") is not None:invoice.weight=json_input.get("weight")
        if json_input.get("status") is not None:invoice.status=json_input.get("status")
        if json_input.get("creator"):invoice.creator=json_input.get("creator")
        db.merge(invoice)
    except ValueError as ve:
        print ve
    except Exception as ex:
        print ex
    except:
        resource_not_found("Invoice")

@delete('/invoice/:id')
def deleteInvoice(id,db):
    isValidUser(db,request)
    try:
        invoice = db.query(Invoice).filter_by(id=id).first()
        soft_delete(db, invoice)
    except:
        resource_not_found("Invoice")

@get('/invoice/:id')
def getInvoice(id,db):
    isValidUser(db,request)
    try:
        invoice = db.query(Invoice).filter_by(id=id).first()
        customer = db.query(Customer).filter_by(id=invoice.customer).first()
        return invoice_json(invoice, customer)
    except:
        resource_not_found("Invoice")

#@get('/invoices')
#def getInvoices(db):
#    isValidUser(db,request)
#    invoices = db.query(Invoice)
#    return json.dumps([ {'id': i.id, } for i in invoices],ensure_ascii=False)

@get('/invoices')
def getInvoices(db):
    isValidUser(db,request)
    json_response = getJsonContainer()
    query = getQuery(db, Invoice, Customer)

    fromPos = request.params.get('from')
    quantity = request.params.get('quantity')
    paging = False
    if fromPos and quantity:
      paging=True
    if paging:
      invoices = query.offset(fromPos).limit(quantity)
    else:
      invoices = query.all()

    #invoices = getDbObjects(db, Invoice)
    full_info = getFullInfo()


    if full_info:
      for invoice in invoices:
          #customer = db.query(Customer).filter_by(id=invoice.customer).first()
          invDict = invoice_json(invoice[0], invoice[1])
          json_response['data'].append(invDict)
    else:
      for invoice in invoices:
          invDict = { 'id': invoice[0].id, 'code': invoice[0].code}
          json_response['data'].append(invDict)
    count = request.params.get('count')
    if count is not None and count is 'true':
      json_response['info']['count']=getCount(db, Invoice)
    return json.dumps(json_response,ensure_ascii=False)

def invoice_json(invoice, customer):
  invoice_json = {'id': invoice.id,
                  'inv_address': invoice.inv_address,
                  'del_address': invoice.del_address,
                  'code': invoice.code,
                  'remark': invoice.remark,
                  'shipping': invoice.shipping,
                  'products': invoice.products,
                  'total': invoice.total,
                  'vat': invoice.vat,
                  'creation_date': str(invoice.creation_date),
                  'delivery_date': str(invoice.delivery_date),
                  'paid_date': str(invoice.paid_date),
                  'weight': invoice.weight,
                  'status': invoice.status,
                  'creator': invoice.creator}
  if customer:
      invoice_json['customer'] = {'id': customer.id, 'name': customer.name}
  return invoice_json



def resource_not_found(resource):
    abort(404, "%s Not Found" %resource)

def forbidden():
    abort(403, "Please login")

def get_input_json(http_request):
    req = http_request.body.readline()
    if not req:
        abort(400, 'No data received')
    return json.loads(req)

def soft_delete(db, dbObject):
  dbObject.active = False
  db.merge(dbObject)

@get('/initdb')
def initdb(db):
  passwd = request.params.get('passwd')
  if(passwd == 'krishnaorjef'):
    try:
      cleaner.clean_all(db)
      cleaner.add_admin(db)
    except:
      return 'Problem while doing db init'
  else:
    return 'wrong passwd'


#LOCAL DB ACCESSOR METHODS



#def getUserByUsername(username,db):
#    try:
#        user = db.query(User).filter_by(username=username).first()
#        return user
#    except:
#        return None

def adapt_stock(db, article_id, quantity):
  stock = db.query(Stock).filter_by(id=article_id).first()
  if stock is None:
    stock = Stock(0, article_id, True)
  if quantity:
    stock.quantity -= quantity
    db.merge(stock)
    
def getDbObjects(db, clazz):
  isValidUser(db,request)
  fromPos = request.params.get('from')
  quantity = request.params.get('quantity')
  if request.params.get('orderOn') is not None:
    order_by = request.params.get('orderOn')
    if request.params.get('asc')=='true' or request.params.get('asc') is None:
      asc = True
    else:
      asc = False
  else:
    order_by = None
  additional_condition = request.params.get('additionalCondition')
  if request.params.get('includesNonActive') and request.params.get('includesNonActive')=='true':
    includes_non_active = True
  else:
    includes_non_active = False
  paging = False
  if fromPos and quantity:
    paging=True


  query = db.query(clazz)
  if additional_condition and includes_non_active :
    query = query.filter(additional_condition)
  elif additional_condition and not includes_non_active :
    query = query.filter(and_(clazz.active==1, additional_condition))
  elif not includes_non_active :
    query = query.filter(clazz.active==1)
  if order_by and asc:
    query = query.order_by(order_by)
  elif order_by and not asc:
    query = query.order_by(desc(order_by))
  else:
    query = query.order_by("id")
  if paging:
    objects = query.offset(fromPos).limit(quantity)
  else:
    objects = query.all()
  
  return objects

def getQuery(db, clazz, join_clazz):
  isValidUser(db,request)
  order_by = request.params.get('orderOn')
  if order_by is not None and len(order_by) > 0:
    if request.params.get('asc')=='true' or request.params.get('asc') is None:
      asc = True
    else:
      asc = False
    if '.' not in order_by:
      order_by = clazz.__name__.lower()+'.'+order_by
  else:
    order_by = clazz.__name__.lower()+'.id'
    asc = True
  additional_condition = request.params.get('additionalCondition')
  if request.params.get('includesNonActive') and request.params.get('includesNonActive')=='true':
    includes_non_active = True
  else:
    includes_non_active = False


  if join_clazz is None:
    query = db.query(clazz)
  else:
    query = db.query(clazz, join_clazz)
    query = query.join(join_clazz)
  if additional_condition and includes_non_active :
    query = query.filter(additional_condition)
  elif additional_condition and not includes_non_active :
    query = query.filter(and_(clazz.active==1, additional_condition))
  elif not includes_non_active :
    query = query.filter(clazz.active==1)
  if order_by and asc:
    query = query.order_by(order_by)
  elif order_by and not asc:
    query = query.order_by(desc(order_by))
  else:
    query = query.order_by(clazz.__name__.lower()+".id")

  return query

def getCount(db, clazz):
  isValidUser(db,request)
  additional_condition = request.params.get('additionalCondition')
  if request.params.get('includesNonActive') and request.params.get('includesNonActive')=='true':
    includes_non_active = True
  else:
    includes_non_active = False


  query = db.query(clazz)
  if additional_condition and includes_non_active :
    query = query.filter(additional_condition)
  elif additional_condition and not includes_non_active :
    query = query.filter(and_(clazz.active==1, additional_condition))
  elif not includes_non_active :
    query = query.filter(clazz.active==1)
  else:
    query = query.order_by("id")
  return query.count()

def getFullInfo():
  if request.params.get('fullInfo') and request.params.get('fullInfo')=='true':
    return True
  else:
    return False

def getJsonContainer():
  return {'info':{'count':-1},'data':[]}

