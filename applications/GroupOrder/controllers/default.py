# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if len(request.args): page=int(request.args[0])
    else: page = 0
    items_per_page=19
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    myorder = db.bulletinboards.Created_On
    board_list = db(db.bulletinboards.Board_Title > 0).select(orderby=~myorder, limitby=limitby)
    form = SQLFORM(db.bulletinboards)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    postsdblist = db(db.posts.Post_Title > 0).select()
    return dict(board_list=board_list, form=form, postsdblist=postsdblist, page=page,items_per_page=items_per_page)

def reset():
  db(db.bulletinboards.id> 0).delete()
  db(db.posts.id>0).delete()
  return

@auth.requires_signature()
def load_messages():
    """Loads all messages for the user."""
    myorder = db.bulletinboards.Created_On
    rows = db(db.bulletinboards.Board_Title > 0).select(orderby=~myorder)
    d = {r.id: {'Board_Title': r.Board_Title,
                'Board_id': r.id}
         for r in rows}
    return response.json(dict(board_list=d))






def loadGroup():
    """Loads all messages for the user."""
    rows = db(db.Groups.id > 0).select()
    d = {r.id: {'groupName': r.groupName,
                'groupId': r.id}
         for r in rows}
    return response.json(dict(groupList=d))


@auth.requires_signature()
def createGroup():
    db.Groups.insert(groupName = request.vars.groupName)
    rows = db(db.Groups.id > 0).select()
    d = {r.id: {'groupName': r.groupName,
                'groupId': r.id}
         for r in rows}
    return response.json(dict(groupList=d))

def groupOrders():

    return dict()




@auth.requires_signature()
def add_msg():
    db.bulletinboards.update_or_insert((db.bulletinboards.id == request.vars.Board_id),
        Board_Title= request.vars.Board_Title,
        )
    return "ok"





@auth.requires_signature()
def new_board():
    myorder = db.bulletinboards.Created_On
    db.bulletinboards.insert(Board_Title = request.vars.Board_Title )
    rows = db(db.bulletinboards.Board_Title > 0).select(orderby=~myorder)
    d = {r.id: {'Board_Title': r.Board_Title,
                'Board_id': r.id}
         for r in rows}
    return response.json(dict(board_list=d))






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


def my_form_processing(form):
    boardid = db.bulletinboards(request.args(0))
    if form.vars.Category != boardid.id:
       form.vars.Category = boardid.id
    else:
       form.vars.Category = boardid.id

def post():
    if len(request.args) > 1: page=int(request.args[1])
    else: page=0
    items_per_page=19
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    boardid = db.bulletinboards(request.args(0))
    usefulid = request.args(0)
    myorder = db.posts.Created_On
    post_form = SQLFORM(db.posts)
    author = auth.user_id

    if post_form.process(onvalidation=my_form_processing).accepted:
        db(db.bulletinboards.id == boardid.id).update(Created_On = datetime.utcnow())
        redirect(URL('default', 'post', args=[boardid.id]))
    return dict(post_form=post_form, boardid=boardid, author=author, usefulid=usefulid, myorder=myorder, limitby=limitby,page=page,items_per_page=items_per_page)


@auth.requires_signature()
def load_posts():
    """Loads all messages for the user."""
    rows = db(db.posts.Category == request.vars.boardid).select()
    d = {r.id: {'Post_Title': r.Post_Title,
                'Post_id': r.id,
                'author': r.author,
                'Post_Description': r.Post_Description,
                'Category': r.Category}
         for r in rows}
    return response.json(dict(post_list=d))



@auth.requires_signature()
def save_post():
    db.posts.update_or_insert((db.posts.id == request.vars.Post_id),
        Post_Title = request.vars.Post_Title,
        Post_Description = request.vars.Post_Description,
        )
    return "ok"

@auth.requires_signature()
def delete_post():
    db(db.posts.id == request.vars.Post_id).delete()
    return "ok"


@auth.requires_signature()
def new_post():
    db.posts.insert(Post_Title = request.vars.Post_Title,
                    Post_Description = request.vars.Post_Description,
                    author = request.vars.author,
                    Category = request.vars.Category)
    rows = db(db.posts.Category == request.vars.Category).select()
    d = {r.id: {'Post_Title': r.Post_Title,
                'Post_id': r.id,
                'Post_Description': r.Post_Description,
                'Category': r.Category,
                'author': r.author}
         for r in rows}
    return response.json(dict(post_list=d))








def edit():
    record = db.posts(request.args(1))
    edit_form = SQLFORM(db.posts, record, showid=False)
    anthoerdid = request.args(0)
    if edit_form.process(onvalidation=my_form_processing).accepted:
        response.flash = 'edit success'
        redirect(URL('default','post', args=[anthoerdid, 0]))
    elif edit_form.errors:
        response.flash = 'edit failure'
    return dict(edit_form=edit_form)

@auth.requires_signature()
def delete():
    post_id = request.args(1)
    board_id = request.args(0)
    db(db.posts.id == post_id).delete()
    redirect(URL('default', 'post', args=[board_id]))
    return