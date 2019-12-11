import cherrypy
import webbrowser
import os
import simplejson
import sys
import json

import service

class Stock(object):
    @cherrypy.expose
    def index(self, companyName=None):
        return open("media/index.html")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def company_suggestions(self, text):
        result = service.get_company_suggestions(text)
        return {"companies": result}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def company_stats(self, companyName):
        response = service.get_company_stats(companyName)
        return response

def main():
   # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
    })

    conf = {"/media": {"tools.staticdir.on": True,
                       "tools.staticdir.dir": os.path.abspath("media"),
                       }
            }
    cherrypy.quickstart(Stock(), config=conf)


if __name__ == '__main__':
    main()
