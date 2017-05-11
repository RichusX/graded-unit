#!flask/bin/python
from app import app
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.debug = False
app.run(host='0.0.0.0', port=8080)
