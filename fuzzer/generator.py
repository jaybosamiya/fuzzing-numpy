import random
import numpy as np
import pickle

try:
    with open('data.pickle', 'rb') as f:
        callables, data_possibilities, data_types = pickle.load(f)
except FileNotFoundError:
    exclude = ['lookfor', 'memmap', 'fromregex', 'fromfile', 'chararray',
               'show_config', 'save', 'savez', 'savez_compressed',
               'int_asbuffer']

    callables = ['np.'+a
                 for a in dir(np)
                 if a not in exclude and callable(getattr(np,a))]

    data_possibilities = [
        '"A"', '("A"*0x100)', '("A"*0x1000)',
        '0', '1', '-1',
        '(2**32)', '(2**32+1)', '(2**32-1)',
        '(2**64)', '(2**64+1)', '(2**64-1)',
        '[]','()','{}', 'set()',
    ]

    data_types = set()


def generate():
    c = random.choice(callables)
    vals = ', '.join(
        random.choice(data_possibilities)
        for _ in range(random.randint(0, 5))
    )
    t = "%s(%s)" % (c, vals)

    print ("-----------------------------------\n%s\n--------------" % t)

    return t

def register(t):
    te = eval(t, {'np':np})
    tt = str(type(te))
    if (tt not in data_types) or (random.randint(0, 10**5) == 0):
        data_possibilities.append(t)
        data_types.add(tt)
        for a in dir(te):
            try:
                if callable(getattr(te,a)):
                    callables.append(t + '.' + a)
            except TypeError: # Happens sometimes for data attribute of np.Str_ objects
                pass

        with open('data.pickle', 'wb') as f:
            pickle.dump((callables, data_possibilities, data_types), f)
