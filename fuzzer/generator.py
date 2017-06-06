import random
import numpy as np

exclude = ['tile','blackman','diag_indices']
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
    # TODO: Use the generated valid code to seed the fuzzer more
    pass
