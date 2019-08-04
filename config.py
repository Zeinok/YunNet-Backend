"""
Configuration file for YunNet-Backend
"""
import sanic

# ---Begin configuration file--- #
'''
Password salt
'''

PASSWORD_SALT = 'PutYourSuperLongSaltSecretHereForPasswordHash'

'''
JWT secret
'''
JWT = {
    'useRSA': False,  # RSA support is at low priority
    'jwtSecret': 'PutYourLongJsonWebTokenSecretHereForVerifyingSignature',
    'algorithm': 'HS256',  # set approriate algorithm
    # 'jwtPublicKey': '',
    # 'jwtPrivateKey': '',
}

'''
SQL_CREDENTIALS is the parameters of Connection constructor in PyMySQL
https://pymysql.readthedocs.io/en/latest/modules/connections.html#pymysql.connections.Connection
'''

SQL_CREDENTIALS = {
    'host': 'db',
    'port': 3306,
    'user': 'user',
    'password': 'password',
    'db': 'yunnet',
}

MONGODB_URI = "mongodb://mongo:27017"

'''
Session module endpoint configuration
'''
SESSION_MODULE = {
    'endpoint': 'http://0.0.0.0:5000/Session',
    # 'api_key': '',
}

'''
Google reCaptcha configuration
'''
RECAPTCHA = {
    'enabled': True,
    'secret': '',
}

'''
Set your webhook link here for exception logging.
Leave empty to disable.
'''
WEBHOOK_URL = ""

'''
Sanic app configuration
https://sanic.readthedocs.io/en/latest/sanic/deploying.html
'''
SANIC_APP: dict = {
    'host': '0.0.0.0',
    'port': '8000',
    # 'debug': False,
    'ssl': None,
    # 'sock': None,
    # 'workers': 1,
    # 'loop': None,
    # 'protocol': sanic.websocket.HttpProtocol,
    # 'access_log': True,
}

'''
Sanic configuration
Uncomment if you want to modify it
https://sanic.readthedocs.io/en/latest/sanic/config.html
'''
# REQUEST_MAX_SIZE = 100000000
# REQUEST_BUFFER_QUEUE_SIZE = 100
# REQUEST_TIMEOUT = 60
# RESPONSE_TIMEOUT = 60
# KEEP_ALIVE = True
# KEEP_ALIVE_TIMEOUT = 5
# GRACEFUL_SHUTDOWN_TIMEOUT = 15.0
# ACCESS_LOG = True
# PROXIES_COUNT = -1
# FORWARDED_FOR_HEADER = "X-Forwarded-For"
# REAL_IP_HEADER = "X-Real-IP"
