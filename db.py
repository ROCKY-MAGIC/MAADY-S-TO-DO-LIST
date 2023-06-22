from sqlalchemy import create_engine,text
import os

connection_string = my_secret = os.environ['Conn_str']
engine = create_engine(connection_string, 
                      connect_args={
          "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
          }
                      })

with engine.connect() as connection:
  result = connection.execute(text("SELECT * FROM notepad;"))

print(type(result.all()))