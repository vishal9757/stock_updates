import cherrypy
import service

class Stock(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def company_suggestions(self, text):
        result = service.get_company_suggestions(text)
        return {"companies": result}
if __name__ == '__main__':
    cherrypy.quickstart(Stock())