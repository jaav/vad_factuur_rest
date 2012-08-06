import json
from time import strptime
from bottle import get, post, put, delete, request, abort, response
import hashlib
import settings
from sqlalchemy import or_
from model import User, Unit, ArticleType, Supplier, Sector, Person, Customer, Address, Article, Stock, InvoiceLine, Invoice


__author__ = 'jefw'

def add_admin(db):
  try:
    user = User(name='Admin', username='admin', password='admin', role=2)
    db.add(user)
  except:
    return 'Problem while doing db init'

def clean_all(db):
  try:
    cleanInvoices(db)
    cleanLines(db)
    cleanArticles(db)
    cleanArticleTypes(db)
    cleanUnits(db)
    cleanSuppliers(db)
    cleanCustomers(db)
    cleanPersons(db)
    cleanSectors(db)
    cleanStocks(db)
    cleanUsers(db)
    cleanAddresss(db)
    return 'SUCCESSO'
  except:
    return 'PROBLEMO'


def cleanInvoices(db):
  invoices = db.query(Invoice)
  for invoice in invoices:
    db.delete(invoice)

def cleanLines(db):
  lines = db.query(InvoiceLine)
  for line in lines:
    db.delete(line)

def cleanArticles(db):
  articles = db.query(Article)
  for article in articles:
    db.delete(article)

def cleanArticleTypes(db):
  articleTypes = db.query(ArticleType)
  for articleType in articleTypes:
    db.delete(articleType)

def cleanUnits(db):
  units = db.query(Unit)
  for units in units:
    db.delete(units)

def cleanSuppliers(db):
  suppliers = db.query(Supplier)
  for supplier in suppliers:
    db.delete(supplier)

def cleanCustomers(db):
  customers = db.query(Customer)
  for customer in customers:
    db.delete(customer)

def cleanPersons(db):
  persons = db.query(Person)
  for person in persons:
    db.delete(person)

def cleanSectors(db):
  sectors = db.query(Sector)
  for sector in sectors:
    db.delete(sector)

def cleanStocks(db):
  stocks = db.query(Stock)
  for stock in stocks:
    db.delete(stock)

def cleanUsers(db):
  users = db.query(User)
  for user in users:
    db.delete(user)

def cleanAddresss(db):
  addresss = db.query(Address)
  for address in addresss:
    db.delete(address)


