import bottle
import hashlib
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine, Column, Integer, BigInteger,Sequence, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://root:@localhost/vad3',echo=True)

class ArticleType(Base):
    __tablename__ = 'article_type'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    article = relationship("Article")

    def __init__(self, name):
        self.name = name

class Unit(Base):
    __tablename__ = 'unit'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    article = relationship("Article")

    def __init__(self, name):
        self.name = name

class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    article = relationship("Article")

    def __init__(self, name):
        self.name = name

class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    name = Column(String(200))
    username = Column(String(50))
    password_hash = Column(String(200))
    role = Column(Integer)
    article = relationship("Article")

    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        self.role = role

class Article(Base):
    __tablename__ = 'article'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    code = Column(String(50))
    name = Column(String(100))
    description = Column(String(500))
    list_price = Column(Float)
    weight = Column(Integer)
    create_date = Column(DateTime)
    vat = Column(Float)
    article_type = Column(BigInteger,ForeignKey("article_type.id"))
    unit = Column(BigInteger, ForeignKey("unit.id"))
    creator = Column(BigInteger, ForeignKey("user.id")) 
    supplier = Column(BigInteger, ForeignKey("supplier.id"))  
    stock = relationship("Stock")
    invoice_line = relationship("InvoiceLine")

    def __init__(self, code, name, description, list_price, weight, create_date, vat, article_type, unit, creator, supplier):
        self.code = code
        self.name = name
        self.description = description
        self.list_price = list_price
        self.weight = weight
        self.create_date = create_date
        self.vat = vat
        self.article_type = article_type
        self.unit = unit
        self.creator = creator
        self.supplier = supplier

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    quantity = Column(Integer)
    article = Column(BigInteger, ForeignKey("article.id"))

    def __init__(self, quantity, article):
        self.quantity = quantity
        self.article = article

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    vat = Column(Float)
    iban = Column(String(100))
    remark = Column(String(100))
    person = relationship("Person")
    address = relationship("Address")
    sector = Column(BigInteger, ForeignKey("sector.id"))
    subsector = Column(BigInteger, ForeignKey("sector.id"))
    relationship("sector",primaryjoin="sector.id==customer.sector")
    relationship("sector",primaryjoin="sector.id==customer.subsector")

    def __init__(self, name, vat, iban, remark, sector, subsector):
        self.name = name
        self.vat = vat
        self.iban = iban
        self.remark = remark
        self.sector = sector
        self.subsector = subsector

class Person(Base):
    __tablename__ = 'person'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    title = Column(String(10))
    name = Column(String(100))
    email = Column(String(100))
    mobile = Column(String(100))
    customer = Column(BigInteger, ForeignKey("customer.id"))

    def __init__(self, name, title, email, mobile, customer):
        self.name = name
        self.title = title
        self.email = email
        self.mobile = mobile
        self.customer = customer

class Sector(Base):
    __tablename__ = 'sector'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))
    parent = Column(BigInteger, ForeignKey("sector.id"))
    children = relationship("Sector")

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

class InvoiceLine(Base):
    __tablename__ = 'invoice_line'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    article = Column(BigInteger, ForeignKey("article.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    discount = Column(Float)
    unit_discount = Column(Float)
    invoice = Column(BigInteger, ForeignKey("invoice.id"))

    def __init(self, article, quantity, unit_price, discount, unit_discount, invoice):
        self. article = article
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount = discount
        self.unit_discount = unit_discount
        self.invoice = invoice


class Address(Base):
    __tablename__ = 'address'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    customer = Column(BigInteger, ForeignKey("customer.id"))
    address_type = Column(Integer)
    address = Column(String(500))
    zipcode = Column(String(20))
    city = Column(String(500))
    tel = Column(String(20))
    fax = Column(String(20))
    email = Column(String(200))

    def __init__(self, customer, address_type, address, zipcode, city, tel, fax, email):
        self.customer = customer
        self.address_type = address_type
        self.address = address
        self.zipcode = zipcode
        self.city = city
        self.tel = tel
        self.fax = fax
        self.email = email

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    customer = Column(BigInteger, ForeignKey("customer.id"))
    inv_address = Column(BigInteger, ForeignKey("address.id"))
    del_address = Column(BigInteger, ForeignKey("address.id"))
    code = Column(String(100))
    remark = Column(String(300))
    shipping = Column(Float)
    total = Column(Float)
    vat = Column(Float)
    creation_date = Column(DateTime)
    delivery_date = Column(DateTime)
    paid_date = Column(DateTime)
    weight = Column(Float)
    status = Column(Integer)
    creator = Column(BigInteger, ForeignKey("user.id"))
    relationship("address",primaryjoin="address.id==invoice.del_address")
    relationship("address",primaryjoin="address.id==invoice.inv_address")
    invoice_line = relationship("InvoiceLine")

    def __init__(self, customer, inv_address, del_address, code, remark, shipping, total, vat, creation_date, delivery_date, paid_date, weight, status, creator):
        self.customer = customer
        self.inv_address = inv_address
        self.del_address = del_address
        self.code = code
        self.remark = remark
        self.shipping = shipping
        self.total = total
        self.vat = vat
        self.creation_date = creation_date
        self.delivery_date = delivery_date
        self.paid_date = paid_date
        self.weight = weight
        self.status = status
        self.creator = creator


bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))
Base.metadata.create_all(engine)
