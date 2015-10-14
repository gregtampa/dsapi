# https://flask-basicauth.readthedocs.org/en/latest/
# https://flask-restful.readthedocs.org/en/latest/index.html
# https://github.com/miguelgrinberg/REST-auth
# https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py

from flask import Flask, request, make_response, jsonify, abort
from flask_restful import Resource, Api, reqparse
from flask.ext.basicauth import BasicAuth
import json
from sqlalchemy import create_engine

db = create_engine('sqlite:///servers.db')
app = Flask(__name__)
api = Api(app)
app.config['BASIC_AUTH_USERNAME'] = 'demo'
app.config['BASIC_AUTH_PASSWORD'] = 'demo'
basic_auth = BasicAuth(app)


def router_exists(router):
	conn = db.connect()
	query = conn.execute("select count(*) from servers where server='%s'" % router.lower()).fetchone()
	if query[0] == 1:
		return True

# PUBLIC API QUERIES
class All(Resource): # returns the full list of routers
	def get(self):
		conn = db.connect()
		query = conn.execute("select server,port,type from servers")
		return {'servers': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Official(Resource): # convert to return official or community ?
	def get(self):
		conn = db.connect()
		query = conn.execute("select * from servers where type='official'")
		result = {'server': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result # return router information

class Community(Resource): # convert to return official or community ?
	def get(self):
		conn = db.connect()
		query = conn.execute("select * from servers where type='community'")
		result = {'server': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result # return router information

class Query(Resource): # query information on a single router by router address
	@basic_auth.required
	def get(self, servername):
		conn = db.connect()
		query = conn.execute("select * from servers where server='%s'" % servername.lower())
		result = {'server': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		if not len(result['server']) > 0:
			abort(404) # error is bad and you should feel bad, seriously fix this 
		return result


# PRIVATE/RESTRICTED API QUERIES
class Manage(Resource):
	@basic_auth.required

	def __init__(self):
		self.parser = reqparse.RequestParser(trim=True)
		self.parser.add_argument('server', required=True) # server/router address always required
		self.parser.add_argument('port', type=int)
		self.parser.add_argument('type')
		super(Manage, self).__init__()


	def post(self): # we're adding a new router here
		args = self.parser.parse_args(strict=True)
		s,p,t = args['server'],args['port'],args['type']
		if not router_exists(s):
			if p is not None and t is not None:
				conn = db.connect()
				query = conn.execute("insert into servers values ('%s', '%i', '%s')" % (s.lower(), p, t.lower()))
				return {'result': True}, 204
			else:
				return {'result': False}, 400
		else:
			return {'result': False}, 400


	def put(self): # we're updating a router here
		# need to make sure that args['server'] exists in db and then update
		args = self.parser.parse_args(strict=True)
		s,p,t = args['server'],args['port'],args['type']
		if router_exists(s):
			if p is not None and t is not None:
				conn = db.connect()
				query = conn.execute("update servers set port='%i', type='%s' where server='%s'" % (p, t.lower(), s.lower()))
				return {'result': True}, 204
		else:
			return {'result': False}, 400


	def delete(self): # we're removing a router here
		args = self.parser.parse_args(strict=True)
		s = args['server']
		if router_exists(s):
			conn = db.connect()
			query = conn.execute("delete from servers where server='%s'" % s.lower())
			return {'result': True}, 201
		else:
			return {'result': False}, 400



api.add_resource(All, '/v1', '/v1/')
api.add_resource(Official, '/v1/official', '/v1/official/')
api.add_resource(Community, '/v1/community', '/v1/community/')
api.add_resource(Query, '/v1/query/<string:servername>', endpoint='servername')
api.add_resource(Manage, '/v1/manage', '/v1/manage/')

if __name__ == '__main__':
	app.run(debug=True)