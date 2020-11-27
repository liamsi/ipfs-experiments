import random
import time
import sys
import json

import requests
import ipfshttpclient
import matplotlib.pyplot as plt
import numpy as np

headers = {'Content-Type': 'application/json'}

current_milli_time = lambda: int(round(time.time() * 1000))
ipfs = ipfshttpclient.connect()


def run_test(i):
    # TODO it would be better to generate these testfiles in python instead:
    res = ipfs.dag.put(data='testfiles/32_' + str(i) + '.json', format='merkle-leaves')
    cid = str(res["Cid"]["/"])
    paths = []

    num_paths = 150
    for idx in range(0, num_paths):
        path_num = random.randint(0, 31)
        path = cid + "/" + "/".join([char for char in '{0:05b}'.format(path_num)])
        paths.append(path)
    url = 'https://' + sys.argv[1] + '/get_dag_paths'
    start_time = current_milli_time()
    print("sending requests to:", url)
    print(json.dumps(paths))
    end_time = int(requests.post(url, json=json.dumps(paths), headers=headers).content)
    return end_time - start_time


x = []
for i in range(100):
    t = run_test(i)
    print(t)
    x.append(t)

plt.hist(x)
plt.ylabel('Probability')
plt.xlabel('Latency (ms)')
plt.savefig('graph-dag-full.pdf')
