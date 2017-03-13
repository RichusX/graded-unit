#!/usr/bin/python
import web
import updateTables

urls = (
    '/', 'index',
    '/favicon.ico','icon',
    '/tables', 'league_tables',
    '/stats', 'player_statistics',
    '/login', 'login',
    '/logout', 'logout'
)
globalVars = {'subscriber': True}

class index:
    def __init__(self):
        self.render = web.template.render('templates/', base='layout', globals=globalVars)
    def GET(self):
        listtest = ['I like potatoes', 'He likes potatoes', 'Everyone likes potatoes']
        return self.render.index(listtest)

class league_tables:
    def __init__(self):
        self.render = web.template.render('templates/', base='layout', globals=globalVars)
    def GET(self):
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
        globalVars['subscriber'] = True
        raise web.seeother("/")

class logout:
    def GET(self):
        globalVars['subscriber'] = False
        raise web.seeother("/")

if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.degub = True
    app.run()
