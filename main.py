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

class Customer(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    cid = ndb.StringProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    phone=ndb.StringProperty()
       
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)


app = Flask(__name__)


@app.route('/')
def hello():
	log=Login()
	cust=Customer()
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
	
@app.route('/delete')
def delete():
	return  render_template("delete.html")
	
@app.route('/del',methods = ['POST'])
def dele():
	cid=request.form["cid"]
	#ndb.Key(Customer,cid).delete()
	log = Customer.query(Customer.cid==cid)
	for i in log:
		#i.name="hell"
		i.key.delete()
		
	#log1 = Customer.cid()
	
	#skey=log.get()
	#print(log.id())
	#print(log.key.id())
	#print(log.kind())
	#print(log.urlsafe())
	return  redirect('/delete')
	
@app.route('/view',methods = ['POST'])
def home2():
	log = Customer.query()
	a=[]
	for i in log:
		b=[]
		b.append(i.cid)
		b.append(i.name)
		b.append(i.phone)
		b.append(i.address)
		a.append(b)
	"""
	for i in cust:
	
		b=[]
		b.append[i.cid]
		b.append[i.name]
		b.append[i.phone]
		b.append[i.address]
		a.append(b)
		"""
	#c=len(cust)
	response = jsonify(a)
	return response	
	
@app.route('/search')
def search():
	return  render_template("search.html")
	
@app.route('/add')
def add():
	return  render_template("add.html")
	
@app.route('/api', methods=['POST'])
def api():
	cid=request.form["cid"]
	name=request.form["name1"]
	address=request.form["address"]
	phone=request.form["phone"]
	log=Customer()
	log.cid=cid
	log.name=name
	log.address=address
	log.phone=phone
	log.put()
	
	return redirect('/add')

@app.route('/update')
def update():
	return  render_template("update.html")	

@app.route('/up', methods=['POST'])
def up():
	cid=request.form["cid"]
	name=request.form["name1"]
	address=request.form["address"]
	phone=request.form["phone"]
	log=Customer().query(Customer.cid==cid)
	for i in log:
		if name!="":
			i.name=name
		if address!="":
			i.address=address
		if phone!="":
			i.phone=phone
		i.put()
		#i.key.delete()
	
	
	
	#log.cid=cid
	#log.name=name
	#log.address=address
	#log.phone=phone
	#log.put()
	
	return redirect('/update')
	
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
if __name__ == '__main__':
    # This is used when running locally.
    app.run(debug=True)

# [END app]
