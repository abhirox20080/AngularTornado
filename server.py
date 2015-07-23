import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
from bson import json_util, ObjectId
import json
from pymongo import MongoClient


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
class DbHandler(tornado.web.RequestHandler):
    def get(self):
        client = MongoClient('localhost', 27017)
        db = client['mydb']
        collection = db['mycollection']
        data=collection.find_one()
        print "Fetching data"
        x = json.loads(json_util.dumps(data))
        print type(x)
        self.write(x)

        
application = tornado.web.Application(handlers=[
  (r'/', MainHandler),
  (r'/db', DbHandler),  
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),],
  template_path=os.path.join(os.path.dirname(__file__), "templates"),
  static_path=os.path.join(os.path.dirname(__file__), "app/static"),
  #images=os.path.join(os.path.dirname(__file__), "images"),
  debug=True)

#added images to test

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(9292)
  print "The Tornado server started on port 9292"
  #application.listen(9090)#, address='192.168.1.38')
  tornado.ioloop.IOLoop.instance().start()
