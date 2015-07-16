import os
import uuid
import redis
import json
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#CCFF00"
GREEN = "#33CC33"

COLOR = BLUE
r_env = json.loads(os.getenv('VCAP_SERVICES'))['rediscloud'][0]
r_connection = r_env['credentials']
r_server = redis.Redis(host=r_connection['hostname'], port=r_connection['port'], password=r_connection['password'])

#hostname = services_info['rediscloud'][0]['credentials']['hostname']
#password = services_info['rediscloud'][0]['credentials']['password']
#...and so forth
#then connect with:
# r_connection = redis.Redis(host=hostname,port=port,password=password)

@app.route('/')
def hello():
	global r_server
	r_server.incr('counter')
	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="black">Hi, I'm GUID:<br/>
	{}
	</center>

	<center>
		<h3>
		Page Hits: {}
  		</h3>
	</center>
	</body>
	</html>
	""".format(COLOR,my_uuid, r_server.get('counter'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
