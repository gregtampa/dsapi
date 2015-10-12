# https://flask-basicauth.readthedocs.org/en/latest/
# https://flask-restful.readthedocs.org/en/latest/index.html
# https://github.com/miguelgrinberg/REST-auth
# https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py

from flask import Flask, request, make_response, jsonify, abort
from flask_restful import Resource, Api
from flask.ext.httpauth import HTTPBasicAuth
import json
from sqlalchemy import create_engine

db = create_engine('sqlite:///servers.db')

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'mfrank':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

# PUBLIC API QUERIES
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

# PRIVATE/RESTRICTED API QUERIES
class ManageServer(Resource):
	#decorators = [auth.login_required]

	def get(self, servername):
		# need to ensure /v1/manage/ doesn't return empty json
		# ^
		conn = db.connect()
		query = conn.execute("select * from servers where server='%s'" % servername.lower())
		result = {'server': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		if not len(result['server']) > 0:
			abort(404)
		return result

	# PUT
	# DELETE



api.add_resource(ServerList, '/v1', '/v1/')
api.add_resource(Server, '/v1/<string:servername>','/v1/<string:servername>/')
api.add_resource(ManageServer, '/v1/manage/<string:servername>','/v1/manage/<string:servername>/')

if __name__ == '__main__':
	app.run(debug=True)