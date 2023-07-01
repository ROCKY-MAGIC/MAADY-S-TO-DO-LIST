import os
from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from authlib.integrations.flask_client import OAuth
from db import *

app = Flask(__name__)

app.secret_key = os.environ['secret']

oauth = OAuth(app)

oauth.register(
  'google',
  client_id=os.environ['id'],
  client_secret=os.environ['secret'],
  server_metadata_url=
  'https://accounts.google.com/.well-known/openid-configuration',
  client_kwargs={
    'scope':
    'openid profile email https://www.googleapis.com/auth/user.gender.read'
  })


@app.route("/")
def hello():
  profile = dict(session)
  try:
    name = profile['user']['userinfo']['name']
    photo = profile['user']['userinfo']['picture']
    head = profile['id']
    return render_template("mylist.html", name=name, photo=photo, title=head)

  except:
    return render_template("home.html", photo="static/20230616_144154.png")


@app.route("/complete")
def complete():
  title = request.args['title']
  profile = dict(session)
  id = profile['user']['userinfo']['email']
  id = id[:id.find("@")]
  comp(id, title)
  return redirect("/user")


@app.route("/logout")
def logout():
  session.pop("user", None)
  session.pop("id", None)
  return redirect("/")


@app.post("/add_todo")
def add():
  try:
    profile = dict(session)
    id = profile['user']['userinfo']['email']
    id = id[:id.find("@")]
    title = request.form.get("title")
    add_todo(id, title)
    return redirect("/user")

  except:
    return redirect("/home")


def page_not_found(e):
  return render_template('404.html', photo="static/20230616_144154.png"), 404


@app.route('/login')
def login():
  redirect_uri = url_for('authorize', _external=1)
  redirect_uri = "https" + redirect_uri[4:]
  return oauth.google.authorize_redirect(redirect_uri)



@app.get('/user')
def user():
 try:
  profile = dict(session)
  id = profile['user']['userinfo']['email']
  id = id[:id.find("@")]
  detail = access_tit(id)
  session['id'] = detail
  return redirect("/")
 except:
  return redirect("/")


@app.route('/delete')
def delete():
  tit = request.args['tit']
  profile = dict(session)
  id = profile['user']['userinfo']['email']
  id = id[:id.find("@")]
  dele(id, tit)
  return redirect('/user')


@app.route('/authorize')
def authorize():
  token = oauth.google.authorize_access_token()
  session['user'] = token
  return redirect('/user')


if __name__ == "__main__":

  app.register_error_handler(404, page_not_found)
  
  app.run(host="0.0.0.0", debug=1)
