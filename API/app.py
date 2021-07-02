from flask import Flask
from router import create_app

app = Flask(__name__)

application = create_app(app)

if __name__ == '__main__':
    application.run()
