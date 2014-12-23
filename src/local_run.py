__author__ = 'david'
from davesite.app.factory import create_app

app = create_app()

app.run("", 8080)