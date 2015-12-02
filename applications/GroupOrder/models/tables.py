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
                Field('dishName'),
                Field('dishPrice'),
                Field('menuId', db.Menus))

db.define_table('GroupOrders',
                Field('groupOrderCreator', db.auth_user),
                Field('groupOrderDeadline'),
                Field('menuId', db.Menus))

db.define_table('SingleOrder',
                Field('singleOrderCreator', db.auth_user),
                Field('orderId', db.GroupOrders),
                Field('orderList'),
                Field('orderQuantity'),
                Field('orderPrice'))







db.define_table('bulletinboards',
                Field('Board_Title'),
                Field('Created_On', 'datetime'),
                )
db.bulletinboards.Created_On.default = datetime.utcnow()
db.define_table('posts',
                Field('author', db.auth_user),
                Field('Post_Title', 'string'),
                Field('Post_Description', 'text'),
                Field('Created_On', 'datetime'),
                Field('Category', db.bulletinboards))
db.posts.author.readable = db.posts.author.writable = False
db.posts.Created_On.readable = db.posts.Created_On.writable = False
db.posts.Created_On.default = datetime.utcnow()
now = datetime.utcnow()
yesterday = now - timedelta(days=1)

