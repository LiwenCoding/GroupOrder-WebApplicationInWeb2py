


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
    group_access_id = auth.add_group('general', request.vars.groupName)
    db.Groups.insert(groupName = request.vars.groupName,
                     groupCreator = request.vars.groupCreator,
                     groupAccessId=group_access_id)
    auth.add_membership(group_access_id, auth.user_id)
    logger.info(group_access_id)
    logger.info(auth.user_group(auth.user_id))

    rows = db(db.Groups.id > 0).select()
    d = {r.id: {'groupName': r.groupName,
                'groupId': r.id}
         for r in rows}
    return response.json(dict(groupList=d))



@auth.requires_login()
def groupOrders():
    groupId = request.args[0]
    group_entry = db(db.Groups.id == groupId).select()
    group_access_id= group_entry[0].groupAccessId
    logger.info(group_access_id)
    if not (auth.has_membership(group_access_id, auth.user_id, 'general') or auth.has_membership(group_access_id, auth.user_id, 'admin')):
        # redirect(URL('default', 'requestGroupMembership', args=[groupId, group_access_id]))
        session.flash = T("Authorization required")
        redirect(URL('default', 'index'))
    return dict(groupId=groupId,)


@auth.requires_signature()
def loadMenuOrderList():
    menu_rows = db(db.Menus.groupId == request.vars.groupId).select()
    menu_d = {r.id: {'menuName': r.menuName,
                'menuId': r.id}
         for r in menu_rows}

    order_rows = db(db.GroupOrders.groupId == request.vars.groupId).select()
    order_d = {r.id: {'groupOrderDeadline': r.groupOrderDeadline,
                      'menuId': r.menuId,
                      'creatorFirstName': r.creatorFirstName,
                      'menuName': r.menuName,
                      'groupOrderId': r.id,
                      }
               for r in order_rows}
    return response.json(dict(displayMenu=menu_d, displayOrder=order_d))


@auth.requires_signature()
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


@auth.requires_signature()
def getMenuDetail():
    # testEntry = db(db.MenuDetails.menuId == request.vars.menuId).select()
    # logger.info(testEntry[1].itemName == "")
    rows = db((db.MenuDetails.menuId == request.vars.menuId) & (db.MenuDetails.itemName != "") & (db.MenuDetails.itemPrice != "")).select()
    d = {r.id: {'itemName': r.itemName,
                'itemPrice': r.itemPrice,
                'itemId': r.id}
         for r in rows}
    return response.json(dict(displayMenuDetail=d))


@auth.requires_signature()
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
                      'creatorFirstName': r.creatorFirstName,
                      'menuName': r.menuName,
                      'groupOrderId': r.id,
                      }
               for r in order_rows}
    return response.json(dict(displayOrder=order_d))


def resetOrder():
    db(db.GroupOrders.id> 0).delete()
    return

def resetSingleOrder():
    db(db.SingleOrders.id > 0).delete()


def singleOrders():
    menuId = request.args[0]
    groupOrderId = request.args[1]
    deadline = db(db.GroupOrders.id == groupOrderId).select().first().groupOrderDeadline
    groupOrderCreator=db(db.GroupOrders.id == groupOrderId).select().first().groupOrderCreator
    logger.info(deadline)
    return dict(menuId=menuId, groupOrderId=groupOrderId, deadline=deadline, groupOrderCreator=groupOrderCreator)


def addSingleOrders():
    logger.info(request.vars.itemName)
    logger.info(request.vars.itemQuantity)
    logger.info(request.vars.itemPrice)
    logger.info(request.vars.groupOrderId)
    itemArr = request.vars.itemName.split(';')
    priceArr = request.vars.itemPrice.split(';')
    quantity_arr = request.vars.itemQuantity.split(';')

    if request.vars.itemName is not None:
        for i, val in enumerate(itemArr):
            logger.info(val)
            db.SingleOrders.insert(singleOrderCreator=request.vars.singleOrderCreator,
                                   status=request.vars.status,
                                   groupOrderId=request.vars.groupOrderId,
                                   itemName=itemArr[i],
                                   itemPrice=priceArr[i],
                                   itemQuantity=quantity_arr[i])

    order_rows = db(db.SingleOrders.groupOrderId==request.vars.groupOrderId).select()
    d = {r.id: {'creatorId': r.singleOrderCreator,
                'creatorFirstName': r.singleOrderCreator.first_name,
                'itemName': r.itemName,
                'itemPrice': r.itemPrice,
                'itemQuantity': r.itemQuantity,
                'status': r.status,
                'groupOrderId': r.id,
                }
               for r in order_rows}
    return response.json(dict(displayOrderDetail=d))



def getOrderDetail():

    order_rows = db(db.SingleOrders.groupOrderId == request.vars.groupOrderId).select()
    d = {r.id: {'creatorId': r.singleOrderCreator,
                'creatorFirstName': r.singleOrderCreator.first_name,
                'itemName': r.itemName,
                'itemPrice': r.itemPrice,
                'itemQuantity': r.itemQuantity,
                'status': r.status,
                'groupOrderId': r.id,
                }
               for r in order_rows}
    return response.json(dict(displayOrderDetail=d))


@auth.requires_signature()
def deleteSingleOrder():
    db(db.SingleOrders.id == request.vars.singleOrderId).delete()
    d = getSingleOrderDict(request.vars.groupOrderId)
    return response.json(dict(displayOrderDetail=d))
    # order_rows = db(db.SingleOrders.groupOrderId == request.vars.groupOrderId).select()
    # d = {r.id: {'creatorId': r.singleOrderCreator,
    #             'creatorFirstName': r.singleOrderCreator.first_name,
    #             'itemName': r.itemName,
    #             'itemPrice': r.itemPrice,
    #             'itemQuantity': r.itemQuantity,
    #             'status': r.status,
    #             'groupOrderId': r.id,
    #             }
    #            for r in order_rows}
    # return response.json(dict(displayOrderDetail=d))


def confirmSingleOrder():
    logger.info(request.vars.singleOrderId + "requesting for success")
    db(db.SingleOrders.id == request.vars.singleOrderId).update(status="success")
    d = getSingleOrderDict(request.vars.groupOrderId)
    return response.json(dict(displayOrderDetail=d))


def cancelSingleOrder():
    logger.info(request.vars.singleOrderId + "requesting for success")
    db(db.SingleOrders.id == request.vars.singleOrderId).update(status="failure")
    d = getSingleOrderDict(request.vars.groupOrderId)
    return response.json(dict(displayOrderDetail=d))



def getSingleOrderDict(groupId):
    order_rows = db(db.SingleOrders.groupOrderId == groupId).select()
    # db.SingleOrders.ALL, orderby=db.SingleOrders.creatorId
    d = {r.id: {'creatorId': r.singleOrderCreator,
                'creatorFirstName': r.singleOrderCreator.first_name,
                'itemName': r.itemName,
                'itemPrice': r.itemPrice,
                'itemQuantity': r.itemQuantity,
                'status': r.status,
                'groupOrderId': r.id,
                }
               for r in order_rows}
    return d


@auth.requires_signature()
def resetRequest():
    db(db.JoinGroupRequest.id > 0).delete()
    return


@auth.requires_login()
def sendRequest():
    groupId = request.vars.groupId
    logger.info("request for " + groupId)
    logger.info(auth.user_id)
    requestTableEntry = db((db.JoinGroupRequest.applicantId == auth.user_id) & (db.JoinGroupRequest.groupId == groupId)).select().first()
    logger.info(requestTableEntry)
    if requestTableEntry is not None:
        logger.info("request already made!")
        return response.json(dict(insert=False))
    group_entry = db(db.Groups.id == groupId).select()
    group_access_id = group_entry[0].groupAccessId
    group_creator_id = group_entry[0].groupCreator
    group_name = group_entry[0].groupName
    if group_creator_id == auth.user_id:
        logger.info("requester is creator!")
        return response.json(dict(insert=False))

    requester_name = db(db.auth_user.id == auth.user_id).select(db.auth_user.first_name)[0].first_name
    creator_name = db(db.auth_user.id == group_creator_id).select(db.auth_user.first_name)[0].first_name

    logger.info("requester name: " + requester_name)
    logger.info("creator name: " + creator_name)
    logger.info("group name: " + group_name)

    db.JoinGroupRequest.insert(applicantId=auth.user_id,
                               applicantName=requester_name,
                               groupId=groupId,
                               groupName=group_name,
                               groupAccessId=group_access_id,
                               groupCreatorId=group_creator_id,
                               groupCreatorName=creator_name,
                               status='pending')
    return response.json(dict(insert=True))


@auth.requires_login()
def manage():
    logger.info("in manage page")
    # auth.user_id
    return dict()


@auth.requires_signature()
def loadRequest():
    rows_control = db(db.JoinGroupRequest.groupCreatorId == auth.user_id).select()
    d_control = {r.id: {'groupName': r.groupName,
                        'groupId': r.groupId,
                        'groupAccessId': r.groupAccessId,
                        'groupCreatorId': r.groupCreatorId,
                        'groupCreatorName': r.groupCreatorName,
                        'applicantId': r.applicantId,
                        'applicantName': r.applicantName,
                        'status': r.status
                        }
                 for r in rows_control}
    logger.info(len(d_control))

    rows_request = db(db.JoinGroupRequest.applicantId == auth.user_id).select()
    d_request = {r.id: {'groupName': r.groupName,
                        'groupId': r.groupId,
                        'groupAccessId': r.groupAccessId,
                        'groupCreatorId': r.groupCreatorId,
                        'groupCreatorName': r.groupCreatorName,
                        'applicantId': r.applicantId,
                        'applicantName': r.applicantName,
                        'status': r.status
                        }
                 for r in rows_request}
    return response.json(dict(controlList=d_control, requestList=d_request))


@auth.requires_signature()
def approveRequest():
    request_id = request.vars.requestId
    request_entry = db(db.JoinGroupRequest.id == request_id).select().first()
    # logger.info(request_entry.applicantName)
    # logger.info(request_entry.groupName)
    auth.add_membership(request_entry.groupAccessId, request_entry.applicantId)
    db(db.JoinGroupRequest.id == request_id).update(status="approved")

    rows_control = db(db.JoinGroupRequest.groupCreatorId == auth.user_id).select()
    d_control = {r.id: {'groupName': r.groupName,
                        'groupId': r.groupId,
                        'groupAccessId': r.groupAccessId,
                        'groupCreatorId': r.groupCreatorId,
                        'groupCreatorName': r.groupCreatorName,
                        'applicantId': r.applicantId,
                        'applicantName': r.applicantName,
                        'status': r.status
                        }
                 for r in rows_control}
    return response.json(dict(controlList=d_control))


@auth.requires_signature()
def rejectRequest():
    request_id = request.vars.requestId
    db(db.JoinGroupRequest.id == request_id).update(status="rejected")
    rows_control = db(db.JoinGroupRequest.groupCreatorId == auth.user_id).select()
    d_control = {r.id: {'groupName': r.groupName,
                        'groupId': r.groupId,
                        'groupAccessId': r.groupAccessId,
                        'groupCreatorId': r.groupCreatorId,
                        'groupCreatorName': r.groupCreatorName,
                        'applicantId': r.applicantId,
                        'applicantName': r.applicantName,
                        'status': r.status
                        }
                 for r in rows_control}
    return response.json(dict(controlList=d_control))



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

