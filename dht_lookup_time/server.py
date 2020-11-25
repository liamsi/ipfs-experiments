import time
import urllib

from flask import Flask
import concurrent.futures
import ipfshttpclient

current_milli_time = lambda: int(round(time.time() * 1000))
ipfs = ipfshttpclient.connect()

app = Flask(__name__)


@app.route('/receive_hash/<ipfs_hash>')
def receive_hash(ipfs_hash):
    ipfs.cat(ipfs_hash)
    return str(current_milli_time())


@app.route('/get_dag_paths/<path:paths>')
def get_dag_paths(paths):
    paths = urllib.parse.unquote(paths)
    paths = paths.split('+')
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_path = {executor.submit(ipfs.dag.resolve, path): path for path in paths}
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (path, exc))
            else:
                print('%r path resolved %s' % (path, len(data)))

    return str(current_milli_time())


app.run(host='0.0.0.0')
