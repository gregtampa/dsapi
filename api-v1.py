from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from sqlalchemy import create_engine

db = create_engine('sqlite:///servers.db')

app = Flask(__name__)
api = Api(app)

class ServerList(Resource):
	def get(self):
		conn = db.connect()
		query = conn.execute("select server,port,type from servers")
		return {'servers': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Server(Resource):
	def get(self, servername):
		conn = db.connect()
		query = conn.execute("select * from servers where server='%s'" % servername.lower())
		result = {'server': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result

api.add_resource(ServerList, '/v1', '/v1/')
api.add_resource(Server, '/v1/<string:servername>','/v1/<string:servername>/')

if __name__ == '__main__':
	app.run(debug=True)