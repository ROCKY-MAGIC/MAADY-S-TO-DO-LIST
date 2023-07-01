from sqlalchemy import create_engine, text
import os

connection_string = os.environ['Conn_str']
engine = create_engine(connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": os.environ['doc']
                       }})

con = engine.connect()


def add_user(id):
  con.execute(
    text(
      f"CREATE TABLE {id}(title VARCHAR(50) NOT NULL UNIQUE, description varchar(500),completed bit,PRIMARY KEY(title));"
    ))


def add_todo(id, title):
  try:
    con.execute(
      text(
        f"INSERT INTO {id}(title,completed) VALUES('{title}',0)")
    )

  except:
    return 0


def fetch_det(id):
  det = con.execute(text(f"SELECT title,completed FROM {id};")).all()
  fin = {}
  for i, a in det:
    fin[i] = bool(a[-1])
  return fin


def access_tit(id):
  try:
    txt = fetch_det(id)
    return txt

  except:
    add_user(id)
    txt = fetch_det(id)
    return txt



def dele(id, title):
  con.execute(text(f"DELETE FROM {id} WHERE title = '{title}';"))


def comp(id, title):
  stat = not bool(
    con.execute(text(
      f"SELECT completed FROM {id} WHERE title = '{title}';")).all()[0][0][-1])
  con.execute(
    text(f"UPDATE {id} SET completed = {stat} WHERE title = '{title}';"))
  con.execute(text("commit"))


