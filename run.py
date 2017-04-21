#!flask/bin/python
from app import app

app.debug = False
app.run(host='0.0.0.0', port=1337)
