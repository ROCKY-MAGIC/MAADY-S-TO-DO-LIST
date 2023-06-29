from sqlalchemy import create_engine, text
import os

connection_string = os.environ['Conn_str']
engine = create_engine(connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": os.environ['doc']
                       }})

con = engine.connect()
con.execute(text("SET GLOBAL  time_zone = '+05:30';"))

def viewer(id, title):
  result = con.execute(
    text(f"SELECT * FROM {id} WHERE title = '{title}';")).all()
  print(result)


def add_user(id):
  con.execute(
    text(
      f"CREATE TABLE {id}(title VARCHAR(50) NOT NULL UNIQUE, description varchar(500),created datetime,modified datetime, completed bit,PRIMARY KEY(title));"
    ))


def add_todo(id, title):
  try:
    con.execute(
      text(
        f"INSERT INTO {id}(title,created,completed) VALUES('{title}',NOW(),1)")
    )

  except:
    return 0


def fetch_det(id):
  det = con.execute(text(f"SELECT title FROM {id};")).all()
  return det


def access_tit(id):
  try:
    txt = fetch_det(id)
    return txt

  except:
    add_user(id)
    txt = dict(fetch_det(id))
    return txt


def modify(id, col, txt, title):
  con.execute(
    text(
      f"UPDATE {id} SET {col} = '{txt}',modified = NOW() WHERE title ='{title}'"
    ))
  con.execute(text("commit"))


def delete(id, title):
  con.execute(text(f"DELETE FROM {id} WHERE title = '{title}';"))


def comp(id, title):
  stat = not bool(
    con.execute(text(
      f"SELECT completed FROM {id} WHERE title = '{title}';")).all()[0][0][-1])
  print(stat)

  con.execute(
    text(f"UPDATE {id} SET completed = {stat} WHERE title = '{title}';"))

def conv(t):
  fin = ""
  bc = [int(i) for i in t[11:].split(":")]
  fin += t[:11]
  
  bc[0] = bc[0]+5
  st = not bc[0] >= 24
  bc[0] = bc[0] if st else bc[0]-24
  bc[1] = bc[1]+30
  st = not bc[1] >= 60
  bc[1] = bc[1] if st else bc[1]-60
  
  bc = [str(i) for i in bc]
  fin += ":".join(bc)+","
  return fin

def time(id, title):
 fin = ""
 for i in {"created","modified"}:
  t = str(con.execute(text(f"SELECT {i} FROM {id} WHERE title = '{title}'")).one()[0])
  
  try:
   fin += conv(t)
  except :
   return fin
  return fin

