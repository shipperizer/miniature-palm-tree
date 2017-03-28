import logging
from uuid import uuid4

from flask import Flask, jsonify


def init_logging(app):
    """
    Add a Streamhandler to the Flask default logger
    """
    sh = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] - [%(asctime)s] - server - %(message)s')
    sh.setFormatter(formatter)
    app.logger.addHandler(sh)
    app.logger.setLevel(logging.INFO)


app = Flask(__name__)
init_logging(app)

@app.route('/<uuid:uuid>')
def serve(uuid):
    return jsonify(uuid=uuid, data={'data_uuid': str(uuid4())})

@app.route('/<uuid:uuid>/noise', methods=['POST'])
def noise(uuid):
    app.logger.info('Noise made {}'.format(str(uuid)))
    return jsonify(uuid=uuid, data={'noise': str(uuid4())})
