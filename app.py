import cherrypy
import webbrowser
import os
import simplejson
import sys
import json
import config

import service

class Stock(object):
    @cherrypy.expose
    def index(self):
        """
        Endpoint for index page of application
        """
        return open("media/index.html")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def company_suggestions(self, text):
        """
        Endpoint to get company suggestions
        """
        result = service.get_company_suggestions(text)
        return {"companies": result}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def company_stats(self, companyName):
        """
        Endpoint to get company stats
        """
        response = service.get_company_stats(companyName)
        return response
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sorted_company(self, sort):
        """
        Endpoint to get sorted company based on given key
        """
        resp = service.get_sorted_company(sort)
        return resp

def main():
    """
    Main function to load config of application
    """
   # configuration file

    conf = config.APPLICATION_CONFIG
    cherrypy.quickstart(Stock(), config=conf)


if __name__ == '__main__':
    main()
