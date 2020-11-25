import time

from flask import Flask


import ipfshttpclient

from werkzeug.routing import BaseConverter


current_milli_time = lambda: int(round(time.time() * 1000))
ipfs = ipfshttpclient.connect()

app = Flask(__name__)

class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)

app.url_map.converters['list'] = ListConverter

@app.route('/receive_hash/<ipfs_hash>')
def receive_hash(ipfs_hash):
    ipfs.cat(ipfs_hash)
    return str(current_milli_time())

@app.route('/get_dag_paths/<list:paths>')
def get_dag_paths(paths):
    for path in paths:

        # TODO run multiple dag gets in parallel
        ipfs.dag.get(path)

    return str(current_milli_time())


app.run(host='0.0.0.0')
