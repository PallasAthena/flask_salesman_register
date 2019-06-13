from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sshtunnel import SSHTunnelForwarder
import os
import json

app = Flask(__name__)

with open('/etc/flask_config.json') as config_file:
    config = json.load(config_file)



app.config['SECRET_KEY'] = config.get('SECRET_KEY')

SSH_IP = config.get('SSH_IP')
SSH_USERNAME = config.get('SSH_USERNAME')
SSH_PASSWORD = config.get('SSH_PASSWORD')
SSH_REMOTE_BIND_IP = config.get('SSH_REMOTE_BIND_IP')
SSH_REMOTE_BIND_PORT = config.get('SSH_REMOTE_BIND_PORT')
DATABASE_USER_PASS = config.get('DATABASE_USER_PASS')

tunnel = SSHTunnelForwarder(
    (SSH_IP), ssh_username=SSH_USERNAME, ssh_password=SSH_PASSWORD,
                remote_bind_address=(SSH_REMOTE_BIND_IP, SSH_REMOTE_BIND_PORT)
)
tunnel.start()


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}@127.0.0.1:{}/acornuser'.format(DATABASE_USER_PASS, tunnel.local_bind_port)
app.config['SQLALCHEMY_BINDS'] = {'regions': 'sqlite:///regions.db'}
db = SQLAlchemy(app)


from flaskRegister import routes