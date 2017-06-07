import random
import numpy as np
import pickle

exclude = ['lookfor', 'memmap', 'fromregex', 'fromfile', 'chararray',
           'show_config', 'save', 'savez', 'savez_compressed',
           'int_asbuffer']
callables = [a
             for a in dir(np)
             if a not in exclude and callable(getattr(np,a))]

data_possibilities = [
    '"A"', '("A"*0x100)', '("A"*0x1000)',
    '0', '1', '-1',
    '(2**32)', '(2**32+1)', '(2**32-1)',
    '(2**64)', '(2**64+1)', '(2**64-1)',
    '[]','()','{}', 'set()',
]

data_types = []

try:
    with open('data.pickle', 'rb') as f:
        data_possibilities, data_types = pickle.load(f)
except FileNotFoundError:
    pass

def generate():
    c = random.choice(callables)
    vals = ', '.join(
        random.choice(data_possibilities)
        for _ in range(random.randint(0, 5))
    )
    t = "np.%s(%s)" % (c, vals)

    print ("-----------------------------------\n%s\n--------------" % t)

    return t

def register(t):
    te = eval(t, {'np':np})
    tt = str(type(te))
    if tt not in data_types:
        data_possibilities.append(t)
        data_types.append(tt)
    elif random.randint(0, 10**5) == 0:
        data_possibilities.append(t)
    else:
        return

    with open('data.pickle', 'wb') as f:
        pickle.dump((data_possibilities, data_types), f)
