import xmlrpc.client


# info = xmlrpc.client.ServerProxy('http://localhost:8069/start').start()
# url, db, username, password = info['host'], info['database'], info['user'], info['password']

# print ("\n\ninfo is ::: ", url, db, username, password)

db = "odoo15"
username = "pra"
password = "1"

common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print ("Connection Successful")

models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')


#create records
#value=models.execute_kw(db, uid, password, 'estate.property.tag', 'create', [{'name':'new'}])
print("Successful",value)



#search  records
#to_confrim_ids = models.execute_kw(db, uid, password, 'estate.properties', 'search', [[('name', '=', 'Apartment')]])
# result = models.execute_kw(db, uid, password, 'estate.properties', 'write', [1, {'name':'east'}])
#print ("\n\n value::: ", value)
#print ("\n\n conformid::: ",to_confrim_ids)

## Unlink Record
# results = models.execute_kw(db, uid, password, 'estate.properties', 'unlink', [result])
#result = models.execute_kw(db, uid, password, 'estate.properties', 'unlink', [to_confrim_ids])
#print ("\n\n value::: ",result)