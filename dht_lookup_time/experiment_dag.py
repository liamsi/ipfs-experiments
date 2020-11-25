import random
import time
import sys
import urllib

import requests
import ipfshttpclient
import matplotlib.pyplot as plt

current_milli_time = lambda: int(round(time.time() * 1000))
ipfs = ipfshttpclient.connect()

def run_test(i):
    # TODO it would be better to generate these testfiles in python instead:
    res = ipfs.dag.put(data='testfiles/32_'+str(i)+'.json', format='merkle-leaves')
    cid = str(res["Cid"]["/"])
    paths = ""

    num_paths = 15
    for idx in range(0, num_paths):
        path_num = random.randint(0, 31)
        if idx != 0:
            path = "+"
        else:
            path = ""
        path = path + cid + "/" + "/".join([char for char in '{0:05b}'.format(path_num)])
        print(path)
        paths = paths+path

    start_time = current_milli_time()
    end_time = int(requests.get(sys.argv[1] + '/get_dag_paths/' + paths).content)
    return end_time-start_time

x = []
for i in range(100):
    t = run_test(i)
    print(t)
    x.append(t)

plt.hist(x)
plt.ylabel('Probability')
plt.xlabel('Latency (ms)');
plt.savefig('graph-dag-full.pdf')
