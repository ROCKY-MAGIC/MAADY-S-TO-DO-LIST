import os
from flask import Flask, render_template, url_for, redirect, session,request,jsonify
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
    id = profile['user']['userinfo']['email']
    head = profile['id']
    return render_template("mylist.html", name=name, photo=photo,  title = head)

  except:
    return render_template("home.html", photo="static/20230616_144154.png")


@app.route("/logout")
def logout():
  session.pop("user", None)
  return redirect("/")

@app.post("/add_todo")
def add():
  try:
    profile = dict(session)
    id = profile['user']['userinfo']['email']
    id = id[:id.find("@")]
    title = request.form.get("title").rstrip()
    add_todo(id, title)
    return redirect("/user")

  except :
    return redirect("/home")


def page_not_found(e):
    return render_template('404.html',photo="static/20230616_144154.png"), 404

@app.route('/login')
def login():
  redirect_uri = url_for('authorize', _external=1)
  redirect_uri = "https" + redirect_uri[4:]
  print(redirect_uri)
  return oauth.google.authorize_redirect(redirect_uri)

@app.route('/test')
def test():
  con.execute(text("SET GLOBAL  time_zone = '+05:30';"))
  time = list(con.execute(text("SELECT created FROM velraj0004;")))[0][0]
  return jsonify(time)

@app.get('/user')
def user():
  try:
    profile = dict(session)
    id = profile['user']['userinfo']['email']
    id = id[:id.find("@")]
    detail = []
    for i in list(access_tit(id)):
      detail.append(i[0])

    session['id'] = detail
    print(session)
    return redirect(url_for("hello"))
  except:
    return redirect(url_for("hello"))


@app.route('/authorize')
def authorize():
  token = oauth.google.authorize_access_token()

  session['user'] = token
  return redirect('/user')


if __name__ == "__main__":
  
  app.register_error_handler(404, page_not_found)
  app.run(host="0.0.0.0", debug=1)
