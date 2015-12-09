


def index():
    return dict()



def reset():
  db(db.Menus.id> 0).delete()
  db(db.MenuDetails.id>0).delete()
  db(db.Groups.id>0).delete()
  return



def loadGroup():
    rows = db(db.Groups.id > 0).select()
    d = {r.id: {'groupName': r.groupName,
                'groupId': r.id}
         for r in rows}
    return response.json(dict(groupList=d))


@auth.requires_signature()
def createGroup():
    db.Groups.insert(groupName = request.vars.groupName,
                     groupCreator = request.vars.groupCreator)
    rows = db(db.Groups.id > 0).select()
    d = {r.id: {'groupName': r.groupName,
                'groupId': r.id}
         for r in rows}
    return response.json(dict(groupList=d))




def groupOrders():
    groupId = request.args[0]
    return dict(groupId=groupId)


def loadMenuOrderList():
    menu_rows = db(db.Menus.groupId == request.vars.groupId).select()
    menu_d = {r.id: {'menuName': r.menuName,
                'menuId': r.id}
         for r in menu_rows}

    order_rows = db(db.GroupOrders.groupId==request.vars.groupId).select()
    order_d = {r.id: {'groupOrderDeadline': r.groupOrderDeadline,
                      'menuId': r.menuId,
                      'creatorFirstName': r.creatorLastName,
                      'menuName': r.menuName,
                      'groupOrderId': r.id,
                      }
               for r in order_rows}
    return response.json(dict(displayMenu=menu_d, displayOrder=order_d))



def addMenuList():

    # menuList = json.load(request.vars.menuList)

    db.Menus.insert(menuName = request.vars.menuName,
                    menuCreator = request.vars.menuCreator,
                    groupId = request.vars.groupId)

    rows = db(db.Menus.id > 0).select()
    thisMenu = rows.last()

    db.MenuDetails.insert(itemName = request.vars.item1,
                          itemPrice = request.vars.price1,
                           menuId = thisMenu.id)

    db.MenuDetails.insert(itemName = request.vars.item2,
                      itemPrice = request.vars.price2,
                     menuId = thisMenu.id)

    db.MenuDetails.insert(itemName=request.vars.item3,
                      itemPrice=request.vars.price3,
                      menuId=thisMenu.id)

    rows = db(db.Menus.groupId == request.vars.groupId).select()

    d = {r.id: {'menuName': r.menuName,

                'menuId': r.id}
         for r in rows}
    return response.json(dict(displayMenu=d))


def getMenuDetail():
    rows = db(db.MenuDetails.menuId == request.vars.menuId).select()
    d = {r.id: {'itemName': r.itemName,
                'itemPrice': r.itemPrice,
                'itemId': r.id}
         for r in rows}
    return response.json(dict(displayMenuDetail=d))



def addOrder():
    creatorFirsts = db(db.auth_user.id == auth.user_id).select()
    creatorLasts = db(db.auth_user.id == auth.user_id).select()
    menuNames = db(db.Menus.id == request.vars.menuId).select()
    creatorFirst = creatorFirsts[0].first_name
    creatorLast = creatorLasts[0].last_name
    menuName = menuNames[0].menuName
    db.GroupOrders.insert(groupOrderCreator=auth.user_id,
                          creatorFirstName=creatorFirst,
                          creatorLastName=creatorLast,
                          groupOrderDeadline=request.vars.deadline,
                          menuId=request.vars.menuId,
                          menuName=menuName,
                          groupId=request.vars.groupId)

    order_rows = db(db.GroupOrders.groupId==request.vars.groupId).select()
    order_d = {r.id: {'groupOrderDeadline': r.groupOrderDeadline,
                      'menuId': r.menuId,
                      'creatorFirstName': r.creatorLastName,
                      'menuName': r.menuName,
                      'groupOrderId': r.id,
                      }
               for r in order_rows}
    return response.json(dict(displayOrder=order_d))



def resetOrder():
    db(db.GroupOrders.id> 0).delete()
    return


def singleOrders():
    menuId = request.args[0]
    groupOrderId = request.args[1]
    return dict(menuId=menuId,groupOrderId=groupOrderId)


def addSingleOrders():

    db.SingleOrders.insert(singleOrderCreator = request.vars.singleOrderCreator,
                           status = request.vars.status,
                           groupOrderId = request.vars.groupOrderId,
                           itemName = request.vars.itemName1,
                           itemPrice = request.vars.itemPrice1,
                           itemQuantity = request.vars.itemQuantity1)

    db.SingleOrders.insert(singleOrderCreator = request.vars.singleOrderCreator,
                       status = request.vars.status,
                       groupOrderId = request.vars.groupOrderId,
                       itemName = request.vars.itemName2,
                       itemPrice = request.vars.itemPrice2,
                       itemQuantity = request.vars.itemQuantity2)

    db.SingleOrders.insert(singleOrderCreator = request.vars.singleOrderCreator,
                       status = request.vars.status,
                       groupOrderId = request.vars.groupOrderId,
                       itemName = request.vars.itemName3,
                       itemPrice = request.vars.itemPrice3,
                       itemQuantity = request.vars.itemQuantity3)

    return "ok"








def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

