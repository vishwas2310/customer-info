# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import os
from flask import Flask, request, jsonify
from flask import render_template
import json
from flask import redirect
from google.appengine.ext import ndb

class Login(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()

class Hotel(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    name = ndb.StringProperty()
    location = ndb.StringProperty()
       
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)


app = Flask(__name__)


@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/',methods = ['POST'])
def check():
	usr =  request.form["username"]
	pwd=request.form["pass"]
	count=0
	log = Login.query()
	for i in log:
		if i.username==usr:
			if i.password==pwd:
				return redirect("home")
	
	"""log.username=usr
	log.password=pwd
	log.put()
	
	if(count==1):
		return redirect("home")
		"""
	return render_template("index.html")

@app.route('/signup')
def sign1():
	return  render_template("signup.html")

@app.route('/done',methods = ['POST'])
def sign2():
	usr =  request.form["username"]
	pwd=request.form["password"]
	name=request.form["name1"]
	count=0
	log = Login.query()
	for i in log:
		if i.username==usr:
			return redirect("/signup")
	log = Login()
	log.name=name
	log.username=usr
	log.password=pwd
	log.put()
	return redirect("/")

@app.route('/home')
def home1():
	return  render_template("home.html")

@app.route('/home',methods = ['POST'])
def home2():
	name =  request.form["name1"]
	location=request.form["location"]
	log = Hotel()
	log.name=name
	log.location=location
	log.put()
	return  redirect("/home")
	
@app.route('/search')
def search():
	return  render_template("search.html")
	
@app.route('/api', methods=['POST'])
def api():
    input = request.json
    log = Hotel.query()
    x=[]
    for i in log:
		 if i.location==input:
			 x.append(i.name)
	
    response = jsonify(x)
    return response	
	
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
if __name__ == '__main__':
    # This is used when running locally.
    app.run(debug=True)

# [END app]
