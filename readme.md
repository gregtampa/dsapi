# demonserv API Documentation

The demonserv API exposes a sqlite database with all known community and official DemonSaw routers to allow programmatic access to the data as well as providing a simple means to manipulating that data. Currently all data is returned in JSON format but this might change to XML or the next version (v2) will serve XML.

There are 3 public URIs currently available without authentication or rate limits, these public URIs allow anyone to pull a full list of known routers, just community routers, or just official routers.

A management URI is available for updating and managing the router database, this URI requires authentication by means of BasicAuth.

## Public URIs/Methods

These requests will return json formatted data only, any failed/invalid requests will return HTTP 404.

**For a full list of community and official routers:**

`http://api.demonserv.xyz/v1/`

**For a list of only official routers:**

`http://api.demonserv.xyz/v1/official`

**For a list of only community servers:**

`http://api.demonserv.xyz/v1/community`

**For details of a specific router:**

`http://api.demonserv.xyz/v1/query/<router.address>`



## Management API Access

There is currently 1 URI for database management where POST/PUT/DELETE requests are used to manipulate data.

**Management URI**

`http://api.demonserv.xyz/v1/manage`

**Add a router**

`curl -u user:pass http://api.demonserv.xyz/v1/manage -d server=new.server.com -d port=80 -d type=community -X POST`

**Update a router**

`curl -u user:pass http://api.demonserv.xyz/v1/manage -d server=new.server.com -d port=80 -d type=community -X PUT`

**Remove a router**

`curl -u user:pass http://api.demonserv.xyz/v1/manage -d server=new.server.com -X DELETE`

### Management Responses

* All successful actions will return {'result': True} and HTTP 204

* All unsuccessful actions will return {'result': False} and HTTP 400
