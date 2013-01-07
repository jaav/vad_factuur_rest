import bottle
import hashlib
import settings
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine, Column, Integer, Integer,Sequence, String, ForeignKey, Float, DateTime, Boolean, Date
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()
engine = create_engine(settings.database,echo=True)

class MyMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id =  Column(Integer, Sequence('id_seq'), primary_key=True)
    active = Column(Boolean)

class ArticleType(Base):
    __tablename__ = 'article_type'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    article = relationship("Article")
    active = Column(Boolean)

    def __init__(self, name, active=True):
        self.name = name
        self.active = active

class Unit(Base):
    __tablename__ = 'unit'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    article = relationship("Article")
    active = Column(Boolean)

    def __init__(self, name):
        self.name = name
        self.active=1


class Post(MyMixin, Base):
    __tablename__ = 'post'
    bottom_weight = Column(Float)
    top_weight = Column(Float)
    price = Column(Float)
    name = Column(String(100))

    def __init__(self, name, bottom, top, price):
        self.name=name
        self.bottom_weight = bottom
        self.top_weight=top
        self.price=price
        self.active = 1


class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    article = relationship("Article")
    active = Column(Boolean)

    def __init__(self, name, active=True):
        self.name = name
        self.active=active
      


class UpdateStatus(Base):
    __tablename__ = 'update_status'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    user = Column(Integer,ForeignKey("user.id"))
    articles = Column(Boolean)
    customers = Column(Boolean)

    def __init__(self, user, articles, customers):
        self.user = user.id
        self.articles = articles
        self.customers = customers
      
    def setRefreshArticles(self, user, articles):
        self.user = user.id
        self.articles = articles
      
    def setRefreshCustomers(self, user, customers):
        self.user = user.id
        self.customers = customers

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(200))
    username = Column(String(50))
    password_hash = Column(String(200))
    role = Column(Integer)
    article = relationship("Article")
    active = Column(Boolean)

    def __init__(self, name, username, password, role, active=True):
        self.name = name
        self.username = username
        self.password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        self.role = role
        self.active=active

    def addHash(self, password):
        self.password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()

class Article(MyMixin, Base):
    __tablename__ = 'article'
    #id = Column(Integer, Sequence('id_seq'), primary_key=True)
    code = Column(String(50))
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Float)
    weight = Column(Integer)
    create_date = Column(DateTime)
    copy_date = Column(Date)
    vat = Column(Float)
    article_type = Column(Integer,ForeignKey("article_type.id"))
    unit = Column(Integer, ForeignKey("unit.id"))
    creator = Column(Integer, ForeignKey("user.id")) 
    supplier = Column(Integer, ForeignKey("supplier.id"))  
    stock = relationship("Stock")
    invoice_line = relationship("InvoiceLine")
    #active = Column(Boolean)
    free_quantity = Column(Integer)

    def __init__(self, code, name, description, price, free_quantity, copy_date, weight, create_date, vat, article_type, unit, creator, supplier, active=True):
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.weight = weight
        self.create_date = create_date
        self.vat = vat
        self.article_type = article_type
        self.unit = unit
        self.creator = creator
        self.supplier = supplier
        self.free_quantity = free_quantity
        self.copy_date = copy_date
        self.active = active

class Stock(MyMixin, Base):
    __tablename__ = 'stock'
    quantity = Column(Integer)
    article = Column(Integer, ForeignKey("article.id"))

    def __init__(self, quantity, article, active=True):
        self.quantity = quantity
        self.article = article
        self.active = active

class Customer(MyMixin, Base):
    __tablename__ = 'customer'
    name = Column(String(100))
    vat = Column(String(20))
    iban = Column(String(100))
    remark = Column(String(100))
    persons = relationship("Person", backref="Customer")
    addresses = relationship("Address", backref="Customer")
#    person = relationship("Person")
#    address = relationship("Address")
    sector = Column(Integer, ForeignKey("sector.id"))
    subsector = Column(Integer, ForeignKey("sector.id"))
    relationship("sector",primaryjoin="sector.id==customer.sector")
    relationship("sector",primaryjoin="sector.id==customer.subsector")

    def __init__(self, name, vat, iban, remark, sector, subsector, active=True):
        self.name = name
        self.vat = vat
        self.iban = iban
        self.remark = remark
        self.sector = sector
        self.subsector = subsector
        self.active=active

class Person(MyMixin, Base):
    __tablename__ = 'person'
    title = Column(String(10))
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(100))
    customer = Column(Integer, ForeignKey('customer.id'))
    customer_rel = relationship("Customer", primaryjoin="Person.customer==Customer.id")
#    customer = Column(Integer, ForeignKey("customer.id"))

    def __init__(self, name, title, email, phone, customer, active=True):
        self.name = name
        self.title = title
        self.email = email
        self.phone = phone
        self.customer = customer
        self.active = active

class Sector(MyMixin, Base):
    __tablename__ = 'sector'
    name = Column(String(100))
    parent = Column(Integer, ForeignKey("sector.id"))
#    parent_rel = relation('Sector')
    children = relationship("Sector")

    def __init__(self, name, parent, active=True):
        self.name = name
        self.parent = parent
        self.active=active

class InvoiceLine(MyMixin, Base):
    __tablename__ = 'invoice_line'
    article = Column(Integer, ForeignKey("article.id"))
    quantity = Column(Integer)
    weight = Column(Float)
    unit_price = Column(Float)
    unit_discount = Column(Float)
    invoice = Column(Integer, ForeignKey("invoice.id"))
    apply_free = Column(Boolean)

    def __init(self, article, quantity, unit_price, unit_discount, invoice, active=True, apply_free=True):
        self. article = article
        self.quantity = quantity
        self.unit_price = unit_price
        self.unit_discount = unit_discount
        self.invoice = invoice
        self.active=active
        self.apply_free=apply_free


class Address(MyMixin, Base):
    __tablename__ = 'address'

    customer = Column(Integer, ForeignKey('customer.id'))
    customer_rel = relationship("Customer", primaryjoin="Customer.id==Address.customer")
#    customer = Column(Integer, ForeignKey("customer.id"))
    address_type = Column(Integer)
    street = Column(String(500))
    zipcode = Column(String(20))
    city = Column(String(500))
    tel = Column(String(20))
    fax = Column(String(20))
    email = Column(String(200))
    att = Column(String(200))

    def __init__(self, customer, address_type, street, zipcode, city, tel, fax, email, att, active=True):
        self.customer = customer
        self.address_type = address_type
        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.tel = tel
        self.fax = fax
        self.email = email
        self.att = att
        self.active=active

class Invoice(MyMixin, Base):
    __tablename__ = 'invoice'
    customer = Column(Integer, ForeignKey("customer.id"))
    inv_address = Column(Integer, ForeignKey("address.id"))
    del_address = Column(Integer, ForeignKey("address.id"))
    code = Column(String(100))
    remark = Column(String(300))
    shipping = Column(Float)
    products = Column(Float)
    total = Column(Float)
    vat = Column(Float)
    creation_date = Column(DateTime)
    invoice_date = Column(DateTime)
    delivery_date = Column(DateTime)
    paid_date = Column(DateTime)
    weight = Column(Float)
    status = Column(Integer)
    creator = Column(Integer, ForeignKey("user.id"))
    relationship("address",primaryjoin="address.id==invoice.del_address")
    relationship("address",primaryjoin="address.id==invoice.inv_address")
    invoice_line = relationship("InvoiceLine")

    def __init__(self, customer, inv_address, del_address, code, remark, shipping, products, total, vat, creation_date, delivery_date, paid_date, weight, status, creator, active=True):
        self.customer = customer
        self.inv_address = inv_address
        self.del_address = del_address
        self.code = code
        self.remark = remark
        self.shipping = shipping
        self.products = products
        self.total = total
        self.vat = vat
        self.creation_date = creation_date
        self.delivery_date = delivery_date
        self.paid_date = paid_date
        self.weight = weight
        self.status = status
        self.creator = creator
        self.active=active


bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))
Base.metadata.create_all(engine)



#ALTER TABLE address ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE article ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE article_type ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE customer ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE invoice ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE invoice_line ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE person ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE sector ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE stock ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE supplier ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE unit ADD COLUMN active BOOL DEFAULT true NOT NULL;
#ALTER TABLE user ADD COLUMN active BOOL DEFAULT true NOT NULL;

#ALTER TABLE article ADD COLUMN free_quantity INT DEFAULT 0 NOT NULL;
#ALTER TABLE article ADD COLUMN copy_date DATE AFTER create_date;

#ALTER table person CHANGE mobile phone varchar(100);

#ALTER TABLE invoice_line ADD COLUMN apply_free BOOL DEFAULT true NOT NULL;

#alter table article change list_price price

#ALTER TABLE invoice ADD COLUMN products FLOAT AFTER shipping;


#update invoice set products = shipping;

#update invoice set shipping = total-products;

#de-activate all products having '******_*****' in their description
#create a default supplier and add it as supplier to all products
#create a default article_type and add it as type  to all products

#ALTER TABLE address ADD COLUMN att VARCHAR(200);

#alter table address change address street
