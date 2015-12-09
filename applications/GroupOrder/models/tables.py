#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
from datetime import datetime,timedelta

db.define_table('Groups',
                Field('groupName'),
                Field('groupCreator', db.auth_user))

db.define_table('Menus',
                Field('menuName'),
                Field('menuCreator', db.auth_user),
                Field('groupId', db.Groups))

db.define_table('MenuDetails',
                Field('itemName'),
                Field('itemPrice'),
                Field('menuId', db.Menus))

db.define_table('GroupOrders',
                Field('groupOrderCreator', db.auth_user),
                Field('creatorFirstName'),
                Field('creatorLastName'),
                Field('groupOrderDeadline'),
                Field('menuId', db.Menus),
                Field('menuName'),
                Field('groupId', db.Groups))

db.define_table('SingleOrders',
                Field('singleOrderCreator', db.auth_user),
                Field('orderId', db.GroupOrders),
                Field('itemId'),
                Field('itemQuantity'),
                Field('orderPrice'),
                Field('status', requires=IS_IN_SET('pending', 'success', 'failure')))



