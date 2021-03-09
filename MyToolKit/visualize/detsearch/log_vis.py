# log visualize for simpledet, plot iter-level
import re
from matplotlib import pyplot as plt
import numpy as np
from collections.abc import Iterable
import os

def match_one_line(string, pattern):
    res = re.findall(pattern, string)
    return res

def gen_pattern(keys):
    # suit for simpledet log, 
    assert isinstance(keys, Iterable)
    # \d+\.?\d* -> match 1.2, 12345
    # .* -> any char
    base_p = r"(Iter: \d+).*"
    for key in keys:
        base_p += r"({}=\d+\.?\d*).*".format(key)
    return base_p

def read_log(log_path):
    with open(log_path, 'r') as f:
        log = f.readlines()
    return log

def match_log(log_path, keys):
    p = gen_pattern(keys)
    log = read_log(log_path)
    res = dict(iter=[])
    for key in keys:
        res[key] = []
    for line in log:
        try:
            match = match_one_line(line, p)
            if match:
                res['iter'].append(eval(match[0][0].split(':')[-1]))
                for i,key in enumerate(keys):
                    res[key].append(eval(match[0][i+1].split('=')[-1]))
        except re.error:
            print(line, " >> regex error")
    return res
    
def plot_log(log_path, keys, plot_kwargs=dict(marker='*', s=6), savepath='./'):
    match_res = match_log(log_path, keys)
    for key in keys:
        fig,ax = plt.subplots()
        ax.scatter(match_res['iter'], match_res[key], **plot_kwargs)
        ax.plot(match_res['iter'], match_res[key])
        title = 'Iter-%s'%key
        ax.set_title(title)
        plt.savefig(os.path.join(savepath, "{}.jpg".format(title)))


if __name__ == "__main__":
    log_path = "/home/tusimple/Projects/MyToolKit/MyToolKit/visualize/_test.log"
    keys = ['RpnL1', 'RcnnL1']
    # m = match_log(log_path, keys)
    # print(m)
    plot_log(log_path, keys)
    plt.show()
    string = 'Iter: 1665'


