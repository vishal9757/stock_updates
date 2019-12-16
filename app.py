import cherrypy
import webbrowser
import os
import simplejson
import sys
import json
import config
import service

APP_HOST = os.environ['APP_HOST']
APP_PORT = int(os.environ['APP_PORT'])


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
        print (companyName)
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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def last_updated_date(self):
        """
        Endpoint to get last date when file is processed
        """
        resp = service.get_last_updated_date()
        return resp


def main():
    """
    Main function to load config of application
    """
   # configuration file

    conf = config.APPLICATION_CONFIG
    cherrypy.config.update({'server.socket_host': APP_HOST,
                            'server.socket_port': APP_PORT,
                            })
    cherrypy.quickstart(Stock(), config=conf)


if __name__ == '__main__':
    main()
