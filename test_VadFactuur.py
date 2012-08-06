import json
from webtest import TestApp
import server
import unittest

__author__ = 'jefw'

ap = TestApp(server.app)

class Test(unittest.TestCase):
  def test_a(self):
      print "Running for class", self.__class__

  def notest_clean_all(self):
    res = ap.get('/cleanAll')

  def test_clean_db(self):
    self.cleanInvoices()
    self.cleanLines()
    self.cleanArticle()
    self.cleanArticleType()
    self.cleanUnit()
    self.cleanSupplier()
    self.cleanCustomer()
    self.cleanPerson()
    self.cleanSector()
    self.cleanStock()
    self.cleanUser()
    self.cleanAddress()

  def cleanInvoices(self):
    res = ap.get('/invoices')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/invoice/%s' % anId)

  def cleanLines(self):
    res = ap.get('/invoiceLines')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/invoiceLine/%s' % anId)

  def cleanArticle(self):
    res = ap.get('/articles')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/article/%s' % anId)

  def cleanArticleType(self):
    res = ap.get('/articleTypes')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/articleType/%s' % anId)

  def cleanUnit(self):
    res = ap.get('/units')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/unit/%s' % anId)

  def cleanSupplier(self):
    res = ap.get('/suppliers')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/supplier/%s' % anId)

  def cleanCustomer(self):
    res = ap.get('/customers')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/customer/%s' % anId)

  def cleanPerson(self):
    res = ap.get('/persons')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/person/%s' % anId)

  def cleanSector(self):
    res = ap.get('/sectors')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/sector/%s' % anId)

  def cleanStock(self):
    res = ap.get('/stocks')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/stock/%s' % anId)

  def cleanUser(self):
    res = ap.get('/users')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      role = anObject.get('role')
      print 'role%s' % role
      #if(role <= 1):
      ap.delete('/user/%s' % anId)

  def cleanAddress(self):
    res = ap.get('/addresss')
    json_input = json.loads(res.body)
    for anObject in json_input:
      anId = anObject.get('id')
      print anId
      ap.delete('/address/%s' % anId)



if __name__ == '__main__':
    unittest.main()
