import logging
import os
import ssl
import time
import json
from uuid import uuid4

import requests


def init_logging():
    logger = logging.getLogger('client')
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] - [%(asctime)s] - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def create_ssl_context(certfile, keyfile):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.options |= (
        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
    )
    ssl_context.set_ciphers("EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH")
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    ssl_context.set_alpn_protocols(["h2"])
    return ssl_context


def poll_server(url):
    data = requests.get('{}/{}'.format(url, str(uuid4())), verify='/tmp/ca/cacert.pem', cert=('/tmp/client/cert.pem', '/tmp/client/key.pem'))
    json = data.json()
    logger.info('[{}] Server has something for me => {}'.format(data.status_code, json))


def push_data(url):
    data = requests.post('{}/{}/noise'.format(url, str(uuid4())), verify='/tmp/ca/cacert.pem', cert=('/tmp/client/cert.pem', '/tmp/client/key.pem'))
    json = data.json()
    logger.info('[{}] I had something for the Server => {}'.format(data.status_code, json))



logger = init_logging()

if __name__ == '__main__':
    server = 'https://{}'.format(os.environ['SERVER_HOST'])

    while True:
        try:
            poll_server(server)
            push_data(server)
        except requests.exceptions.RequestException:
            logger.error('Server lost, retrying connection')
        except json.decoder.JSONDecodeError:
            logger.error('Server replied in a bad format')
        finally:
            time.sleep(10)
