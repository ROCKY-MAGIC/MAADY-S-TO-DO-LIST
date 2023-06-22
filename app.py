import os
from flask import Flask,render_template,url_for,redirect,session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.secret_key = os.environ['secret']

oauth = OAuth(app)

oauth.register(
    'google',
    client_id = os.environ['id'],
    client_secret = os.environ['secret'],
server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email https://www.googleapis.com/auth/user.gender.read'}
)

@app.route("/")
def hello():
    profile = dict(session)
    try:
     name = profile['user']['userinfo']['name']
     return render_template("home.html", name=name,links="logout",dynamic="logout")
    except:
     print(url_for("login"))
     return render_template("home.html",dynamic="login",links="login",name="None") 
      
@app.route("/logout")
def logout ():
  session.pop("user",None)
  return redirect ("/")

    
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=1)
    #redirect_uri = "https"+redirect_uri[4:]
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    
    session['user'] = token
    return redirect('/')


if __name__ == "__main__":
  app.run(host="0.0.0.0",debug=1)