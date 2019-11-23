import logging

from flask import Flask

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
