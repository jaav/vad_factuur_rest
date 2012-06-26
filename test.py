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
     res = ap.post('/user',json.dumps(dict(name='krishna',password='pass',username='kittugadu',role=2)))
     res = ap.get('/users')
     assertResponseOk(res)
     a = json.loads(res.body)
     assertNotNone(a[0],'name')
     assertNotNone(a[0],'role')
     assertNotNone(a[0],'username')
     assertNone(a[0],'password')
     user_id = a[0].get('id')
     res = ap.get('/user/%s' %user_id)
     resp_dict = json.loads(res.body)
     res_name = resp_dict.get('name')
     res_username = resp_dict.get('username')
     update_user_dict = dict(name=res_name+'Updated',username=res_username+'Updated')
     res = ap.post('/user/%s' %user_id, json.dumps(update_user_dict))
     assertResponseOk(res)
     res = ap.get('/user/%s' %user_id)
     assertResponseOk(res)
     resp_dict = json.loads(res.body)
     assert resp_dict.get('name') == res_name+'Updated'
     assert resp_dict.get('username') == res_username+'Updated'

def test_ArticleType():
    noun = 'articleType'
    noun_dict = dict(name=noun)
    members = ['name']
    up_dict = dict(name=noun+'Updated')
    testNounCrud(noun,noun_dict,up_dict,members)

def test_Unit():
    noun = 'unit'
    noun_dict = dict(name=noun)
    members = ['name']
    up_dict = dict(name=noun+'Updated')
    testNounCrud(noun,noun_dict,up_dict,members)

def test_Supplier():
    noun = 'supplier'
    noun_dict = dict(name=noun)
    members = ['name']
    up_dict = dict(name=noun+'Updated')
    testNounCrud(noun,noun_dict,up_dict,members)

def test_Sector():
    noun = 'sector'
    noun_dict = dict(name=noun)
    members = ['name']
    up_dict = dict(name=noun+'Updated')
    testNounCrud(noun,noun_dict,up_dict,members)

def test_Customer():
    sec_dicts = getAllNounsTest('sector')
    sec1 = sec_dicts[0].get('id')
    sec2 = sec_dicts[1].get('id')
    noun = 'customer'
    noun_dict = dict(name='aName',vat='22.5',iban='2522',remark='aRemark',
            sector=sec1,subsector=sec2)
    members = ['name', 'vat', 'iban','remark','sector','subsector']
    up_dict = dict(name='aNameUpd',vat='25.5',iban='2522Upda',remark='aRemarkUped',
            sector=sec2,subsector=sec1)
    testNounCrudExt(noun,noun_dict,up_dict,members)
    #============================================
    res = ap.get('/customersBySector/%s' %sec1)
    assertResponseOk(res)
    repdict = json.loads(res.body)
    assert repdict[0].get('id') != None

def test_Person():
    cust_dict = getAllNounsTest('customer')
    cust = cust_dict[0].get('id')
    cust1 = cust_dict[1].get('id')
    noun = 'person'
    noun_dict = dict(title= 'aTitle', name = 'aName', email='anEmail',
            mobile = '9590952331', customer=cust)
    members = ['title', 'name', 'email', 'mobile', 'customer']
    up_dict = dict(title= 'theTitle', name = 'theName', email='theEmail',
            mobile = '9849098490', customer=cust1)
    testNounCrudExt(noun, noun_dict, up_dict,members)
    #============================================
    res = ap.get('/personByCustomer/%s' %cust1)
    assertResponseOk(res)
    repdict = json.loads(res.body)
    assert repdict.get('id') != None

def test_Address():
    cust_dict = getAllNounsTest('customer')
    cust = cust_dict[0].get('id')
    cust1 = cust_dict[1].get('id')
    noun = 'address'
    noun_dict = dict(customer=cust,address_type=1,address='anAddress',
            zipcode='560041',city='brussels',tel='9834552',fax='e435232232',
            email='anEmailId')
    up_dict = dict(customer=cust1,address_type=2,address='theAddress',
            zipcode='960041',city='antwerp',tel='004834552',fax='p435232232',
            email='theEmailId')
    members = ['customer','address_type','address','zipcode','city','tel','fax','email']
    testNounCrudExt(noun,noun_dict,up_dict,members)

def test_Article():
    artType_dict = getAllNounsTest('articleType')
    artType1 = artType_dict[0].get('id')
    artType2 = artType_dict[1].get('id')
    unitType_dict = getAllNounsTest('unit')
    unit1 = unitType_dict[0].get('id')
    unit2 = unitType_dict[1].get('id')
    suppType_dict = getAllNounsTest('supplier')
    supp1 = suppType_dict[0].get('id')
    supp2 = suppType_dict[1].get('id')
    userType_dict = getAllNounsTest('user')
    user1 = userType_dict[0].get('id')
    user2 = userType_dict[1].get('id')
    noun = 'article'
    noun_dict = dict(code='aCode',name='aName',description='aDescription',
            listPrice='54',weight=54,create_date='11/11/2011',vat='32',
            article_type=artType1,unit=unit1,creator=user1,supplier=supp1)
    members = ['code','name','description','listPrice','weight','create_date',
            'vat', 'article_type','unit','creator','supplier']
    up_dict = dict(code='theCode',name='theName',description='theDescription',
            listPrice='45',weight=42,create_date='11/11/2012',vat='23',
            article_type=artType2,unit=unit2,creator=user2,supplier=supp2)
    testNounCrudExt(noun,noun_dict,up_dict,members)
    #============================================
    res = ap.get('/articleBySupplier/%s' %supp2)
    assertResponseOk(res)
    repdict = json.loads(res.body)
    assert repdict[0].get('id') != None

def test_Stock():
    articles_dict = getAllNounsTest('article')
    article1 = articles_dict[0].get('id')
    article2 = articles_dict[1].get('id')
    noun = 'stock'
    noun_dict = dict(article=article1,quantity='33')
    members = ['article', 'quantity']
    up_dict = dict(article=article2,quantity='55')
    testNounCrudExt(noun,noun_dict,up_dict,members)

def test_Invoice():
    cust_dict = getAllNounsTest('customer')
    cust1 = cust_dict[0].get('id')
    cust2 = cust_dict[1].get('id')
    add_dict = getAllNounsTest('address')
    add1 = add_dict[0].get('id')
    add2 = add_dict[1].get('id')
    user_dict = getAllNounsTest('user')
    user1 = user_dict[0].get('id')
    user2 = user_dict[1].get('id')
    noun = 'invoice'
    noun_dict = dict(customer=cust1,inv_address=add1,del_address=add2,code='aCode',
            remark='aRemark',shipping=45.43,total=52.38,vat=1432,
            creation_date='31/12/2010',delivery_date='08/01/2011',paid_date='01/01/2011',
            weight=1.34,status=1,creator=user1)
    members = ['customer','inv_address','del_address','code','remark','shipping','total',
            'vat','creation_date','delivery_date','paid_date','weight',
            'status','creator']
    up_dict = dict(customer=cust2,inv_address=add2,del_address=add1,code='theCode',
            remark='theRemark',shipping=5.43,total=152.38,vat=14.32,
            creation_date='01/01/2011',delivery_date='31/01/2011',paid_date='02/01/2011',
            weight=5.34,status=2,creator=user2)
    testNounCrudExt(noun,noun_dict,up_dict,members)

def test_InvoiceLine():
    art_dict = getAllNounsTest('article')
    article1 = art_dict[0].get('id')
    article2 = art_dict[1].get('id')
    inv_dict = getAllNounsTest('invoice')
    invoice1 = inv_dict[0].get('id')
    invoice2 = inv_dict[1].get('id')
    noun = 'invoiceLine'
    noun_dict = dict(article=article1,quantity=41,unit_price=21.21,
            discount=35.23,unit_discount=87.32,invoice=invoice1)
    members = ['article','quantity','unit_price','discount','unit_discount','invoice']
    up_dict = dict(article=article2,quantity=14,unit_price=81.21,
            discount=55.23,unit_discount=8.32,invoice=invoice2)
    testNounCrudExt(noun,noun_dict,up_dict,members)
    #============================================
    res = ap.get('/invoiceLineByInvoice/%s' %invoice2)
    assertResponseOk(res)
    repdict = json.loads(res.body)
    assert repdict[0].get('id') != None

def testNounCrud(noun,noun_dict,up_dict,members):
    addNounTest(noun,noun_dict)
    type_dict = getAllNounsTest(noun)
    resp_dict = getNounTest(noun,type_dict, members)
    updateSimpleNounTest(noun,resp_dict,up_dict)

def testNounCrudExt(noun,noun_dict,up_dict,members):
    addNounTest(noun,noun_dict)
    type_dict = getAllNounsTest(noun)
    resp_dict = getNounTestExt(noun,type_dict, members)
    updateSimpleNounTest(noun,resp_dict,up_dict)

def addNounTest(noun,noun_dict):
    res = ap.post('/'+noun,json.dumps(noun_dict))
    assertResponseOk(res)

def getAllNounsTest(noun):
    res = ap.get('/'+noun+'s')
    assertResponseOk(res)
    type_dict = json.loads(res.body)
    return type_dict

def updateSimpleNounTest(noun,resp_dict,up_dict):
    ret_id = resp_dict.get('id')
    res = ap.post('/'+noun+'/%s' %ret_id, json.dumps(up_dict))
    assertResponseOk(res)


def getNounTest(noun,type_dict,members):
    ret_id = type_dict[0].get('id')
    res = ap.get('/'+noun+'/%s' %ret_id)
    assertResponseOk(res)
    resp_dict = json.loads(res.body)
    assert ret_id == resp_dict.get('id')
    for m in members:
        assert type_dict[0].get(m) == resp_dict.get(m)
    return resp_dict


def getNounTestExt(noun,type_dict,members):
    ret_id = type_dict[0].get('id')
    res = ap.get('/'+noun+'/%s' %ret_id)
    assertResponseOk(res)
    resp_dict = json.loads(res.body)
    assert ret_id == resp_dict.get('id')
    for m in members:
        res = ap.get('/'+noun+'/%s' %ret_id)
        type_dict = json.loads(res.body)
        assert type_dict.get(m) == resp_dict.get(m)
    return resp_dict

def assertResponseOk(res):
    assert res.status == '200 OK'

def assertNotNone(a,b):
    assert a.get(b) != None

def assertNone(a,b):
    assert a.get(b) == None
test_hello_world()
get_users()
get_users()
test_ArticleType()
test_ArticleType()
test_Unit()
test_Unit()
test_Supplier()
test_Supplier()
test_Sector()
test_Sector()
test_Customer()
test_Customer()
test_Person()
test_Address()
test_Address()
test_Article()
test_Article()
test_Stock()
test_Invoice()
test_Invoice()
test_InvoiceLine()
