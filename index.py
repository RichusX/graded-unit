#!/usr/bin/python
import web
import updateTables
import hashlib

web.config.debug = False

urls = (
    '/', 'index',
    '/favicon.ico','icon',
    '/tables', 'league_tables',
    '/stats', 'player_statistics',
    '/login', 'login',
    '/logout', 'logout'
)
globalVars = {'subscriber': False}

app = web.application(urls, locals())
db = web.database(host='localhost', dbn='mysql', db='sportsleague', user='sportsleague', pw='FH9Y9iaVZuBRmYoF')

store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})

#-------------------- PAGE CLASSES --------------------

class index:
    def __init__(self):
        self.render = web.template.render('templates/', base='layout', globals=globalVars)
    def GET(self):
        return self.render.index()

class league_tables:
    def __init__(self):
        self.render = web.template.render('templates/', base='layout', globals=globalVars)
    def GET(self):
        #updateTables.getTables()
        return self.render.tables()

class player_statistics:
    def __init__(self):
        self.render = web.template.render('templates/', base='layout', globals=globalVars)
    def GET(self):
        return self.render.stats()

class icon:
    def GET(self):
        raise web.seeother("/static/images/favicon.ico")

class login:
    def GET(self):
        if logged():
            render = create_render(session.privilege)
            return '%s' % render.index()
        else:
            render = create_render(session.privilege)
            return '%s' % render.login()
    def POST(self):
        username, passwd = web.input().username, web.input().passwd
        try:
            ident = db.select('users', where='user=$username', vars=locals())[0]
            if hashlib.sha1(passwd).hexdigest() == ident['pass']:
                session.login = 1
                session.privilege = ident['privilege']
                render = create_render(session.privilege)
                return render.login_ok()
            else:
                session.login = 0
                session.privilege = 0
                render = create_render(session.privilege)
                return render.login_error()
        except:
            session.login = 0
            session.privilege = 0
            render = create_render(session.privilege)
            return render.login_error()

class logout:
    def GET(self):
        session.login = 0
        session.kill()
        render = create_render(session.privilege)
        return render.index()
#------------------------------------------------------

def logged():
        if session.login==1:
            return True
        else:
            return False

def create_render(privilege):
        if logged():
            if privilege == 0:
                render = web.template.render('templates/', base='layout')
            elif privilege == 1:
                render = web.template.render('templates/', base='layout')
            elif privilege == 2:
                render = web.template.render('templates/', base='layout')
            else:
                render = web.template.render('templates/', base='layout')
        else:
            render = web.template.render('templates', base='layout')
        return render

if __name__ == "__main__":
    app.run()
