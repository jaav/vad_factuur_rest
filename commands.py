import json
from bottle import get, post, put, delete, request, abort
import hashlib
from sqlalchemy import or_
from model import User, Unit, ArticleType, Supplier, Sector, Person, Customer, Address, Article, Stock, InvoiceLine, Invoice

@put('/user')
@post('/user')
def setUser(db):
    json_input = get_input_json(request)
    user = User(name=json_input.get("name"), username=json_input.get("username"), password=json_input.get("password"), role=json_input.get("role"))
    db.add(user)

@post('/user/:id')
def updateUser(id,db):
    try:
        user = db.query(User).filter_by(id=id).first()
        json_input = get_input_json(request)
        if json_input.get("name"): user.name = json_input.get("name")
        if json_input.get("username"): user.username = json_input.get("username")
        if json_input.get("password"): user.password = hashlib.md5(json_input.get("password").encode("utf-8")).hexdigest()
        if json_input.get("role"): user.role = json_input.get("role")
        db.merge(user)
    except:
        resource_not_found( 'User not found')

@get('/user/:id')
def getUser(id,db):
    try:
        user = db.query(User).filter_by(id=id).first()
        return {'id': user.id,
                     'name': user.name,
                     'username': user.username,
                     'role': user.role}
    except:
        resource_not_found( 'User')

@get('/users')
def getUsers(db):
    users = db.query(User)
    json_response = [ {'id': user.id,
                       'name': user.name,
                       'username': user.username,
                       'role': user.role} for user in users]
    return json_response

@delete('/user/:id')
def deleteUser(id, db):
    try:
        user = db.query(User).filter_by(id=id).first()
        db.delete(user)
    except:
        resource_not_found( 'User')

@put('/unit')
@post('unit')
def setUnit(db):
    json_input = get_input_json(request)
    unit = Unit(name=json_input.get("name"))
    db.add(unit)

@post('/unit/:id')
def updateUnit(id,db):
    try:
        unit = db.query(Unit).filter_by(id=id).first()
        json_input = get_input_json(request)
        if json_input.get("name"): unit.name = json_input.get("name")
        db.merge(unit)
    except:
        resource_not_found( "Unit not found")

@get('/unit/:id')
def getUnit(id,db):
    try:
        unit = db.query(Unit).filter_by(id=id).first()
        return {'id': unit.id,
                'name': unit.name}
    except:
        resource_not_found( "Unit")

@get('/units')
def getUnits(db):
    units = db.query(Unit)
    json_response = [ {'id': unit.id,
                        'name': unit.name} for unit in units]
    return json_response

@delete('/unit/:id')
def deleteUnit(id,db):
    try:
        unit = db.query(Unit).filter_by(id=id).first()
        db.delete(unit)
    except:
        resource_not_found("Unit")

@put('/articleType')
@post('/articleType')
def addArticleType(db):
    json_input = get_input_json(request)
    articleType = ArticleType(name=json_input.get("name"))
    db.add(articleType)

@post('/articleType/:id')
def updateArticleType(id,db):
    try:
        json_input = get_input_json(request)
        articleType = db.query(ArticleType).filter_by(id=id).first()
        if json_input.get("name"): articleType.name = json_input.get("name")
        db.merge(articleType)
    except:
        resource_not_found("ArticleType")

@get('/articleType/:id')
def getArticleType(id,db):
    try:
        articleType = db.query(ArticleType).filter_by(id=id).first()
        return {'id': articleType.id,
                'name': articleType.name}
    except:
        resource_not_found("ArticleType")

@get('/articleTypes')
def getArticleTypes(db):
    articleTypes = db.query(ArticleType)
    json_response = [ {'id': a.id,
                        'name': a.name} for a in articleTypes]
    return json_response

@delete('/articleType/:id')
def deleteArticleType(id,db):
    try:
        articleType = db.query(ArticleType).filter_by(id=id).first()
        db.delete(articleType)
    except:
        resource_not_found("ArticleType")

@put('/supplier')
@post('/supplier')
def addSupplier(db):
    json_input = get_input_json(request)
    supplier = Supplier(name=json_input.get("name"))
    db.add(supplier)

@post('/supplier/:id')
def updateSupplier(id,db):
    try:
        json_input = get_input_json(request)
        supplier = db.query(Supplier).filter_by(id=id).first()
        if json_input.get("name"): supplier.name = json_input.get("name")
        db.merge(supplier)
    except:
        resource_not_found("Supplier")

@get('/supplier/:id')
def getSupplier(id,db):
    try:
        supplier = db.query(Supplier).filter_by(id=id).first()
        return {'id': supplier.id,
                'name': supplier.name}
    except:
        resource_not_found("Supplier")

@get('/suppliers')
def getSuppliers(db):
        suppliers = db.query(Supplier)
        json_response = [
                {'id': s.id,
                    'name': s.name} for s in suppliers]
        return json_response

@delete('/supplier/:id')
def deleteSupplier(id,db):
    try:
        supplier = db.query(Supplier).filter_by(id=id).first()
        db.delete(supplier)
    except:
        resource_not_found("Supplier")

@put('/sector')
@post('/sector')
def addSector(id, db):
    json_input = get_input_json(request)
    sector = Sector(json_input.get('name'),json_input.get('parent'))
    db.add(sector) 

@post('/sector/:id')
def updateSector(id, db):
    try:
        json_input = get_input_json(request)
        sector = db.query(Sector).filter_by(id=id).first()
        if json_input.get('name'): sector.name = json_input.get('name')
        if json_input.get('parent'): sector.parent = json_input.get('parent')
        db.merge(sector)
    except:
        resource_not_found("Sector")

@get('/sector/:id')
def getSector(id, db):
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
    sectors = db.query(Sector)
    json_response = [
            {'id': s.id,
                'name': s.name,
                'parent': s.parent} for s in sectors]
    return json_response

@delete('/sector/:id')
def deleteSector(id, db):
    try:
        sector = db.query(Sector).filter_by(id=id).first()
        db.delete(sector)
    except:
        resource_not_found("Sector")

@put('/person')
@post('/person')
def addPerson(db):
    try:
        json_input = get_input_json(request)
        person  = Person(title=json_input.get('title'),
                name=json_input.get('name'),email=json_input.get('email'),
                mobile=json_input.get('mobile'),customer=json_input.get('customer'))
        db.add(person)
    except:
        resource_not_found("Person")

@post('/person/:id')
def updatePerson(id,db):
    try:
        json_input = get_input_json(request)
        person = db.query(Person).filter_by(id=id).first()
        if json_input.get('name'): person.name = json_input.get('name')
        if json_input.get('email'): person.email = json_input.get('email')
        if json_input.get('mobile'): person.mobile = json_input.get('mobile')
        if json_input.get('customer'): person.customer = json_input.get('customer')
        if json_input.get('title'): person.title = json_input.get('title')
        db.merge(person)
    except:
        resource_not_found("Person")

@get('/person/:id')
def getPerson(id,db):
    try:
        person = db.query(Person).filter_by(id=id).first()
        return { 'id': person.id,
                'title': person.title,
                'name': person.name,
                'email': person.email,
                'mobile': person.mobile,
                'customer': person.customer }
    except:
        resource_not_found("Person")

@get('/personByCustomer/:id')
def getPersonByCustomer(id,db):
    try:
        person = db.query(Person).filter_by(customer=id).first()
        return { 'id': person.id,
                'title': person.title,
                'name': person.name,
                'email': person.email,
                'mobile': person.mobile,
                'customer': person.customer }
    except:
        resource_not_found("Person")

@delete('/person/:id')
def deletePerson(id,db):
    try:
        person = db.query(Person).filter_by(id=id).first()
        db.delete(person)
    except:
        resource_not_found("Person")

@get('/persons')
def getPersons(db):
    persons= db.query(Person)
    json_response = [ { 'id': person.id } for person in persons]
    return json_response

@put('/customer')
@post('/customer')
def addCustomer(db):
    json_input = get_input_json(request)
    customer = Customer(name=json_input.get('name'),vat=json_input.get('vat'),
            iban=json_input.get('iban'),remark=json_input.get('remark'),
            sector=json_input.get('sector'),subsector=json_input.get('subsector'))
    db.add(customer)

@post('/customer/:id')
def updateCustomer(id,db):
    try:
        json_input = get_input_json(request)
        customer = db.query(Customer).filter_by(id=id).first()
        if json_input.get('name'): customer.name = json_input.get('name')
        if json_input.get('vat'): customer.vat = json_input.get('vat')
        if json_input.get('iban'): customer.iban = json_input.get('iban')
        if json_input.get('remark'): customer.remark = json_input.get('remark')
        if json_input.get('sector'): customer.sector = json_input.get('sector')
        if json_input.get('subsector'): customer.subsector = json_input.get('subsector')
        db.merge(customer)
    except:
        resource_not_found("Customer")

@get('/customer/:id')
def getCustomer(id,db):
    try:
        customer = db.query(Customer).filter_by(id=id).first()
        return {'id': customer.id,
                'name': customer.name,
                'vat': customer.vat,
                'iban': customer.iban,
                'remark': customer.remark,
                'sector': customer.sector,
                'subsector': customer.subsector}
    except:
        resource_not_found("Customer")

@delete('/customer/:id')
def deleteCustomer(id,db):
    try:
        customer = db.query(Customer).filter_by(id=id).first()
        db.delete(customer)
    except:
        resource_not_found("Customer")

@get('/customers')
def getCustomers(db):
    customers = db.query(Customer)
    return [{'id' : cust.id } for cust in customers]

@get('/customersBySector/:id')
def getCustomersBySector(id,db):
    try:
        customers = db.query(Customer).filter(or_ (Customer.sector==id),
                (Customer.subsector==id))
        return [{'id' : cust.id } for cust in customers]
    except:
        resource_not_found("Customers")

@put('/address')
@post('/address')
def addAddress(db):
    json_input = get_input_json(request)
    address = Address(customer=json_input.get('customer'),address=json_input.get('address'),
            address_type=json_input.get('address_type'),zipcode=json_input.get('zipcode'),
            city=json_input.get('city'),tel=json_input.get('tel'),fax=json_input.get('fax'),
            email=json_input.get('email'))
    db.add(address)

@post('/address/:id')
def updateAddress(id,db):
    try:
        json_input = get_input_json(request)
        address = db.query(Address).filter_by(id=id).first()
        if json_input.get('customer'): address.customer = json_input.get('customer')
        if json_input.get('address_type'): address.address_type = json_input.get('address_type')
        if json_input.get('address'): address.address = json_input.get('address')
        if json_input.get('zipcode'): address.zipcode = json_input.get('zipcode')
        if json_input.get('city'): address.city = json_input.get('city')
        if json_input.get('tel'): address.tel = json_input.get('tel')
        if json_input.get('fax'): address.fax = json_input.get('fax')
        if json_input.get('email'): address.email = json_input.get('email')
        db.merge(address)
    except:
        resource_not_found("Address")

@get('/address/:id')
def getAddress(id,db):
    try:
        address = db.query(Address).filter_by(id=id).first()
        return {'id': address.id,
                'customer': address.customer,
                'address': address.address,
                'address_type': address.address_type,
                'zipcode': address.zipcode,
                'city': address.city,
                'tel': address.tel,
                'fax': address.fax,
                'email': address.email }
    except:
        resource_not_found('Address')

@get('/addresses')
def getAddresses(db):
    addresses = db.query(Address)
    json_response = [ {'id': a.id} for a in addresses]
    return json_response

@delete('/address/:id')
def deleteAddress(id,db):
    try:
        address = db.query(Address).filter_by(id=id).first()
        db.delete(address)
    except:
        resource_not_found('Address')


@put('/article')
@post('/article')
def addArticle(db):
    json_input = get_input_json(request)
    article = Article(article_type=json_input.get('article_type'),
            code=json_input.get('code'), name=json_input.get('name'),
            description=json_input.get('description'),list_price=json_input.get('listPrice'),
            unit=json_input.get('unit'),supplier=json_input.get('supplier'),
            weight=json_input.get('weight'), create_date=json_input.get('create_date'),
            vat=json_input.get('vat'),creator=json_input.get('creator'))
    db.add(article)

@post('/article/:id')
def updateArticle(id,db):
    try:
        json_input = get_input_json(request)
        article = db.query(Article).filter_by(id=id).first()
        if json_input.get('article_type'): article.article_type=json_input.get('article_type')
        if json_input.get('code'): article.code=json_input.get('code')
        if json_input.get('name'): article.name=json_input.get('name')
        if json_input.get('description'): article.description=json_input.get('description')
        if json_input.get('listPrice'): article.list_price=json_input.get('listPrice')
        if json_input.get('unit'): article.unit=json_input.get('unit')
        if json_input.get('weight'): article.weight=json_input.get('weight')
        if json_input.get('create_date'): article.create_date=json_input.get('create_date')
        if json_input.get('vat'): article.vat=json_input.get('vat')
        if json_input.get('creator'): article.creator=json_input.get('creator')
        if json_input.get('supplier'): article.supplier=json_input.get('supplier')
        db.merge(article)
    except:
        resource_not_found("Article")

@get('/articles')
def getArticles(db):
    articles = db.query(Article)
    return [ {'id': a.id } for a in articles ]

@get('/articleBySupplier/:supplierId')
def getArticlesBySupplier(supplierId,db):
    try:
        articles = db.query(Article).filter_by(supplier=supplierId).all()
        return [ {'id': a.id } for a in articles ]
    except:
        resource_not_found("Article")

@get('/article/:id')
def getArticle(id,db):
    try:
        article = db.query(Article).filter_by(id=id).first()
        return { 'id': article.id,
                 'article_type': article.article_type,
                 'code': article.code,
                 'name': article.name,
                 'description': article.description,
                 'listPrice': article.list_price,
                 'unit': article.Unit,
                 'weight': article.weight,
                 'create_date': article.create_date,
                 'vat': article.vat,
                 'creator': article.creator,
                 'supplier': article.supplier
                 }
    except:
        resource_not_found("Article")

@delete('/article/:id')
def deleteArticle(id,db):
    try:
        article = db.query(Article).filter_by(id=id).first()
        db.delete(article)
    except:
        resource_not_found('Article')

@put('/stock')
@post('/stock')
def addStock(db):
    json_input = get_input_json(request)
    stock = Stock(article=json_input.get('article'),quantity=json_input.get('quantity'))
    db.add(stock)

@post('/stock/:id')
def updateStock(id,db):
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
    try:
        stock = db.query(Stock).filter_by(id=id).first()
        return {'id': stock.id,
                'article': stock.article,
                'quantity': stock.quantity }
    except:
        resource_not_found("Stock")

@delete('/stock/:id')
def deleteStock(id,db):
    try:
        stock = db.query(Stock).filter_by(id=id).first()
        db.delte(stock)
    except:
        resource_not_found("Stock")

@get('/stocks')
def getStocks(db):
    stocks = db.query(Stock)
    json_response = [ {'id': s.id,
        'article': s.article,
        'quantity': s.quantity} for s in stocks ]
    return json_response

@put('/invoiceLine')
@post('/invoiceLine')
def addInvoiceLine(db):
    json_input = get_input_json(request)
    invoice_line = InvoiceLine(article=json_input.get('article'),
            quantity=json_input.get('quantity'),
            unit_price=json_input.get('unit_price'),
            discount=json_input.get('discount'),
            unit_discount=json_input.get('unit_discount'),
            invoice=json_input.get('invoice'))
    db.add(invoice_line)

@post('/invoiceLine/:id')
def updateInvoiceLine(id,db):
    try:
        json_input = get_input_json(request)
        invoice_line = db.query(InvoiceLine).filter_by(id=id).first()
        if json_input.get('article'): invoice_line.article=json_input.get('article')
        if json_input.get('quantity'): invoice_line.quantity=json_input.get('quantity')
        if json_input.get('unit_price'): invoice_line.unit_price=json_input.get('unit_price')
        if json_input.get('discount'): invoice_line.discount=json_input.get('discount')
        if json_input.get('unit_discount'): invoice_line.unit_discount=json_input.get('unit_discount')
        if json_input.get('invoice'): invoice_line.invoice=json_input.get('invoice')
        db.merge(invoice_line)
    except:
        resource_not_found("InvoiceLine")

@get('/invoiceLine/:id')
def getInvoiceLine(id,db):
    try:
        invoice_line = db.query(InvoiceLine).filter_by(id=id).first()
        return {'id': invoice_line.id,
                'article': invoice_line.article,
                'quantity': invoice_line.quantity,
                'unit_price': invoice_line.unit_price,
                'discount': invoice_line.discount,
                'unit_discount': invoice_line.unit_discount,
                'invoice': invoice_line.invoce }
    except:
        resource_not_found("InvoiceLine")

@get('/invoiceLines')
def getInvoiceLines(db):
    invoice_lines = db.query(InvoiceLine)
    return [{'id': i.id} for i in invoice_lines]

@delete('/invoiceLine/:id')
def deleteInvoiceLine(id,db):
    try:
        invoice_line = db.query(InvoiceLine).filter_by(id=id).first()
        db.delete(invoice_line)
    except:
        resource_not_found("InvoiceLine")

@put('/invoice')
@post('/invoice')
def addInvoice(db):
    json_input = get_input_json(request)
    invoice = Invoice(customer=json_input.get('customer'),
            inv_address=json_input.get("inv_address"),
            del_address=json_input.get("del_address"),
            code=json_input.get("code"),
            remark=json_input.get("remark"),
            shipping=json_input.get("shipping"),
            total=json_input.get("total"),
            vat=json_input.get("vat"),
            creation_date=json_input.get("creation_date"),
            delivery_date=json_input.get("delivery_date"),
            paid_date=json_input.get("paid_date"),
            weight=json_input.get("weight"),
            status=json_input.get("status"),
            creator=json_input.get("creator"),
            )
    db.add(invoice)

@post('/invoice/:id')
def updateInvoice(id,db):
    try:
        json_input = get_input_json(request)
        invoice = db.query(Invoice).filter_by(id=id).first()
        if json_input.get('customer'):invoice.customer=json_input.get('customer')
        if json_input.get("inv_address"):invoice.inv_address=json_input.get("inv_address")
        if json_input.get("del_address"):invoice.del_address=json_input.get("del_address")
        if json_input.get("code"):invoice.code=json_input.get("code")
        if json_input.get("remark"):invoice.remark=json_input.get("remark")
        if json_input.get("shipping"):invoice.shipping=json_input.get("shipping")
        if json_input.get("total"):invoice.total=json_input.get("total")
        if json_input.get("vat"):invoice.vat=json_input.get("vat")
        if json_input.get("creation_date"):invoice.creation_date=json_input.get("creation_date")
        if json_input.get("delivery_date"):invoice.delivery_date=json_input.get("delivery_date")
        if json_input.get("paid_date"):invoice.paid_date=json_input.get("paid_date")
        if json_input.get("weight"):invoice.weight=json_input.get("weight")
        if json_input.get("status"):invoice.status=json_input.get("status")
        if json_input.get("creator"):invoice.creator=json_input.get("creator")
        db.merge(invoice)
    except:
        resource_not_found("Invoice")

@delete('/invoice/:id')
def deleteInvoice(id,db):
    try:
        invoice = db.query(Invoice).filter_by(id=id).first()
        db.delete(invoice)
    except:
        resource_not_found("Invoice")

@get('/invoice/:id')
def getInvoice(id,db):
    try:
        invoice = db.query(Invoice).filter_by(id=id).first()
        return {'id': invoice.id,
                'customer': invoice.customer,
                'inv_address': invoice.inv_address,
                'del_address': invoice.del_address,
                'code': invoice.code,
                'remark': invoice.remark,
                'shipping': invoice.shipping,
                'total': invoice.total,
                'vat': invoice.vat,
                'creation_date': invoice.creation_date,
                'delivery_date': invoice.deliver_date,
                'paid_date': invoice.paid_date,
                'weight': invoice.weight,
                'status': invoice.status,
                'creator': invoice.creator }
    except:
        resource_not_found("Invoice")

@get('/invoices')
def getInvoices(db):
    invoices = db.query(Invoice)
    return [ {'id': i.id} for i in invoices]

def resource_not_found(resource):
    abort(404, "%s Not Found" %resource)

def get_input_json(http_request):
    req = http_request.body.readline()
    if not req:
        abort(400, 'No data received')
    return json.loads(req)